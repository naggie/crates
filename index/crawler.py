from models import ImmutableFile
from os.path import walk,splitext,join,access

# crawler could have a worker thread and queue, depending on benchmark results
class FileCrawler():
    def __init__(self):
        pass

    def crawl(self,directory):
        for filepath in self._enumerate(directory):
            self._insert(filepath)


    def _insert(self,filepath):
        # what sort of file is it? Guess the model to use from extension.
        root, ext = splitext(filepath)

        if ext == '.mp3':
            f = Mp3File.from_file(filepath)
            f.save()

        # ... otherwise who cares.


    @staticmethod
    def _enumerate(directory):
        'Generator to list all accessable absolute files in given directory, recursively'

        for dirpath,dirnames,filenames in walk(directory,followlinks=True):
            for filename in filenames:
                filepath = join(dirpath,filename)

                if access(filepath,R_OK):
                    yield filepath



