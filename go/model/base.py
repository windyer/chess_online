__all__ = ['Model', 'from_key']

import collections
from datetime import datetime
from dateutil.tz import tzutc

from go.containers.containers import Set, List, Hash
from attributes import *
from key import Key
from managers import ManagerDescriptor, Manager
from exceptions import (FieldValidationError, MissingID, 
                        MissingDB, BadKeyError)


def _initialize_attributes(model_class, name, bases, attrs):
    model_class._attributes = {}

    for parent in bases:
        if not isinstance(parent, ModelBase):
            continue
        for k, v in parent._attributes.iteritems():
            model_class._attributes[k] = v

    for k, v in attrs.iteritems():
        if isinstance(v, Attribute) and not isinstance(v, Counter):
            model_class._attributes[k] = v
            v.name = v.name or k

def _initialize_lists(model_class, name, bases, attrs):
    model_class._lists = {}

    for parent in bases:
        if not isinstance(parent, ModelBase):
            continue
        for k, v in parent._lists.iteritems():
            model_class._lists[k] = v

    for k, v in attrs.iteritems():
        if isinstance(v, ListField):
            model_class._lists[k] = v
            v.name = v.name or k


def _initialize_sets(model_class, name, bases, attrs):
    model_class._sets = {}

    for parent in bases:
        if not isinstance(parent, ModelBase):
            continue
        for k, v in parent._sets.iteritems():
            model_class._sets[k] = v

    for k, v in attrs.iteritems():
        if isinstance(v, SetField):
            model_class._sets[k] = v
            v.name = v.name or k


def _initialize_dicts(model_class, name, bases, attrs):
    model_class._dicts = {}

    for parent in bases:
        if not isinstance(parent, ModelBase):
            continue
        for k, v in parent._dicts.iteritems():
            model_class._dicts[k] = v

    for k, v in attrs.iteritems():
        if isinstance(v, DictField):
            model_class._dicts[k] = v
            v.name = v.name or k

def _initialize_counters(model_class, name, bases, attrs):
    model_class._counters = {}

    for parent in bases:
        if not isinstance(parent, ModelBase):
            continue
        for k, v in parent._counters.iteritems():
            model_class._counters[k] = v

    for k, v in attrs.iteritems():
        if isinstance(v, Counter):
            model_class._counters[k] = v
            v.name = v.name or k

def _initialize_key(model_class, name):
    model_class._key = Key(model_class._meta['key'] or name)

def _initialize_manager(model_class):
    model_class.objects = ManagerDescriptor(Manager(model_class))

def _initialize_auto_increment(model_class):
    if hasattr(model_class._meta.meta, 'auto_increment'):
        model_class.auto_increment = model_class._meta['auto_increment']
    else:
        model_class.auto_increment = True 

class ModelOptions(object):

    def __init__(self, meta):
        self.meta = meta

    def get_field(self, field_name):
        if self.meta is None:
            return None
        try:
            return self.meta.__dict__[field_name]
        except KeyError:
            return None
    __getitem__ = get_field


class ModelBase(type):

    def __init__(cls, name, bases, attrs):
        super(ModelBase, cls).__init__(name, bases, attrs)
        cls._meta = ModelOptions(attrs.pop('Meta', None))
        _initialize_attributes(cls, name, bases, attrs)
        _initialize_lists(cls, name, bases, attrs)
        _initialize_sets(cls, name, bases, attrs)
        _initialize_dicts(cls, name, bases, attrs)
        _initialize_counters(cls, name, bases, attrs)
        _initialize_key(cls, name)
        _initialize_manager(cls)
        _initialize_auto_increment(cls)


