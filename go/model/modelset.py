"""
Handles the queries.
"""
from go.containers.containers import SortedSet, Set 

# Model Set
class ModelSet(Set):
    def __init__(self, model_class):
        self.model_class = model_class
        self.key = model_class._key['all']
        self._db = model_class._meta['db']

    def __getitem__(self, index):
        if isinstance(index, slice):
            return map(lambda id: self._get_item_with_id(id), self._set[index])
        else:
            id = self._set[index]
            if id:
                return self._get_item_with_id(id)
            else:
                raise IndexError

    def __repr__(self):
        if len(self._set) > 30:
            m = self._set[:30]
        else:
            m = self._set
        s = map(lambda id: self._get_item_with_id(id), m)
        return "%s" % s

    def __iter__(self):
        for id in self._set:
            yield self._get_item_with_id(id)

    def __len__(self):
        return len(self._set)

    def __contains__(self, val):
        return val.id in self._set

    def get_by_id(self, id):
        if str(id) not in self._set:
            return
        if self.model_class.exists(id):
            return self._get_item_with_id(id)

    def create(self, **kwargs):
        instance = self.model_class(**kwargs)
        if instance.save():
            return instance
        else:
            return None

    @property
    def db(self):
        return self._db

    @property
    def _set(self):
        s = Set(self.key, db=self.db)
        return list(s.members)

    def _get_item_with_id(self, id):
        instance = self.model_class()
        instance.id = str(id)
        return instance