__all__ = ['TaskExecutor']

class TaskExecutor(object):
    
    def __init__(self):
        pass

    def post_task(self, task):
        pass

    def cancel_task(self, task):
        pass

    @property
    def pending_task_count(self):
        return 0 

    def startup(self):
        pass

    def stop(self):
        pass
