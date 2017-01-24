import functools
from rest_framework import serializers
from django.conf import settings

def args_limit(*limitted_keys):
    def _para_limit(func):
        @functools.wraps(func)
        def _(self, *args, **kwargs):
            for key in kwargs.keys():
                assert key in limitted_keys, "args is more than required"
            resp = func(self, *args, **kwargs)
            return resp
        return _
    return _para_limit


def args_required(*required_keys):
    def _para_required(func):
        @functools.wraps(func)
        def _(self, *args, **kwargs):
            args_keys = kwargs.keys()
            for key in required_keys:
                assert key in args_keys, "args is less than required"
            resp = func(self, *args, **kwargs)
            return resp
        return _
    return _para_required

def request_limit(serializer_class):
    def _request_limit(func):
        @functools.wraps(func)
        def _(self, request, format=None):
            if issubclass(serializer_class, serializers.ModelSerializer):
                limitted_keys = list(serializer_class.Meta.fields)
            elif issubclass(serializer_class, serializers.Serializer):
                limitted_keys = serializer_class.base_fields.keys()

            if settings.DEBUG:
                limitted_keys.append('csrfmiddlewaretoken')
            for key in request.DATA:
                if key not in limitted_keys:
                    raise serializers.ValidationError(
                        "your request para is more than required")
            return func(self, request, format)
        return _
    return _request_limit


if __name__ == '__main__':
    class test(object):
        @args_required('gender',)
        def testfun(self, name, age, **others):
            print name, age, others

    t = test()
    t.testfun('jack', age=28, **{'gender':'male'})
    t.testfun(name='jack', age=28, **{'gender':'male'})
    class test(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    from operator import attrgetter
    lis = [test(1,2),test(3,4), test(3,1), test(5,1),test(5,4),test(5,3),test(4,5)]
    lis.sort(key=attrgetter('a', 'b'), reverse=True)

    for item in lis:
        print item.a, item.b

    from inspect import getcallargs, getmembers
    import inspect
    def trace_service(func):
        @functools.wraps(func)
        def _(self, *args, **kwargs):
            class_name = self.__class__.__name__
            method = func.func_name
            call_args = getcallargs(func, self, *args, **kwargs)
            del call_args['self']

            resp = func(self, *args, **kwargs)


            return resp
        return _


    class Aaaaa(object):
        @trace_service
        def test(self,a, b, c, *_,**__):   
            print "heloo"

    aaa = Aaaaa()
    aaa.test(1,2,3,4,5,6)
    aaa.test(a=1,b=2,c=3)
    print '55'*20

    dic = [1,2.3,4,5,8]
    tt = getmembers(dic)
    print str(dic)
    print tt
    print inspect.isframe(Aaaaa)
    #print aaa