from models import ImmutableFile
from os.path import walk,splitext

# crawler could have a worker thread and queue, depending on benchmark results
class FileCrawler():
    def __init__(self):
        pass

    def _insert(self,filepath):
        # what sort of file is it? Guess the model to use from extension.
        root, ext = splitext(filepath)

        if ext == '.mp3':
            Mp3File.gt


    def crawl(self,directory):
        pass



