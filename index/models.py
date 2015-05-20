from django.db import models

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

    original_filepath = models.CharField(blank=True,null=True,help_text="Where the file came from, local path")

    def mapper(self):
        'Override this. Gives a relative filepath composed from attributes'
        raise NotImplementedError()

        # ... but here's an example using class attributes
        return '{artist}/{album}/{artist} - {album} - {song}.mp3'.format(**self.__dict__)

    @classmethod
    def from_file(cls,filepath):
        'Return an instance of this class derived from the given file.
        Override to add features such as ID3 data extraction, chromaprint gen,
        etc. Best used in a threaded work queue based system.'
        return cls(
            ref = cas.insert(filepath),
            size = stat(filepath).st_size,
            original_filepath = filepath,
        )


    def delete(self,*args,**kwargs):
        'Overridden delete method to also remove CAS object'
        cas.delete(self.ref)
        super(ImmutableFile,self).delete(*args,**kwargs)

class CratesImmutableFile(ImmutableFile):
    peer = models.ForeignKey('network.models.peer',help_text='From whom the file came from')


# ...

#class AudioFile(CratesImmutableFile):
    #album =i ...

class Mp3File(ImmutableFile):
    pass


