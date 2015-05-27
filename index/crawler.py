from models import ImmutableFile,AudioFile,HeaderNotFoundError,ID3NoHeaderError
from os.path import splitext,join
from os import access,walk,R_OK
from requests import get
from urlparse import urlparse,urlunparse
from django.core.serializers import get_serializer,get_deserializer
from cas import BasicCAS

class BaseCrawler():
    '''WIP base class generator based crawler so progress can be seen'''

    self.added = 0
    self.failed = 0
    self.skipped = 0

    def count(self):
        '''Return total number of objects to crawl'''
        raise NotImplementedError()

    def enumerate(self):
        raise NotImplementedError()

    def add(self,item):
        raise NotImplementedError()

    def crawl(self):
        '''Can't be bothered to enumerate/crawl manually?'''
        for item in self.enumerate():
            self.add(item)


# crawler could have a worker thread and queue, depending on benchmark results
class FileCrawler():
    def __init__(self):
        pass

    def crawl(self,directory):
        for filepath in self._enumerate(directory):
            try:
                self._insert(filepath)
            except HeaderNotFoundError: continue
            except ID3NoHeaderError: continue


    def _insert(self,filepath):
        # what sort of file is it? Guess the model to use from extension.
        root, ext = splitext(filepath)

        if ext == '.mp3':
            print filepath # don't do this, keep track of progress with generator etc
            AudioFile.from_mp3(filepath).save()

        elif ext == '.aac':
            AudioFile.from_aac(filepath).save()

        # ... otherwise who cares.


    @staticmethod
    def _enumerate(directory):
        'Generator to list all accessable absolute files in given directory, recursively'

        for dirpath,dirnames,filenames in walk(directory,followlinks=True):
            for filename in filenames:
                filepath = join(dirpath,filename)

                if access(filepath,R_OK):
                    yield filepath


# Could also have a PeerCrawler in here to crawl over HTTP...
# + SoundcloudCrawler? (using origin_url to download new only)
# Even a soundcloud crawler? (using origin_url to download new only)
# TODO hooks for progress, or a base class with a generator and unit processor.

class PeerCrawler(BaseCrawler):
    def __init__(self,peer):
        self.cas = BasicCAS()
        self.peer = peer
        self.urlobj = urlparse(peer.url)
        self.deserialize = get_deserializer('json')

    def _build_url(self,**kwargs):
        return urlunparse( self.urlobj._replace(**kwargs) )


    def enumerate(self):
        url = self._build_url(path="dump/AudioFiles")
        json = get(url).text
        return self.deserialize(json)


    def add(self,item):
        # N.B. item is not a simple django model object, but behaves like one

        # this relationship is lost by the serialiser (currently)
        item.object.ref = item.object.pk

        # remember peer for stats/filtering
        item.object.peer = self.peer

        # dl audio file into CAS via ref. If we get this far, the file is
        # assumed to be good because a query was (hopefully) used requiring a
        # certain quality. If this peer is bad, we can delete by peer thanks to
        # the above relationship
        url = self._build_url(path="cas/%s" % item.object.ref)
        generator = get(url,stream=True).iter_content(chunk_size=8192)
        ref = self.cas.insert_generator(generator)

        if ref != item.object.ref:
            self.cas.delete(ref)
            self.failed +=1
        elif not AudioFile.objects.filter(ref=item.object.ref).exists():
            item.object.save(ref)
            self.added +=1
        else:
            self.skipped +=1

        assert ref == item.object.ref # network/disk/h4x0r problem? Just exit now. Later throw/catch/delete and warn or something.
        # TODO fix potential leak of garbage here

