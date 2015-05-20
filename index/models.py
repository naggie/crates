from django.db import models

from network.models import Peer

from cas import basicCAS
from os import stat

cas = basicCAS()

# todo: some kind of discard mech.

class ImmutableFile(models.Model):
    '''
    Record representing a cache of the metadata of a given file. Primary key is file ref.

    Derived or copied data only.
    '''

    ref = models.CharField(max_length=64,primary_key=True,help_text='CAS ref of file')
    hits = models.IntegerField(default=0,help_text='Number of times the file has been played')

    # could migrate to https://github.com/leplatrem/django-sizefield
    size = models.IntegerField(help_text="Size of file in bytes")

    original_filepath = models.CharField(
            max_length=255,
            blank=True,
            null=True,
            help_text="Where the file came from, local path"
    )

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
        )


    def delete(self,*args,**kwargs):
        'Overridden delete method to also remove CAS object'
        cas.delete(self.ref)
        super(ImmutableFile,self).delete(*args,**kwargs)


    def __unicode__(self):
        'Give a string representation of what the files is. Similar to mapper. Override!'
        return self.ref + ' : ' + self.original_filepath

class CratesImmutableFile(ImmutableFile):
    peer = models.ForeignKey(Peer,help_text='From whom the file came from')

    deprecates = models.ForeignKey( 'self',
            null=True,
            help_text="If this file is an upgrade of another, link it here. The deprecated file object and/orrecord can be deleted later.")
    )


# ...

#class AudioFile(CratesImmutableFile):
    #album =i ...

class AudioFile(ImmutableFile):
    TYPE_CHOICES = (
            ('MIX','Mix/Compilation'),
            ('SAM','Sample'),
            ('LP','Longplay'),
            ('LOOP','Drum loop'),
            ('ACCA','Acappella'),
            ('TRAC','Track'),
    )

    type = models.CharField(
            max_length=4,
            choices=TYPE_CHOICES,
            null=True,
            help_text="Type of audio file",
            default='TRAC'
    )


