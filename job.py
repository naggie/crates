from time import time
from datetime import datetime,timedelta
from humanize import naturaltime
from sys import stdout

class TaskSkipped(Exception): pass
class TaskError(Exception): pass
class Job():
    '''WIP base class generator based crawler so progress can be seen'''
    def count(self):
        '''Return total number of objects to crawl if that's faster than enumerating everything.'''
        raise NotImplementedError()

    def enumerate(self):
        raise NotImplementedError()

    def add(self,item):
        raise NotImplementedError()

    def crawl(self):
        '''Can't be bothered to enumerate/crawl manually?'''
        for item in self.enumerate():
            try:
                print item
                self.add(item)
            except TaskError: pass
            except TaskSkipped: pass

    def crawl_with_progress(self):
        print 'Enumerating tasks...'
        items = list(self.enumerate())
        eta = TimeRemainingEstimator( len(items) )

        print eta.summary()

        for item in items:
            try:
                self.add(item)
                eta.tick()
            except TaskSkipped:
                eta.skip()

            eta.rewrite_eta_frame()

def reprint(*args):
    args = map(str,args)
    line = ' '.join(args)
    # CR, up one line, erase line
    stdout.write('\033[F\r\033[K')
    print(line)

    stdout.flush()

class TimeRemainingEstimator():
    ''' https://xkcd.com/612/ '''

    def __init__(self, total):
        self.total = total
        self.processed = 0.0
        self.start = time()

    def tick(self,count=1.0):
        self.processed +=count

    def skip(self,count=1.0):
        self.total -=count

    def _get_remaining_seconds(self):
        elapsed = time() - self.start
        rate = self.processed/elapsed

        deficit = self.total - self.processed

        return deficit/rate

    def summary(self):
        try:
            eta = self._get_remaining_seconds()
        except ZeroDivisionError:
            return 'Estimating time remaining...'

        return naturaltime(datetime.now() + timedelta(seconds=eta)).replace('from now','remaining')


    def rewrite_eta_frame(self):
        percent = int(100*self.processed/self.total)
        reprint('[ {0: >30} ][ {1: 3}% complete ] [{2: <30}][{3: >5}/{4}]'.format(
            self.summary(),
            percent,
            u'=' * int(percent*30/100),
            int(self.processed),int(self.total)
        ))


