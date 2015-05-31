from models import ImmutableFile,AudioFile,HeaderNotFoundError,ID3NoHeaderError
from os.path import splitext,join
from os import access,R_OK
from requests import get
from urlparse import urlparse,urlunparse
from django.core.serializers import get_serializer,get_deserializer
from cas import BasicCAS
from job import Job,TaskError,TaskSkipped


try:
    from os.scandir import scandir,walk # python 3.5, fast
except ImportError:
    try:
        from scandir import walk # python 2.x, scandir from pip
    except ImportError:
        from os import walk # python 2.x, native and slow

# TODO split into separate module, file per crawler, import in __init__.py

# crawler could have a worker thread and queue, depending on benchmark results
class FileCrawler(Job):
    memory_tradeoff = False

    def __init__(self,directory):
        self.directory = directory

    def enumerate_tasks(self):
        # beware of infinite loop when followlinks is true.
        for dirpath,dirnames,filenames in walk(self.directory,followlinks=False):
            for filename in filenames:
                filepath = join(dirpath,filename)
                yield filepath

    def process_task(self,filepath):
            try:
                # what sort of file is it? Guess the model to use from extension.
                root, ext = splitext(filepath)

                if not access(filepath,R_OK):
                    raise TaskError('Could not access %s' % filepath)

                if ext == '.mp3':
                    AudioFile.from_mp3(filepath).save()

                elif ext == '.aac':
                    AudioFile.from_aac(filepath).save()
                else:
                    raise TaskSkipped()
            # In this case, should make one. In theory, the acoustid mutator
            # should populate them later.
            # TODO: add ID3 tags when there are none.
            # I'm not especially sure this will happen often enough to care.
            except HeaderNotFoundError: raise TaskSkipped()
            except ID3NoHeaderError: raise TaskSkipped()
            # empty but existing tags. Don't care atm.
            except IndexError: raise TaskSkipped()
            except TaskSkipped: raise
            except TaskError: raise
            # invalid characters, and whatever else I can't be bothered to catch
            # TODO: collect these exception for a report summary.
            except Exception as e: print e


# Could also have a PeerCrawler in here to crawl over HTTP...
# + SoundcloudCrawler? (using origin_url to download new only)
# Even a soundcloud crawler? (using origin_url to download new only)
# TODO hooks for progress, or a base class with a generator and unit processor.

class PeerCrawler(Job):
    def __init__(self,peer):
        self.cas = BasicCAS()
        self.peer = peer
        self.urlobj = urlparse(peer.url)
        self.deserialize = get_deserializer('json')

    def _build_url(self,**kwargs):
        return urlunparse( self.urlobj._replace(**kwargs) )


    def enumerate_tasks(self):
        url = self._build_url(path="dump/AudioFiles")
        json = get(url).text
        return self.deserialize(json)


    def process_task(self,item):
        # N.B. item is not a simple django model object, but behaves like one

        # this relationship is lost by the serialiser (currently)
        item.object.ref = item.object.pk

        # remember peer for stats/filtering
        item.object.peer = self.peer

        # TODO: can I just do item.exists() or something?
        if AudioFile.objects.filter(ref=item.object.ref).exists():
            raise TaskSkipped()

        # dl audio file into CAS via ref
        url = self._build_url(path="cas/%s" % item.object.ref)
        generator = get(url,stream=True).iter_content(chunk_size=8192)
        ref = self.cas.insert_generator(generator)

        if item.object.cover_art_ref:
            url = self._build_url(path="cas/%s" % item.object.cover_art_ref)
            generator = get(url,stream=True).iter_content(chunk_size=8192)
            self.cas.insert_generator(generator)

        if ref != item.object.ref:
            self.cas.delete(ref)
            raise TaskError(ref)

        item.object.save(ref)

        assert ref == item.object.ref # network/disk/h4x0r problem? Just exit now. Later throw/catch/delete and warn or something.

def SoundcloudCrawler(Job):
    def __init__(self,usernames):
        self.usernames = liar(usernames)


        # TODO Grab API key from database

    def enumerate_tasks(self):
        pass

    def process_task(self,item):
        pass

