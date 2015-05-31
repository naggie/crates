from django.db.models import CharField, ForeignKey, IntegerField, PositiveSmallIntegerField, DateTimeField, URLField, Model

from network.models import Peer

from mutagen.mp3 import MP3,HeaderNotFoundError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from cas import BasicCAS
from os import stat

import mimetypes

# TODO WARNING: existing objects are currently overwritten. Not sure how I feel about that -- quick abort if already there?

# another actor could be used, configured in settings in the future. For
# example, a CAS with local replication or an encrypted Amazon S3 based CAS.
cas = BasicCAS()

class ImmutableFile(Model):
    '''
    Record representing a cache of the metadata of a given file. Primary key is file ref.

    Derived data only. If you feel the need to modify the file headers, use a
    mutator and then create a new instance of this.

    If an attribute can't be stored in the given filetype header, as long as it
    can be deterministically derived it's OK as long as it's done in a
    classmethod.

    '''
    class Meta:
        # not a model in it's own right. Subclasses will have ImmutableFile
        # fields rather than having 2 tables
        abstract = True

    ref = CharField(max_length=64,primary_key=True,help_text='CAS ref of file')
    hits = IntegerField(default=0,help_text='Number of times the file has been played/read')

    # could migrate to https://github.com/leplatrem/django-sizefield
    size = IntegerField(help_text="Size of file in bytes")

    origin = CharField(
            max_length=255,
            blank=True,
            null=True,
            help_text="Where the file came from, local path or HTTP url etc"
    )

    def mimetype(self):
        '''Returns guessed mimetype for serving this file.
        This assumes origin is a filepath as given by the from_file classmethod.'''
        return mimetypes.guess_type(self.origin) or 'application/octet-stream'

    added = DateTimeField(auto_now=True)

    def map(self):
        'Override this. Gives a relative filepath composed from attributes'
        raise NotImplementedError()

        # ... but here's an example using class attributes
        return '{artist}/{album}/{artist} - {album} - {song}.mp3'.format(**self.__dict__)

    @classmethod
    def from_file(cls,filepath):
        '''Return an instance of this class derived from the given file.
        Override to add features such as ID3 data extraction, chromaprint gen,
        etc. Best used in a threaded work queue based system.'''
        # existing? This is only useful for sub-classes. If a lot of processing
        # is involved, this should save time. However, if extra data is
        # required for new features, this could cause a problem requiring a new
        # index
        ref = cas.insert_file(filepath)
        try: return cls.objects.get(ref=ref)
        except cls.DoesNotExist: pass

        return cls(
            ref = ref,
            size = stat(filepath).st_size,
            origin = filepath,
        )


    def delete(self,*args,**kwargs):
        '''
        Overridden delete method to also remove CAS object.
        See https://docs.djangoproject.com/en/1.8/topics/db/queries/#deleting-objects
        '''
        cas.delete(self.ref)
        super(ImmutableFile,self).delete(*args,**kwargs)


    def __unicode__(self):
        'Give a string representation of what the files is. Similar to mapper. Override!'
        return u'{ref} : {origin}'.format(**self.__dict__)

class CratesImmutableFile(ImmutableFile):
    class Meta:
        # not a model in it's own right. Subclasses will have CratesImmutableFile
        # fields rather than having 2 tables
        abstract = True
    peer = ForeignKey(Peer,help_text='From whom the file came from',null=True)

    deprecates = ForeignKey( 'self',
            null=True,
            help_text="If this file is an upgrade of another, link it here. The deprecated file object and/or record can be deleted later.",
    )


