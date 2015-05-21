from django.db.models import CharField, ForeignKey, IntegerField, PositiveSmallIntegerField, DateTimeField, URLField

from network.models import Peer

import mutagen

from cas import basicCAS
from os import stat

import mimetypes

# another actor could be used, configured in settings in the future. For
# example, a CAS with local replication or an encrypted Amazon S3 based CAS.
cas = basicCAS()

class ImmutableFile(models.Model):
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

    origin_url = URLField(
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
            original_filepath = filepath,
            mimetype = mimetype.guess_type(filepath),
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
        return '{ref} : {original_filepath}'.format(**self.__dict__)

class CratesImmutableFile(ImmutableFile):
    peer = ForeignKey(Peer,help_text='From whom the file came from (local is OK)')

    deprecates = ForeignKey( 'self',
            null=True,
            help_text="If this file is an upgrade of another, link it here. The deprecated file object and/or record can be deleted later.")
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
    title = CharField(max_length=64)
    artist = CharField(max_length=64)
    album = CharField(max_length=64)
    genre = CharField(max_length=64)
    year = PositiveSmallIntegerField(null=True,blank=True,help_text="Year song was released")

    bpm = PositiveSmallIntegerField(null=True,blank=True,help_text="Detected beats-per-minute of song")
    cover_art_ref = CharField(max_length=64,help_text='CAS ref of album/cover art')

    @classmethod
    def from_mp3(cls,filepath):
        # mp3 specific tag loading goes here
        return super(AudioFile,cls).from_file(*args,**kwargs)

    @classmethod
    def from_aac(cls,filepath):
        # aac specific tag loading goes here
        return super(AudioFile,cls).from_file(*args,**kwargs)


