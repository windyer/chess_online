__all__ = ['WarningDef', 
           'ErrorDef',
           'Warning',
           'Error',]

class BaseErrorDef(object):
    
    def __init__(self, index, format):
        self._index = index
        self._format = format
    
    @property
    def format(self):
        return self._format

    @property
    def index(self):
        return self._index

    
class WarningDef(BaseErrorDef):
    pass


class ErrorDef(BaseErrorDef):
    pass


class BaseError(Exception):
    FORMAT = None
    CODE = None

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            self._message = self.FORMAT.format(*args, **kwargs)
        else:
            self._message = self.FORMAT
    
    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, val):
        self._message = val

    def __unicode__(self):
        return self._message

    def __repr__(self):
        return unicode(self)

    def __str__(self):
        return unicode(self)

class Warning(BaseError):

    def __init__(self, *args, **kwargs):
        BaseError.__init__(self, *args, **kwargs)

    def __unicode__(self):
        assert self.CODE is not None
        return u'[Warn|{0}] {1}'.format(self.CODE, self.message)


class Error(BaseError):

    def __init__(self, *args, **kwargs):
        BaseError.__init__(self, *args, **kwargs)

    def __unicode__(self):
        assert self.CODE is not None
        return u'[Error|{0}] {1}'.format(self.CODE, self.message)
