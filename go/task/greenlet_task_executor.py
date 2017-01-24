__all__ = ['GreenletTaskExecutor']

import traceback
import gevent
from gevent.queue import JoinableQueue

import go.logging

class GreenletWorker(object):

    def __init__(self, worker_id, task_queue):
        self._worker_id = worker_id
        self._task_queue = task_queue

    def start(self):
        self._worker_greenlet = gevent.spawn(self._work) 

    def _work(self):
        while True:
            task = self._task_queue.get()
            if task is None:
                break
            try:
                task.execute()
            except Exception as ex:
                traceback.print_exc() 
            finally:
                self._task_queue.task_done()

    def stop(self):
        self._task_queue.put(None)
        self._worker_greenlet.join() 


class GreenletTaskExecutor(object):

    def __init__(self, greenlet_size):
        self._greenlet_size = greenlet_size
        self._task_queue = []
        for i in xrange(greenlet_size):
            self._task_queue.append(JoinableQueue())
        assert len(self._task_queue) == greenlet_size
        self._workers = []
        
    def post_task(self, task):
        task_queue_idx = task.affinity % self._greenlet_size 
        self._task_queue[task_queue_idx].put(task)
        task.pre_run() 

    def cancel_task(self, task):
        task_queue_idx = task.affinity % self.greenlet_size 
        self._task_queue[task_queue_idx].remove(task)

    @property
    def pending_task_count(self):
        pending_count = 0
        for i in xrange(self._greenlet_size):
            pending_count += self._task_queue[i].qsize()
        return pending_count

    def startup(self):
        for i in xrange(self._greenlet_size):
            worker = GreenletWorker(i, self._task_queue[i])
            worker.start()
            self._workers.append(worker)
        assert len(self._workers) == self._greenlet_size

    @property
    def worker_count(self):
        return len(self._workers)

    def stop(self):
        for worker in self._workers:
            worker.stop()
        self._workers = []
