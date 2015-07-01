from django.db.models import CharField, IntegerField, DateTimeField,  Model
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

    def hit(self):
        self.hits +=1
        self.save()

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
        return u'{artist}/{album}/{artist} - {album} - {song}.mp3'.format(**self.__dict__)

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
