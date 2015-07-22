from time import time
from datetime import datetime,timedelta
from humanize import naturaltime
from sys import stdout
from multiprocessing import Queue,Process

class TaskSkipped(Exception): pass
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
    description = "Generic Job"

    # Ignore task exceptions? Note that whether this enabled or not, Tasks can
    # be skipped by raising SkipTask
    best_effort = True

    # set dynamically in enumerate_tasks if you like
    timeout_ms = 60*1000

    # The maximum number of concurrent tasks before performance degrades
    # (not applicable for some JobRunners)
    max_workers = 1

    # Should running a job print (using str(task)) to the console?
    # May not be implemented by JobRunner in use.
    print_task = False

    # load parameters in __init__() which is not defined
    def enumerate_tasks(self):
        'Yield tasks of arbitrary format'
        raise NotImplementedError()

    def process_task(self,task):
        raise NotImplementedError()

    # if a verdict is required, assess all results and return one
    # OPTIONAL
    def reduce_results(self,results,exceptions):
        pass

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__,self.description)

class JobRunner():

    def __init__(self, job_instance):
        self.job = job_instance

    def run(): pass

    # For logging or updating GUI
    def on_start_enumerate(self): pass
    def on_finish_enumerate(self,count,elapsed_ms): pass
    def on_start_task(self,task): pass
    def on_task_exception(self,task,exception): pass
    def on_finish_task(self,task,elapsed_ms): pass
    def on_start_job(self): pass
    def on_finish_job(self,verdict): pass


# mixin
class CliJobRunner():
    # TODO rewrite using above hooks only
    def run(self):
        print 'Preparing tasks...'
        tasks = list(self.job.enumerate_tasks())
        task_count = len(tasks)
        eta = TimeRemainingEstimator(task_count)
        eta.println('Processing tasks...')
        print eta.summary()

        results = list()
        for task in tasks:
            try:
                result = self.job.process_task(task)
                eta.tick()
                results.append(result)
            except TaskSkipped:
                eta.skip()
            except Exception as e:
                if not self.job.best_effort:
                    raise
                eta.skip()

            eta.rewrite_eta_frame()

        return self.job.reduce_results(results)

class SequentialJobRunner():

    def run(self):
        self.on_start_job()
        self.on_start_enumerate()
        tasks = list(self.job.enumerate_tasks())
        task_count = len(tasks)
        self.on_finish_enumerate(task_count)

        results = list()
        for task in tasks:
            try:
                self.on_start_task(task)
                result = self.job.process_task(task)
                eta.tick()
                results.append(result)
                self.on_finish_task(task,result)
            except TaskSkipped:
                eta.skip()
            except Exception as e:
                self.on_task_exception(task,e)
                if not self.job.best_effort:
                    raise
                eta.skip()

            eta.rewrite_eta_frame()

        verdict = self.job.reduce_results(results)
        self.on_finish_job(verdict)
        return verdict

class StreamingJobRunner(JobRunner):
    # TODO this is old, but rewrite as results generator passed to reducer
    def run(self):
        for task in self.enumerate_tasks():
            try:
                self.process_task(task)
            except TaskError: pass
            except TaskSkipped: pass

def MultiProcessJob(Job):
    '''Unfinished concept'''
    # set to limit. 0 = unlimited
    queue_size = 0

    def run(self):
        self.tasks = Queue(max_size=self.queuesize)
        self.results = Queue(max_size=self.queuesize)
        count = 0

        # TODO pool instead?
        pool = list()
        for x in xrange(self.queue_size):
            process = Process(target=self._worker)
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
            except Exception as result:
                result.task = task
            finally:
                self.tasks.task_done()

            self.results.push(result)


class SequentialCliJobRunner(SequentialJobRunner,CliJobRunner):
    pass

class MultiProcessCliJobRunner(SequentialJobRunner,CliJobRunner):
    pass

def reprint(*args):
    args = map(str,args)
    line = ' '.join(args)
    # CR, up one line, erase line
    stdout.write('\033[F\r\033[K')
    print(line)

    stdout.flush()

class TimeRemainingEstimator():
    ''' https://xkcd.com/612/ '''

    line = ''

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
        self.line = u'[ {0: >30} ][ {1: 3}% complete ] [{2: <30}][{3: >5.0f}/{4:.0f}]'.format(
            self.summary(),
            percent,
            u'=' * int(percent*30/100),
            self.processed,self.total
        )
        reprint(self.line)


    def println(self,string):
        'Print above the progress bar'
        reprint(string)
        stdout.write('\n')
        reprint(self.line)