class AudioFile(CratesImmutableFile):
    TYPE_CHOICES = (
            ('MIX','Mix/Compilation'),
            ('SAM','Sample'),
            ('EP','Extended play'),
            ('LOOP','Drum loop'),
            ('ACCA','Acapella'),
            ('TRAC','Track'),
    )

    type = CharField(
            max_length=4,
            choices=TYPE_CHOICES,
            null=True,
            help_text="Type of audio file",
            default='TRAC'
    )

    EXTENSION_CHOICES = (
            ('.mp3','MP3: MPEG-2 Audio Layer III'),
            ('.flac','FLAC: Free Lossless Audio Codec'),
            ('.ogg','OGG: Ogg vorbis'),
            ('.m4a','AAC: Apple audio codec'),
    )

    extension = CharField(
            max_length=5,
            choices=EXTENSION_CHOICES,
            null=True,
            help_text="Codec/filetype of audio file",
            default='TRAC'
    )


    # I'm undecided as to whether these are foreign key joins or text,
    # or both with redundancy. Usage will tell -- django data migrations can be
    # used to change this on an existing database if this is done after the
    # first release.
    title = CharField(max_length=64,null=True)
    artist = CharField(max_length=64,null=True)
    album_artist = CharField(max_length=64,null=True)
    album = CharField(max_length=64,null=True)
    composer = CharField(max_length=64,null=True)
    genre = CharField(max_length=64,null=True)
    year = PositiveSmallIntegerField(null=True,blank=True,help_text="Year song was released")
    track = PositiveSmallIntegerField(null=True,blank=True,help_text="Track on CD release")

    bitrate_kbps = PositiveSmallIntegerField(null=True,blank=True,help_text="MP3/FLAC/etc bitrate")
    length = PositiveSmallIntegerField(null=True,blank=True,help_text="Approximate length in seconds")

    bpm = PositiveSmallIntegerField(null=True,blank=True,help_text="Detected beats-per-minute of song")
    cover_art_ref = CharField(max_length=64,help_text='CAS ref of album/cover art',null=True)

    def __unicode__(self):
        return u'{album_artist} - {album} [{artist}] {album} - {title} [{year}]{extension}'.format(**self.__dict__)

    # @jimjibone, we need to decide how we handle compilations. I think we
    # should detect them and just use a different map for conventional album vs
    # compilations.
    #
    # Note, as we are using symlinks instead of copying files, we can have
    # multiple organisations in the same filesystem. EG: by genre, by label, etc
    #
    # TODO: review mapping system
    # https://github.com/liamks/pyitunes - see attributes that iTunes uses. Specifically album_artist.
    # http://stackoverflow.com/questions/5922622/whats-this-album-artist-tag-itunes-uses-any-way-to-set-it-using-java
    # says it's TPE2: "Band/Orchestra/Accompaniment"
    #
    # So if instead of {artist} we have {album artist} which will default to {artist}. Might work.
    def map(self):
        # ... but here's an example using class attributes
        return u'{album_artist}/{album}/{artist} - {album} - {title}.{extension}'.format(**self.__dict__)

    @classmethod
    def from_mp3(cls,filepath):
        # mp3 specific tag loading goes here
        audioFile = super(AudioFile,cls).from_file(filepath)


        # MP3 class is a superset of ID3 including length and bitrate, etc.
        audio = MP3(filepath)

        if audio.has_key('TIT2'): audioFile.title = audio['TIT2'][0]

        # also default for album_artist
        if audio.has_key('TPE1'): audioFile.artist = audioFile.album_artist = audio['TPE1'][0]
        if audio.has_key('TPE2'): audioFile.album_artist = audio['TPE2'][0]

        if audio.has_key('TALB'): audioFile.album = audio['TALB'][0]
        if audio.has_key('TCON'): audioFile.genre = audio['TCON'][0]
        if audio.has_key('TYER'): audioFile.year = audio['TYER'][0]

        try:
            if audio.has_key('TRCK'): audioFile.track = int(audio['TRCK'][0].partition('/')[0])
        except ValueError: pass

        audioFile.bitrate_kbps = int(audio.info.bitrate/1000)
        audioFile.length = int(audio.info.length)

        # cover art
        if audio.has_key('APIC:Cover'):
            data = audio['APIC:Cover'].data
            audioFile.cover_art_ref = cas.insert_blob(data)
            # record mimtype of cover art...?

        audioFile.extension = 'mp3'

        return audioFile

    @classmethod
    def from_aac(cls,filepath):
        # aac specific tag loading goes here
        return super(AudioFile,cls).from_file(filepath)


