from django.db.models import CharField, ForeignKey, IntegerField, PositiveSmallIntegerField, DateTimeField, URLField, Model, UUIDField
from django.contrib.auth.models import User
from mutagen.mp3 import MP3,HeaderNotFoundError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from cas.models import cas,ImmutableFile
import unicodedata
import re

# TODO WARNING: existing objects are currently overwritten. Not sure how I feel about that -- quick abort if already there?


class CratesImmutableFile(ImmutableFile):
    class Meta:
        # not a model in it's own right. Subclasses will have CratesImmutableFile
        # fields rather than having 3 tables
        abstract = True
    user = ForeignKey(User,help_text='From whom the file came from',null=True)

    deprecated_by = ForeignKey( 'self',
            null=True,
            help_text="""If a mutator finds or creates a better file, it can be
            linked here. Garbage collection can remove all files that have been
            deprecated from the CAS, saving disk. Future crawls will not add
            the file to the CAS any more.""",
    )

    def slugify(self):
        '''Return a cleaned dict() of this instance suitable for filepaths'''
        cleaned = dict()
        for key,val in self.__dict__.iteritems():
            try:
                # str/int only
                val = unicode(val)
                val = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore')
                val = re.sub('[^\w\s\-\.]', '', val).strip()
                cleaned[key] = val
            except:
                continue

        return cleaned

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
            help_text="Codec/filetype of audio file",
    )


    # I'm undecided as to whether these are foreign key joins or text,
    # or both with redundancy. Usage will tell -- django data migrations can be
    # used to change this on an existing database if this is done after the
    # first release.
    title = CharField(max_length=64,null=True)
    artist = CharField(max_length=64,null=True)
    album = ForeignKey(Album)

    # stored redundantly, yes -- some do not belong to an album
    cover_art_ref = CharField(max_length=64,help_text='CAS ref of album/cover art',null=True)

    composer = CharField(max_length=64,null=True)
    genre = CharField(max_length=64,null=True)
    year = PositiveSmallIntegerField(null=True,blank=True,help_text="Year song was released")
    track = PositiveSmallIntegerField(null=True,blank=True,help_text="Track on CD release")

    bitrate_kbps = PositiveSmallIntegerField(null=True,blank=True,help_text="MP3/FLAC/etc bitrate")
    length = PositiveSmallIntegerField(null=True,blank=True,help_text="Approximate length in seconds")

    bpm = PositiveSmallIntegerField(null=True,blank=True,help_text="Detected beats-per-minute of song")

    mbid = UUIDField(
        blank=True,
        null=True,
        help_text="MusicBrainz ID",
        hyphenate=True,
    )

    def __unicode__(self):
        return u'{album_artist} - {album} [{artist}] {album} - {title} [{year}]{extension}'.format(**self.slugify())

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
        return u'{album_artist}/{album}/{title} - {album} - {artist}{extension}'.format(**self.slugify())

    @classmethod
    def from_mp3(cls,filepath):
        # mp3 specific tag loading goes here
        audioFile = super(AudioFile,cls).from_file(filepath)


        # MP3 class is a superset of ID3 including length and bitrate, etc.
        audio = MP3(filepath)

        if audio.has_key('TIT2'): audioFile.title = audio['TIT2'][0]

        album_artist = 'Various Artists'
        # Artist is default for album_artist
        if audio.has_key('TPE1'): audioFile.artist = album_artist = audio['TPE1'][0]
        if audio.has_key('TPE2'): album_artist = audio['TPE2'][0]

        if audio.has_key('TCON'): audioFile.genre = audio['TCON'][0]


        if audio.has_key('APIC:Cover'):
            data = audio['APIC:Cover'].data
            audioFile.cover_art_ref = cas.insert_blob(data)
            # record mimetype of cover art...?

        if audio.has_key('TALB'):
            audioFile.album = Album.objects.get_or_create(
                name = audio['TALB'][0],
                artist = album_artist,
            )
            audioFile.album.cover_art_ref = audioFile.cover_art_ref
            audioFile.album.save()

        # TODO: fix this; TDRC is an ID3TimeStamp which should be converted to a datetime (field)
        #if audio.has_key('TDRC'): audioFile.year = audio['TDRC'][0]

        try:
            if audio.has_key('TRCK'): audioFile.track = int(audio['TRCK'][0].partition('/')[0])
        except ValueError: pass

        audioFile.bitrate_kbps = int(audio.info.bitrate/1000)
        audioFile.length = int(audio.info.length)

        # cover art

        audioFile.extension = '.mp3'

        return audioFile

    @classmethod
    def from_aac(cls,filepath):
        # aac specific tag loading goes here
        return super(AudioFile,cls).from_file(filepath)


def Album(Model):
    album = CharField(max_length=64)
    cover_art_ref = CharField(max_length=64,help_text='CAS ref of album/cover art',null=True)
    artist = CharField(max_length=64,null=True)

    mbid = UUIDField(
        blank=True,
        null=True,
        help_text="MusicBrainz ID",
        hyphenate=True,
    )
