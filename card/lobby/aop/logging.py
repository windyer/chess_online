import functools
from inspect import getcallargs

from django.db import models as django_models
from go import model as go_model

def trace_view(func):
    @functools.wraps(func)
    def _(self, request, *args, **kwargs):
        if request.method == "GET":
            request_para = request.QUERY_PARAMS
        else:
            request_para = request.DATA
            
        user_id = (getattr(request.user, 'id', None)
                   or getattr(request.user, 'user_id', None))

        self.logger.info(u'[user|%s] [method|%s] [view|%s] [request|%s]',
                         user_id, request.method.upper(),
                         self.__class__.__name__, request_para)

        resp = func(self, request, *args, **kwargs)

        data = getattr(resp, 'data', '')
        self.logger.info(u'[user|%s] [method|%s] [view|%s] [response|%s]',
                         user_id, request.method.upper(),
                         self.__class__.__name__, data)
        return resp
    return _

def trace_service(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        class_name = self.__class__.__name__
        method = func.func_name
        call_args = getcallargs(func, self, *args, **kwargs)
        del call_args['self']

        self.logger.debug(u'enter [class|%s] [method|%s] with [args|%s]',
                    class_name, method, call_args)

        try:
            resp = func(self, *args, **kwargs)
        except BaseException as ex:
            self.logger.error(u'leave [class|%s] [method|%s] with [exception|%s]', 
                class_name, method, ex)
            raise
        
        if isinstance(resp, dict) or isinstance(resp, list):
            self.logger.debug(u'leave [class|%s] [method|%s] with [response|%s]',
                                class_name, method, resp)
        elif isinstance(resp, django_models.Model):
            model_name = resp.__class__.__name__
            self.logger.debug(u'leave [class|%s] [method|%s] with django [model|%s] [response|%s]',
                    class_name, method, model_name , resp.__dict__)
        elif isinstance(resp, go_model.Model):
            model_name = resp.__class__.__name__
            self.logger.debug(u'leave [class|%s] [method|%s] with redis [model|%s] [response|%s]',
                    class_name, method, model_name, resp.__str__())

        return resp
    return _