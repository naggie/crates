# Changes
Job becomes an interface instead. 

Best effort flag, or TaskSkipped. TaskError aborts. TaskTimeout...?

JobRunner: What the subclass currently is. Enumerates and runs tasks.
Sequential and Multiprocess job runner, subclassed (hook based) for web based
and CLI based.

Jobrunner can predict ETA based on type of job:

   1. Granular jobs, just predict based on average time
   2. Consistent jobs (builds, CI, ...) jobs which take a consistent amount of
      time with low task count.
   3. Jobs with no ETA

Timeout system (TaskTimeout Exception)


Collecting all tasks for eta an results for reducing is fine, memory usage
shouldn't be an issue for any real use case.

# Web based global jobs (mutex)
Crates will have a global context that only one job can run at a time. A
scheduler can initiate, and so can a user if no jobs are active.

Available jobs are defined and parameterised in settings. Job state is stored
in database or object store (redis?).

Web client polls (or websocket) for progress, eta, etc.


# Pipeline
Some jobs can be chained, the input of one to the output of the next. This can
be manual or managed by a pipeline class.

Only use a pipeline if there are inter-task/job dependencies.

Crucially, an `reduce_results()` method can be defined to iterate over all
results, returning kwargs for the next job __init__ method

Pipeline could be a job itself.

# Scheduler
For crates, to initiate global tasks at specified time (python sched), queue
based mutex system?



### Dsignage
websocket command based
<command> {kwargs}
