from models import ImmutableFile,AudioFile,HeaderNotFoundError,ID3NoHeaderError
from os.path import splitext,join
from os import access,walk,R_OK
from requests import get

from cas impoer BasicCAS

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

class PeerCrawler():
    def __init__(self,peer_url):
        self.cas = BasicCAS()

    def crawl(self,url):
        pass


    def _insert(self,obj):
        obj.ref
        generator = get(url,stream=True).inter_content(chunk_size=8192)
        self.cas.insert_generator(generator)
        assert ref == obj.ref
        # TODO fix potential leak of garbage here