class Model(object):
    __metaclass__ = ModelBase

    def __init__(self, **kwargs):
        self._modified_fields = dict()
        self._enable_track = False
        self.update_attributes(**kwargs)

    def is_valid(self):
        self._errors = []
        for field in self.attributes().values():
            try:
                field.validate(self)
            except FieldValidationError as e:
                self._errors.extend(e.errors)
        self.validate_id()
        self.validate()
        return not bool(self._errors)

    def validate(self):
        pass

    def validate_id(self):
        if self.db is not None and not self.auto_increment and self.is_new():
            self._errors.append(('id', 'model id should be specified'))

    def begin_track(self):
        self._enable_track = True

    def track_enabled(self):
        return self._enable_track

    def track_attribute(self, attr):
        if self._enable_track:
            self._modified_fields[attr.name] = attr

    @property
    def modified_fields(self):
        return dict(self._modified_fields)

    def end_track(self):
        self._enable_track = False
        self._modified_fields.clear()

    def update_attributes(self, **kwargs):
        for k in self.counters():
            if k in kwargs:
                raise AttributeError("can't set a counter. please incr or decr. thanks")

        for k, v in self.attributes().items():
            if k in kwargs:
                v.__set__(self, kwargs[k])

        for k, v in self.lists().items():
            if k in kwargs:
                val = v.__get__(self, None)
                assert isinstance(kwargs[k], (list,tuple))
                del val[:]
                val.extend(kwargs[k])

        for k, v in self.sets().items():
            if k in kwargs:
                val = v.__get__(self, None)
                assert isinstance(kwargs[k], (set, list, tuple))
                val.clear()
                val.update(kwargs[k])

        for k, v in self.dicts().items():
            if k in kwargs:
                val = v.__get__(self, None)
                assert isinstance(kwargs[k], (dict, collections.defaultdict))
                val.clear()
                val.update(kwargs[k])

    @classmethod
    def fields(cls):
        d = dict()
        d.update(cls._attributes)
        d.update(cls._lists)
        d.update(cls._sets)
        d.update(cls._dicts)
        d.update(cls._counters)
        return d

    @classmethod
    def attributes(cls):
        return dict(cls._attributes)

    @classmethod
    def lists(cls):
        return dict(cls._lists)

    @classmethod
    def sets(cls):
        return dict(cls._sets)

    @classmethod
    def dicts(cls):
        return dict(cls._dicts)

    @classmethod
    def counters(cls):
        return dict(cls._counters)

    @classmethod
    def exists(cls, id):
        db = cls._meta['db']
        if db is None:
            raise MissingDB()

        return bool(db.exists(cls._key[str(id)]) or
                    db.sismember(cls._key['all'], str(id)))

    @property
    def counters_value(self):
        h = {}
        if self.db is not None and not self.is_new():
            attrs_hash = Hash(self.key()['Model_Counter'], db=self.db)
            stored_counters = attrs_hash.hgetall()
            for k, v in self.counters().iteritems():
                if v.attrname in stored_counters:
                    h[k] = v.typecast_for_read(stored_counters[v.attrname])
        else:
            for k in self.counters():
                h[k] = getattr(self, k)

        return h

    @property
    def fields_value(self):
        h = {}
        for k in self.attributes():
            h[k] = getattr(self, k)

        for k in self.lists():
            h[k] = getattr(self, k)

        for k in self.sets():
            h[k] = getattr(self, k).copy()

        for k in self.dicts():
            h[k] = getattr(self, k).copy()

        h.update(self.counters_value)

        return h

    @property
    def db(self):
        return None if not self._meta['db'] else self._meta['db']

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            self.is_valid()
        return self._errors

    def is_new(self):
        return not hasattr(self, '_id')

    def incr(self, att, val=1, pipeline=None):
        assert self.db is not None
        assert not self.is_new()

        if att not in self.counters():
            raise ValueError("%s is not a counter.")
        if pipeline is None:
            counter_hash = Hash(self.key()['Model_Counter'], self.db)
        else:
            counter_hash = Hash(self.key()['Model_Counter'], pipeline)

        counter_hash.hincrby(self.counters()[att].attrname, val)

    def decr(self, att, val=1, pipeline=None):
        assert self.db is not None
        assert not self.is_new()
        self.incr(att, -1 * val, pipeline)

    @property
    def attributes_dict(self):
        h = self.fields_value
        if 'id' not in self.attributes() and not self.is_new():
            h['id'] = self.id
        return h

    def set_id(self, val):
        self._id = str(val)

    @property
    def id(self):
        if not hasattr(self, '_id'):
            raise MissingID
        return self._id

    @id.setter
    def id(self, val):
        if self.db is None:
            raise MissingDB()

        #pipeline = self.db.pipeline()
        self._id = str(val)

        attrs_hash = Hash(self.key(), db=self.db)
        stored_attrs = attrs_hash.hgetall()
        attrs = self.attributes().values()
        for att in attrs:
            if att.attrname in stored_attrs and not isinstance(att, Counter):
                att.__set__(self, att.typecast_for_read(stored_attrs[att.attrname]))

        for att in self.dicts().values():
            d = Hash(self.key()[att.attrname], db=self.db)
            stored_dict = d.hgetall()
            att_dict = att.__get__(self, None)
            for k, v in stored_dict.iteritems():
                att_dict[att.key_type(k)] = att.value_type(v)

        for att in self.lists().values():
            l = List(self.key()[att.attrname], db=self.db)
            stored_list = l.members
            att_list = att.__get__(self, None)
            for value in stored_list:
                att_list.append(att.value_type(value))

        for att in self.sets().values():
            s = Set(self.key()[att.attrname], db=self.db)
            stored_set = s.members
            att_set = att.__get__(self, None)
            for item in stored_set:
                att_set.add(att.value_type(item))

        #pipeline.execute()

    def save(self):
        if self.db is None:
            raise MissingDB()

        if not self.is_valid():
            return self._errors
        _new = self.is_new()
        if _new:
            self._initialize_id()
        self._write(_new)
        return True

    def key(self, att=None):
        if att is not None:
            return self._key[self.id][att]
        else:
            return self._key[self.id]

    def delete(self):
        if self.db is None:
            raise MissingDB()

        pipeline = self.db.pipeline()
        self._delete_membership(pipeline)
        pipeline.delete(self.key())

        non_attrs = self.lists().values() + self.sets().values() + \
                    self.dicts().values() + self.counters().values()
        for att in non_attrs:
            pipeline.delete(self.key()[att.attrname])

        pipeline.execute()

    def _initialize_id(self):
        assert self.db is not None
        self._id = str(self.db.incr(self._key['id']))

    def _write(self, _new=False):
        pipeline = self.db.pipeline()
        self._create_membership(pipeline)

        h = {}
        # attributes
        for att in self.attributes().values():
            if isinstance(att, DateTimeField):
                if att.auto_now:
                    att.__set__(self, datetime.now(tz=tzutc()))
                if att.auto_now_add and _new:
                    att.__set__(self, datetime.now(tz=tzutc()))
            elif isinstance(att, DateField):
                if att.auto_now:
                    att.__set__(self, datetime.now(tz=tzutc()))
                if att.auto_now_add and _new:
                    att.__set__(self, datetime.now(tz=tzutc()))
            for_storage = att.__get__(self, None)
            if for_storage is not None:
                h[att.attrname] = att.typecast_for_storage(for_storage)

        pipeline.delete(self.key())
        if h:
            pipeline.hmset(self.key(), h)

        # lists
        for att in self.lists().values():
            l = List(self.key()[att.attrname], pipeline=pipeline)
            l.clear()
            values = att.__get__(self, None)
            if values:
                l.extend(values)

        # sets
        for att in self.sets().values():
            s = Set(self.key()[att.attrname], pipeline=pipeline)
            s.clear()
            values = att.__get__(self, None)
            if values:
                s.add(list(values))

        # dicts
        for att in self.dicts().values():
            d = Hash(self.key()[att.attrname], pipeline=pipeline)
            d.clear()
            values = att.__get__(self, None)
            if values:
                d.hmset(values)

        pipeline.execute()

    ##############
    # Membership #
    ##############

    def _create_membership(self, pipeline=None):
        Set(self._key['all'], pipeline=pipeline).add(self.id)

    def _delete_membership(self, pipeline=None):
        Set(self._key['all'], pipeline=pipeline).remove(self.id)

    ##################
    # Python methods #
    ##################

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        if not self.is_new():
            return "<%s %s>" % (self.key(), self.attributes_dict)
        return "<%s %s>" % (self.__class__.__name__, self.attributes_dict)


def get_model_from_key(key):
    """Gets the model from a given key."""
    _known_models = {}
    model_name = key.split(':', 2)[0]
    # populate
    for klass in Model.__subclasses__():
        _known_models[klass.__name__] = klass
    return _known_models.get(model_name, None)


def from_key(key):
    """Returns the model instance based on the key.

    BadKeyError if the key is not recognized by
    go or no defined model can be found.
    Returns None if the key could not be found.
    """
    model = get_model_from_key(key)
    if model is None:
        raise BadKeyError
    try:
        _, id = key.split(':', 2)
        id = int(id)
    except (ValueError, TypeError):
        raise BadKeyError
    return model.objects.get_by_id(id)
