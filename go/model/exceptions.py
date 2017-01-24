__all__ = ['FieldValidationError', 'MissingID',]

class Error(StandardError):
    pass

class FieldValidationError(Error):

    def __init__(self, errors, *args, **kwargs):
        super(FieldValidationError, self).__init__(*args, **kwargs)
        self._errors = errors

    @property
    def errors(self):
        return self._errors

class MissingID(Error):
    pass

class MissingDB(Error):
    pass

class BadKeyError(Error):
    pass
