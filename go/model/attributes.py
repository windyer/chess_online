__all__ = ['Attribute', 'CharField', 
           'IntegerField', 'FloatField', 'BooleanField', 
           'DateTimeField', 'DateField', 'CustomField',
           'ListField', 'SetField', 'DictField', 'Counter']

from dateutil.tz import tzutc, tzlocal
from datetime import datetime, date
from collections import defaultdict

from exceptions import FieldValidationError
from cow import COWDict, COWSet


class Attribute(object):
    
    def __init__(self, name=None, required=False, validator=None, default=None):
        self.name = name
        self.required = required
        self.validator = validator
        self.default = default

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.attrname)
        except AttributeError:
            setattr(instance, self.attrname, self.default)
            return self.default

    def __set__(self, instance, value):
        origin_value = getattr(instance, self.attrname, None)
        if origin_value != value:
            setattr(instance, self.attrname, value)
            instance.track_attribute(self)

    @property
    def attrname(self):
        return '_' + self.name

    def validate(self, instance):
        val = getattr(instance, self.attrname, None)

        errors = []
        if val is not None and not isinstance(val, self.acceptable_types()):
            errors.append((self.name, 'bad type',))

        if self.required:
            if val is None or not unicode(val).strip():
                errors.append((self.name, 'required'))

        if self.validator:
            r = self.validator(self.name, val)
            if r:
                errors.extend(r)

        if errors:
            raise FieldValidationError(errors)

    def value_type(self):
        return unicode

    def acceptable_types(self):
        return basestring

    def typecast_for_read(self, value):
        """Typecasts the value for reading from database."""
        if value is not None:
            try:
                return unicode(value)
            except UnicodeError:
                return value.decode('utf-8')

    def typecast_for_storage(self, value):
        """Typecasts the value for storing to database."""
        try:
            return unicode(value)
        except UnicodeError:
            return value.decode('utf-8')

class CharField(Attribute):

    def __init__(self, max_length=255, **kwargs):
        super(CharField, self).__init__(**kwargs)
        self.max_length = max_length

    def validate(self, instance):
        errors = []
        try:
            super(CharField, self).validate(instance)
        except FieldValidationError as err:
            errors.extend(err.errors)

        val = getattr(instance, self.attrname, None)
        if val is None and not errors:
            return
        elif val is None and errors:
            raise FieldValidationError(errors)

        if val and len(val) > self.max_length:
            errors.append((self.name, 'exceeds max length'))

        if errors:
            raise FieldValidationError(errors)

    def value_type(self):
        return basestring

    def acceptable_types(self):
        return self.value_type()


class IntegerField(Attribute):
    
    def value_type(self):
        return int

    def acceptable_types(self):
        return (int, long)

    def typecast_for_read(self, value):
        if value is not None:
            return int(value)

    def typecast_for_storage(self, value):
        if value is None:
            return 0
        return value         


class FloatField(Attribute):

    def value_type(self):
        return float

    def acceptable_types(self):
        return self.value_type()

    def typecast_for_read(self, value):
        if value is not None:
            return float(value)
        else:
            return 0

    def typecast_for_storage(self, value):
        if value is None:
            return 0
        return value         


class BooleanField(Attribute):

    def value_type(self):
        return bool

    def acceptable_types(self):
        return self.value_type()

    def typecast_for_read(self, value):
        if value is not None:
            return bool(int(value))
        else:
            return False

    def typecast_for_storage(self, value):
        if value is None:
            return 0
        return 1 if value else 0

class DateField(Attribute):

    def __init__(self, auto_now=False, auto_now_add=False, **kwargs):
        super(DateField, self).__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def value_type(self):
        return date

    def acceptable_types(self):
        return self.value_type()

    def typecast_for_read(self, value):
        try:
            if isinstance(value, date):
                return value
            elif isinstance(value, basestring):
                date_time = datetime.strptime(value, '%Y-%m-%d')
                return date_time.date()
            else:
                return date.fromtimestamp(float(value))
        except (TypeError, ValueError):
            return None

    def typecast_for_storage(self, value):
        if not isinstance(value, date):
            raise TypeError("%s should be date object, and not a %s" %
                    (self.attrname, type(value)))
        if value is None:
            return None
        return date.strftime(value, '%Y-%m-%d')
     

