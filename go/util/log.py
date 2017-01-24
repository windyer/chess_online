#coding=utf-8
import functools
from inspect import getcallargs

from django.db import models as django_models
import logging
root_logger = None

def class_wrapper(cls):
    if root_logger is None:
        cls.logger = logging.getLogger(cls.__name__)
    else:
        cls.logger = root_logger.getChild(cls.__name__)
    return cls

def post_image_loger(func):
    @functools.wraps(func)
    def _(self, request, *args, **kwargs):
        if request.method == "GET":
            request_para = request.GET
        else:
            request_para = request.FILES


        self.logger.info(u'[method|%s] [view|%s] [request|%s]',
                          request.method.upper(),
                         self.__class__.__name__, request_para)

        resp = func(self, request, *args, **kwargs)
        #print resp
        data = getattr(resp, 'RecognizeResult', '')
        self.logger.info(u'[method|%s] [view|%s] [response|%s]',
                          request.method.upper(),
                         self.__class__.__name__, len(str(resp)))

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
        return resp
    return _