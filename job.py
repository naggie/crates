from time import time
from datetime import datetime,timedelta
from humanize import naturaltime
from sys import stdout

class TaskSkipped(Exception): pass
class TaskError(Exception): pass
# TODO MultiThreadedJob

# Python memory profiler
# sudo pip install --upgrade memory_profiler psutil matplotlib
# mprof run <python script>
# mprof plot

class Job():
    memory_tradeoff = False # Set to True to run generator twice for task count

    def count(self):
        '''Hint total number of tasks if that's faster than enumerating everything.'''
        raise NotImplementedError()

    def enumerate_tasks(self):
        'Yield tasks of arbitrary format'
        raise NotImplementedError()

    def process_task(self,task):
        raise NotImplementedError()

    def hint_length(self):
        '''Used as a memory tradeoff for runtime determination. Override with
        something more efficient if possible. This naive implementation just
        exhausts a generator instance, which is obviously inefficient'''
        return sum(1 for task in self.enumerate_tasks() )

    def run(self):
        '''Can't be bothered to enumerate/crawl manually?'''
        for task in self.enumerate_tasks():
            try:
                self.process_task(task)
            except TaskError: pass
            except TaskSkipped: pass

    # TODO is the memory_tradeoff worth it? I implemented it to save a 13GB memory
    # usage situation that turned out to be an infinite loop. Could pune later
    # eg, 150,000 item crawl saves 20MB on 80MB.... not much...
    def _prepare_tasks(self):
        'set self.tasks (generator or list) and self.task_count'
        if self.memory_tradeoff:
            # Do not need to remember tasks for count
            self.task_count = self.hint_length()
            # ...instead, enumerate twice
            self.tasks = self.enumerate_tasks()
        else:
            self.tasks = list(self.enumerate_tasks())
            self.task_count = len(self.tasks)

    def run_with_progress(self):
        print 'Preparing tasks...'
        self._prepare_tasks()
        eta = TimeRemainingEstimator(self.task_count)
        print 'Processing tasks...'
        print eta.summary()

        for task in self.tasks:
            try:
                self.process_task(task)
                eta.tick()
            except TaskSkipped: eta.skip()
            except TaskError as e:
                print e
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
        if self.total == 0:
            print "Nothing to process!"
            return

        percent = int(100*self.processed/self.total)
        reprint('[ {0: >30} ][ {1: 3}% complete ] [{2: <30}][{3: >5.0f}/{4:.0f}]'.format(
            self.summary(),
            percent,
            u'=' * int(percent*30/100),
            self.processed,self.total
        ))


