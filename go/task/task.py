__all__ = ['Task']

import uuid
import time
import traceback

import go.logging

@go.logging.class_wrapper
class Task(object):

    def __init__(self):
        self._task_id = uuid.uuid1()

    @property            
    def tid(self):
        return self._task_id

    @property            
    def affinity(self):
        return 0

    def pre_run(self):
        self._start_time = time.time() 

    def execute(self):
        try:
            self.run()
            self.post_run()
        except Exception as ex:
            traceback.print_exc() 

    def run(self):
        pass

    def post_run(self):
        self._end_time = time.time() 
