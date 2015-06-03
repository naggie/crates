from cas import BasicCAS
from index.models import AudioFile

import pyinotify
cas = BasicCAS()

wm = pyinotify.WatchManager()

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_OPEN(self, event):
        #ref = cas.reverse(event.pathname)
        if event.dir: return
        d = event.pathname
        #try:
        ref = d[-69:-67]+d[-66:-4]

        audiofile = AudioFile.objects.get(ref=ref)
        audiofile.hit()
        audiofile.save
        #except:
        #    pass

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

for directory in cas._bins():
    wdd = wm.add_watch(directory, pyinotify.IN_OPEN)

notifier.loop()
