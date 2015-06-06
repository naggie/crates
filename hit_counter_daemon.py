from cas import BasicCAS
from index.models import AudioFile
from time import sleep
from threading import Thread
from sys import stdout

from django.conf import settings
WATCH_COLLECT_TIME = settings.WATCH_COLLECT_TIME

# Shortcomings:
# * When vault player/admin plays, album art is downloaded too, making the request filtered.
# * If burst%5 = 1, there will be a mis-hit


# This changes for no reason
try: from queue import Queue,Full,Empty
except ImportError: from Queue import Queue,Full,Empty

import pyinotify
cas = BasicCAS()

wm = pyinotify.WatchManager()
q = Queue(maxsize=20)

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_OPEN(self, event):
        # TODO ref = cas.reverse(event.pathname)
        if event.dir:
            # the directory itself, a CAS bin
            return

        d = event.pathname
        try:
            ref = d[-69:-67]+d[-66:-4] # TODO move to CAS
            stdout.write('.')
            stdout.flush()
            q.put(ref,block=False)

        except Full:
            pass

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

for directory in cas._bins():
    wdd = wm.add_watch(directory, pyinotify.IN_OPEN)

def worker():
    last = None
    while True:
        refs = set()
        sleep(WATCH_COLLECT_TIME)
        try:
            while True:
                refs.add( q.get(block=False) )
                q.task_done()
        except Empty: pass

        if len(refs) == 1:
            ref = refs.pop()
            if ref != last:
                try:
                    audioFile = AudioFile.objects.get(ref=ref)
                    audioFile.hit()
                except AudioFile.DoesNotExist:
                    pass
                if last == None: print # dots
                print audioFile

            last = ref
        else:
            last = None


t = Thread(target=worker)
t.daemon = True
t.start()

notifier.loop()
