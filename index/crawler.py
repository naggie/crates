from models import ImmutableFile,AudioFile,HeaderNotFoundError,ID3NoHeaderError
from os.path import splitext,join,islink
from os import access,R_OK,fdopen,unlink
from requests import get
from urlparse import urlparse,urlunparse
from django.core.serializers import get_serializer,get_deserializer
from cas.cas import BasicCAS
from tempfile import mkstemp
from django.conf import settings

from mutagen.mp3 import MP3,HeaderNotFoundError
from mutagen.id3 import ID3,APIC,TIT2,TPE1,TPE2,TCON,TDRC,TALB

from job import Job,TaskError,TaskSkipped,MultiProcessJob
from batch.jobrunner import Job,TaskSkipped

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

    description = """
        Crawl the filesystem for media files, inserting them into
        the database if they don't already exist
    """

    print_task = True

    def __init__(self,directory):
        self.directory = directory

    def enumerate_tasks(self):
        # beware of infinite loop when followlinks is true.
        for dirpath,dirnames,filenames in walk(self.directory,followlinks=False):
            for filename in filenames:
                filepath = join(dirpath,filename)
                root, ext = splitext(filepath)
                # better on the remaining time estimator + memory
                if ext in ('.mp3','.aac'):
                    yield filepath

    def process_task(self,filepath):
        # what sort of file is it? Guess the model to use from extension.
        root, ext = splitext(filepath)

        if islink(filepath):
            raise TaskSkipped('Linked file is probably mapped to CAS')

        #if not access(filepath,R_OK):
        #    raise TaskError('Could not access %s' % filepath)

        if ext == '.mp3':
            AudioFile.from_mp3(filepath).save()

        elif ext == '.aac':
            AudioFile.from_aac(filepath).save()
        else:
            raise TaskSkipped('Not a supported file %s' % filepath)


# TODO: ask the cas if it has the ref first
class PeerCrawler(Job):
    description = """
        Crawl another crates server, downloading and adding files
        that are not on this crates server
    """

    max_workers = 2

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

        # dl audio file into CAS via ref (may already have, even if not index if index is destroyed)
        if not self.cas.has(item.object.ref):
            url = self._build_url(path="cas/%s" % item.object.ref)
            generator = get(url,stream=True).iter_content(chunk_size=8192)
            ref = self.cas.insert_generator(generator)
        else:
            ref = item.object.ref

        if item.object.cover_art_ref and not self.cas.has(item.object.cover_art_ref):
            url = self._build_url(path="cas/%s" % item.object.cover_art_ref)
            generator = get(url,stream=True).iter_content(chunk_size=8192)
            self.cas.insert_generator(generator)

        if ref != item.object.ref:
            self.cas.delete(ref)
            raise IOError(ref)

        item.object.save(ref)

        assert ref == item.object.ref # network/disk/h4x0r problem? Just exit now. Later throw/catch/delete and warn or something.

class SoundcloudCrawler(Job):
    description = """
        Crawl a soundcloud user's favorites, downloading new songs.
        Produces best quality obtainable. Useful as artists sometimes pull songs.
    """

    # stay relatively stealthy
    max_workers = 1

    # TODO: cursor system to grab all favorites (api v2, see likes page on web and net activity)
    def __init__(self,username):
        self.likes_url = "http://api.soundcloud.com/users/%s/favorites.json" % username
        self.username = username
        # TODO Grab API key from database
        from os import getenv
        self.key = getenv('SOUNDCLOUD_API_KEY')


    def enumerate_tasks(self):
        for item in get(self.likes_url,params={'client_id':self.key,'limit':9999}).json():
            # Might be None. Can be hacked: s/large/original/g
            cover_art_url = item.get('artwork_url') or item['user'].get('avatar_url')
            cover_art_url = cover_art_url.replace('large','original')
            # 'download' file is normally 320Kbps vs 128Kbps for stream_url
            if item.get('downloadable'):
                # deprecated
                #mp3_url = item.get('download_url')
                # this will be a 302 redirect to CDN
                mp3_url = 'http://api.soundcloud.com/tracks/%s/download' % item['id']
            else:
                # :( buy it later, then use the upgrade mutator
                #mp3_url = item['stream_url']
                mp3_url = 'http://api.soundcloud.com/tracks/%s/stream' % item['id']

            # they use an incompatible SSL setup. HTTP is fine.
            mp3_url = mp3_url.replace('https','http')
            cover_art_url = cover_art_url.replace('https','http')

            yield {
                'title': item['title'],
                'artist': item['user']['username'],
                'album': item['user']['username'] + 'on soundcloud',
                'album_artist': self.username,
                'genre': item['genre'],
                'comment': item['description'],
                'year': item['created_at'][:4], # must be u''
                'mp3_url': mp3_url,
                'cover_art_url': cover_art_url,
                "origin": item['permalink_url'],
                #"origin":item['purchase_url'], # which is better?
            }

    def process_task(self,track):
        # does it exist already? Using enough fields to disambiguate without
        # having an extra non-standard ID. Should also match tracks produced by the old system, otherwise all of the dictionary would do.
        if AudioFile.objects.filter(
            artist=track['artist'],
            title=track['title'],
            genre=track['genre'],
        ).exists():
            raise TaskSkipped()

        # download MP3 file (tags could be non-existent to great)
        fd,filepath = mkstemp(dir=settings.CAS_DIRECTORY,prefix="soundcloud_mp3_")
        # os-level, not python File. Cannot be GC'd. Plug leak.
        try:
            with fdopen(fd,'wb') as f:
                mp3_res = get(track['mp3_url'],params={'client_id':self.key},stream=True)

                if mp3_res.status_code != 200:
                    raise Exception('Could not download {0}, got HTTP {1}'.format(track['mp3_url'],mp3_res.status_code))

                for chunk in mp3_res.iter_content(chunk_size=8192):
                    f.write(chunk)

            # inspect headers (some can be better than 'meta' can provide)
            audio = MP3(filepath)
            # add ID3 headers if not there (probably isn't) will except if they are
            try: audio.add_tags()
            except: pass

            # download cover art
            cover_res = get(track['cover_art_url'])
            if cover_res.status_code != 200:
                # undo hack
                cover_res = get(track['cover_art_url'].replace('large','original'))

            if cover_res.status_code == 200:
                # else, hopefully there is one embedded
                cover_art = cover_res.content

                audio.tags.add(
                    APIC(
                        encoding=3, # 3 is for utf-8
                        mime='image/jpeg',
                        type=3, # 3 is for the cover image
                        desc=u'Cover',
                        data=cover_res.content
                    )
                )

            audio.tags.add(TIT2(encoding=3, text=track['title']))
            audio.tags.add(TALB(encoding=3, text=track['album']))
            audio.tags.add(TPE1(encoding=3, text=track['artist']))
            audio.tags.add(TPE2(encoding=3, text=track['album_artist']))
            audio.tags.add(TCON(encoding=3, text=track['genre']))
            audio.tags.add(TDRC(encoding=3, text=track['year']))

            # save header to tmp mp3 file
            audio.save()

            # insert into index
            audioFile = AudioFile.from_mp3(filepath)
            AudioFile.origin = track['origin']
            AudioFile.save()

        finally:
            # GC
            unlink(filepath)