class DateTimeField(Attribute):

    def __init__(self, auto_now=False, auto_now_add=False, **kwargs):
        super(DateTimeField, self).__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def value_type(self):
        return datetime

    def acceptable_types(self):
        return self.value_type()

    def typecast_for_read(self, value):
        try:
            if isinstance(value, datetime):
                return value
            elif isinstance(value, basestring):
                date_time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                return date_time.replace(tzinfo=tzutc())
            else:
                return datetime.fromtimestamp(float(value), tzutc())
        except (TypeError, ValueError):
            return None

    def typecast_for_storage(self, value):
        if not isinstance(value, datetime):
            raise TypeError("%s should be datetime object, and not a %s" %
                    (self.name, type(value)))
        if value is None:
            return None

        if value.tzinfo is None:
           value = value.replace(tzinfo=tzlocal())
        value = value.astimezone(tzutc())
        return datetime.strftime(value, '%Y-%m-%d %H:%M:%S')


class CustomField(Attribute):

    def __init__(self, **kwargs):
        super(CustomField, self).__init__(**kwargs)

    def value_type(self):
        return object

    def acceptable_types(self):
        return self.value_type()


class ListField(object):

    def __init__(self, value_type, name=None, validator=None, default=None):
        self.name = name
        self.validator = validator
        self.default = default
        self.value_type = value_type

    def __set__(self, instance, value):
        raise AttributeError('could not set a list field')

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.attrname)
        except AttributeError:
            if self.default is not None:
                l = map(self.value_type, self.default)
            else:
                l = list()
            setattr(instance, self.attrname, l)
            return l

    def __delete__(self, instance):
        delattr(instance, self.attrname)

    @property
    def attrname(self):
        return '_' + self.name


class SetField(object):

    def __init__(self, value_type, name=None, validator=None, default=None):
        self.name = name
        self.validator = validator
        self.default = default
        self.value_type = value_type

    def __set__(self, instance, value):
        raise AttributeError('could not set a set field')

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.attrname)
        except AttributeError:
            def on_modified():
                instance.track_attribute(self)
            if self.default is not None:
                d = COWSet(set(map(self.value_type, self.default)), on_modified)
            else:
                d = COWSet(set(), on_modified)
            setattr(instance, self.attrname, d)
            return d

    def __delete__(self, instance):
        delattr(instance, self.attrname)

    @property
    def attrname(self):
        return '_' + self.name


class DictField(object):

    def __init__(self, key_type, value_type, name=None, validator=None, default=None):
        self.name = name
        self.validator = validator
        self.default = default
        self.key_type = key_type
        self.value_type = value_type

    def __set__(self, instance, value):
        raise AttributeError('could not set a dict field')

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.attrname)
        except AttributeError:
            def on_modified():
                instance.track_attribute(self)
            if self.default is not None:
                df = defaultdict(self.value_type)
                for k,v in self.default.iteritems():
                    df[self.key_type(k)] = self.value_type(v)
                d = COWDict(df, on_modified)
            else:
                d = COWDict(defaultdict(self.value_type), on_modified)
            setattr(instance, self.attrname, d)
            return d

    def __delete__(self, instance):
        delattr(instance, self.attrname)

    @property
    def attrname(self):
        return '_' + self.name


class Counter(IntegerField):

    def __init__(self, **kwargs):
        super(Counter, self).__init__(**kwargs)
        if not kwargs.has_key('default') or self.default is None:
            self.default = 0

    def __set__(self, instance, value):
        raise AttributeError("can't set a counter.")

    def __get__(self, instance, owner):

        attribute_name = self.attrname

        class CounterInteger(long):
            
            def incr(self, val=1):
                assert isinstance(val, (int, long))
                if instance.db is not None:
                    instance.db.hincrby(instance.key()['Model_Counter'], attribute_name, val)
                else:
                    pre_val = getattr(instance, attribute_name)
                    setattr(instance, attribute_name, pre_val + val)

            def decr(self, val=1):
                assert isinstance(val, (int, long)) and val > 0
                self.incr(-1 * val)

        if instance.db is None:
            try:
                val = getattr(instance, self.attrname)
                return CounterInteger(val)
            except AttributeError:
                setattr(instance, self.attrname, self.typecast_for_read(self.default))
                return CounterInteger(self.default)
        else:
            v = instance.db.hget(instance.key()['Model_Counter'], self.attrname)
            v = 0 if v is None else v
            return CounterInteger(v)
