__all__ = ['ModuleError']

from base import WarningDef, ErrorDef
from base import Warning, Error

class ModuleErrorBase(type):
    '''
    Metaclass of ModuleError.
    '''
    
    MODULE_ERROR_COUNT = 1000
    module_dict = {}
    error_dict = {}

    def __init__(cls, name, bases, attrs):
        super(ModuleErrorBase, cls).__init__(name, bases, attrs)
        cls._warnings = []
        cls._errors = []

        if cls.__name__ == 'ModuleError':
            return

        assert hasattr(cls.Meta, 'module_index')
        module_index = cls.Meta.module_index
        assert module_index not in ModuleErrorBase.module_dict, cls
        ModuleErrorBase.module_dict[module_index] = name

        cls._initialize_warnings(name, 
                                 module_index, bases, attrs)
        cls._initialize_errors(name, 
                                 module_index, bases, attrs)

    @classmethod
    def get_by_code(cls, code):
        assert code in cls.error_dict
        return cls.error_dict[code]
    
    def _initialize_warnings(cls, name, 
                              module_index, bases, attrs):

        for parent in bases:
            if not isinstance(parent, ModuleErrorBase):
                continue
            for warn in parent._warnings:
                cls._warnings.append(warn) 
            
        for (k, v) in attrs.iteritems():
            if isinstance(v, WarningDef):
                warn_cls_name = k.upper()
                assert k != warn_cls_name
                warn_cls = type(warn_cls_name, (Warning,), {})
                errno = (ModuleErrorBase.MODULE_ERROR_COUNT * 
                            module_index + v.index)
                warn_cls.FORMAT = v.format
                warn_cls.CODE = errno
                setattr(cls, warn_cls_name, warn_cls)
                assert errno not in ModuleErrorBase.error_dict
                ModuleErrorBase.error_dict[errno] = warn_cls
                cls._warnings.append(warn_cls)

    def _initialize_errors(cls, name, 
                            module_index, bases, attrs):
        
        for parent in bases:
            if not isinstance(parent, ModuleErrorBase):
                continue
            for error in parent._errors:
                cls._errors.append(error) 

        for (k, v) in attrs.iteritems():
            if isinstance(v, ErrorDef):
                error_cls_name = k.upper()
                assert k != error_cls_name
                error_cls = type(error_cls_name, (Error,), {})
                errno = (ModuleErrorBase.MODULE_ERROR_COUNT * 
                            module_index + v.index)
                error_cls.FORMAT = v.format
                error_cls.CODE = errno
                setattr(cls, error_cls_name, error_cls)
                assert errno not in ModuleErrorBase.error_dict
                ModuleErrorBase.error_dict[errno] = error_cls
                cls._errors.append(error_cls)

class ModuleError(object):
    __metaclass__ = ModuleErrorBase
    
    @classmethod
    def iter_warnings(cls):
        return iter(cls._warnings)
    
    @classmethod
    def iter_errors(cls):
        return iter(cls._errors)

    class Meta:
        module_index = 0
