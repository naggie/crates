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
    def reduce_results(self,results):
        pass

    def __unicode__(self):
        return '%s: %s' % (self.__class__.__name__,self.description)

class JobRunner():

    def __init__(self, job_instance):
        self.job = job_instance

    def run():
        raise NotImplementedError()

    # For logging or updating GUI, NOT USING RESULTS
    def on_start_job(self): pass
    def on_start_enumerate(self): pass
    def on_finish_enumerate(self,count,elapsed_ms): pass
    def on_start_task(self,task): pass
    def on_skip_task(self,task): pass
    def on_task_exception(self,task,exception): pass
    def on_finish_task(self,task,result,elapsed_ms): pass
    def on_finish_job(self,verdict): pass

class SequentialJobRunner(JobRunner):
    def run(self):
        self.on_start_job()
        self.on_start_enumerate()
        tasks = list(self.job.enumerate_tasks())
        count = len(tasks)
        # TODO count time for things
        self.on_finish_enumerate(count,-1)

        results = list()
        for task in tasks:
            try:
                self.on_start_task(task)
                result = self.job.process_task(task)
                results.append(result)
                self.on_finish_task(task,result,-1)
            except TaskSkipped:
                self.on_skip_task(task)
            except Exception as e:
                e.task = task
                self.on_task_exception(task,e)
                if not self.job.best_effort:
                    raise

        verdict = self.job.reduce_results(results)
        self.on_finish_job(verdict)
        return verdict

# mixin
class CliJobRunnerMixin():
    def on_start_enumerate(self):
        print 'Preparing tasks...'

    def on_finish_enumerate(self,count,elapsed_ms):
        self.eta = TimeRemainingEstimator(count)
        self.eta.println('Processing tasks...')
        print self.eta.summary()

    def on_start_task(self,task):
        if self.job.print_task:
            self.eta.println(task)

    def on_finish_task(self,task,result,elapsed_ms):
        self.eta.tick()
        self.eta.rewrite_eta_frame()

    def on_task_exception(self,task,exception):
        self.eta.println('\033[31mFAILURE: %s\033[0m' % exception)
        self.eta.skip()


class StreamingJobRunner(JobRunner):
    # TODO this is old, but rewrite as results generator passed to reducer
    def run(self):
        for task in self.enumerate_tasks():
            try:
                self.process_task(task)
            except TaskError: pass
            except TaskSkipped: pass

def MultiProcessJobRunner(Job):
    # TODO use results queue for IPC --  callbacks
    def run(self):


        self.on_start_enumerate()
        tasks = list(self.job.enumerate_tasks())
        count = len(tasks)
        # TODO count time for things
        self.on_finish_enumerate(count,-1)
        self.tasks_q = Queue(max_size=count)

        for task in tasks:
            self.tasks_q.put(task)

        # results + exceptions + IPC
        self.results_q = Queue(max_size=10)

        pool = list()
        for x in xrange(self.job.max_workers):
            process = Process(target=self._worker)
            process.daemon = True
            process.start()
            pool.append(process)

        for x in range(count):
            result = self.results_q.get()
            if isinstance(result,Exception):
                raise result

        for process in pool:
            # TODO join instead? workers could die if Q is empty
            # as Q is loaded before workers
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


class SequentialCliJobRunner(CliJobRunnerMixin,SequentialJobRunner):
    pass

#class MultiProcessCliJobRunner(CliJobRunnerMixin,MultiProcessJobRunner):
#    pass

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

        self.line = '\033[36m%s\033[0m' % self.line

        reprint(self.line)


    def println(self,string):
        'Print above the progress bar'
        reprint(string)
        stdout.write('\n')
        reprint(self.line)
