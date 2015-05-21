from django.db.models import CharField, ForeignKey, IntegerField, PositiveSmallIntegerField, DateTimeField, URLField, Model

from network.models import Peer

from mutagen.mp3 import MP3,HeaderNotFoundError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from cas import basicCAS
from os import stat

import mimetypes


# TODO WARNING: existing objects are currently overwritten. Not sure how I feel about that -- quick abort if already there?

# another actor could be used, configured in settings in the future. For
# example, a CAS with local replication or an encrypted Amazon S3 based CAS.
cas = basicCAS()

class ImmutableFile(Model):
    '''
    Record representing a cache of the metadata of a given file. Primary key is file ref.

    Derived data only. If you feel the need to modify the file headers, use a
    mutator and then create a new instance of this.

    If an attribute can't be stored in the given filetype header, as long as it
    can be deterministically derived it's OK as long as it's done in a
    classmethod.

    '''

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

    mimetype = CharField(
            max_length=64,
            null=True,
            default='application/octet-stream'
    )

    added = DateTimeField(auto_now=True)

    def mapper(self):
        'Override this. Gives a relative filepath composed from attributes'
        raise NotImplementedError()

        # ... but here's an example using class attributes
        return '{artist}/{album}/{artist} - {album} - {song}.mp3'.format(**self.__dict__)

    @classmethod
    def from_file(cls,filepath):
        '''Return an instance of this class derived from the given file.
        Override to add features such as ID3 data extraction, chromaprint gen,
        etc. Best used in a threaded work queue based system.'''
        return cls(
            ref = cas.insert(filepath),
            size = stat(filepath).st_size,
            origin = filepath,
            mimetype = mimetypes.guess_type(filepath),
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
        return '{ref} : {origin}'.format(**self.__dict__)

class CratesImmutableFile(ImmutableFile):
    peer = ForeignKey(Peer,help_text='From whom the file came from (local is OK)')

    deprecates = ForeignKey( 'self',
            null=True,
            help_text="If this file is an upgrade of another, link it here. The deprecated file object and/or record can be deleted later.",
    )


class AudioFile(ImmutableFile):
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

    # I'm undecided as to whether these are foreign key joins or text,
    # or both with redundancy. Usage will tell -- django data migrations can be
    # used to change this on an existing database if this is done after the
    # first release.
    title = CharField(max_length=64,null=True)
    artist = CharField(max_length=64,null=True)
    composer = CharField(max_length=64,null=True)
    album = CharField(max_length=64,null=True)
    genre = CharField(max_length=64,null=True)
    year = PositiveSmallIntegerField(null=True,blank=True,help_text="Year song was released")
    track = PositiveSmallIntegerField(null=True,blank=True,help_text="Year song was released")

    bpm = PositiveSmallIntegerField(null=True,blank=True,help_text="Detected beats-per-minute of song")
    cover_art_ref = CharField(max_length=64,help_text='CAS ref of album/cover art',null=True)

    @classmethod
    def from_mp3(cls,filepath):
        # mp3 specific tag loading goes here
        audioFile = super(AudioFile,cls).from_file(filepath)

        audio = EasyID3(filepath)

        audioFile.title = audio.get('title')
        audioFile.artist = audio.get('artist')
        audioFile.genre = audio.get('genre')
        audioFile.composer = audio.get('composer')
        audioFile.album = audio.get('album')
        #audioFile.track = int(audio.get('tracknumber','0/0').partition('/')[0])

        return audioFile

    @classmethod
    def from_aac(cls,filepath):
        # aac specific tag loading goes here
        return super(AudioFile,cls).from_file(filepath)


