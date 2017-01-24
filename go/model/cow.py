__all__  = ['COWDict', 'COWSet']

import copy

class COWDict(object):

    def __init__(self, d, on_modified=None):
        self._dict = d
        self._on_modified = on_modified

    def __setitem__(self, k, v):
        self._on_write()
        self._dict[k] = v

    def __getitem__(self, k):
        return self._dict.__getitem__(k)

    def __delitem__(self, k):
        return self._dict.__delitem__(k)

    def __contains__(self, k):
        return self._dict.__contains__(k)

    def __len__(self):
        return len(self._dict)

    def _on_write(self):
        self._dict = copy.deepcopy(self._dict)

        if self._on_modified is not None:
            self._on_modified()

    def __repr__(self):
        return repr(self._dict)

    def copy(self):
        return COWDict(self._dict)

    def __getattr__(self, attr):
        return getattr(self._dict, attr)

class COWSet(object):

    def __init__(self, s, on_modified=None):
        self._set = s
        self._on_modified = on_modified

    def add(self, e):
        self._on_write()
        self._set.add(e)

    def remove(self, e):
        self._on_write()
        self._set.remove(e)

    def clear(self):
        self._on_write()
        self._set.clear()
    
    def __eq__(self, s):
        return self._set.__eq__(s)

    def __contains__(self, k):
        return self._set.__contains__(k)

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return self._set.__iter__()
    
    def _on_write(self):
        self._set = copy.deepcopy(self._set)
        if self._on_modified is not None:
            self._on_modified()

    def __repr__(self):
        return repr(self._set)

    def copy(self):
        return COWSet(self._set)

    def __getattr__(self, attr):
        return getattr(self._set, attr)