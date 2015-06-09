from time import time
from datetime import datetime,timedelta
from humanize import naturaltime
from sys import stdout
from multiprocessing import Queue,Process

class TaskSkipped(Exception): pass
class TaskError(Exception): pass
# TODO MultiThreadedJob

# Python memory profiler
# sudo pip install --upgrade memory_profiler psutil matplotlib
# mprof run <python script>
# mprof plot

# Note that a memory_tradeoff feature was implemented after large memory usage
# (14GB ish) triggered me to implement a system to pre-enumerate all tasks just
# to count them first. After the memory usage turned out to be the result of an
# infinite loop instead, only saving 20MB out of 80MB, the feature was deemed
# excessive and removed. Should it be required later, see
# b7e9924b01cf3d70b74de43fb9c731f91c33fa0e

class Job():
    def count(self):
        '''Hint total number of tasks if that's faster than enumerating everything.'''
        raise NotImplementedError()

    def enumerate_tasks(self):
        'Yield tasks of arbitrary format'
        raise NotImplementedError()

    def process_task(self,task):
        raise NotImplementedError()

    def run(self):
        '''Can't be bothered to enumerate/crawl manually?'''
        for task in self.enumerate_tasks():
            try:
                self.process_task(task)
            except TaskError: pass
            except TaskSkipped: pass

    def run_with_progress(self):
        print 'Preparing tasks...'
        tasks = list(self.enumerate_tasks())
        task_count = len(tasks)
        eta = TimeRemainingEstimator(task_count)
        print 'Processing tasks...'
        print eta.summary()

        for task in tasks:
            try:
                self.process_task(task)
                eta.tick()
            except TaskSkipped:
                eta.skip()
            except TaskError as e:
                print 'TaskError:',e,'\n'
                eta.skip()

            eta.rewrite_eta_frame()


def MultiProcessJob(Job):
    # set to limit. 0 = unlimited
    queue_size = 0

    def run(self):
        self.tasks = Queue(max_size=self.queuesize)
        self.results = Queue(max_size=self.queuesize)
        count = 0

        # TODO pool instead?
        pool = list()
        for x in xrange(self.queue_size):
            process = Process(target=self.worker)
            process.daemon = True
            process.start()
            pool.append(process)

        for task in self.enumerate_tasks():
            self.tasks.put(task)
            count +=1

        # if results are (or progress is) not required, join can be done here
        #self.tasks.join()

        for x in xrange(count):
            result = self.results.get()
            if isinstance(result,Exception):
                raise result

        for process in pool:
            process.terminate()


    def _worker(self):
        while True:
            task = self.tasks.get()
            try:
                result = self.process_task(task)
                self.tasks.task_done()
            except Exception as result:
                pass

            self.results.push(result)



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
        reprint(u'[ {0: >30} ][ {1: 3}% complete ] [{2: <30}][{3: >5.0f}/{4:.0f}]'.format(
            self.summary(),
            percent,
            u'=' * int(percent*30/100),
            self.processed,self.total
        ))


