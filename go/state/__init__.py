__all__ = ['State', 'state_machine', 'action']

import inspect
import functools

class State(object):

    @staticmethod
    def enter_state(state_machine):
        pass

    @staticmethod
    def exit_state(state_machine):
        pass

def state_machine(cls):
    initial_states = []
    for i in cls.__dict__.itervalues():
        if inspect.isclass(i) and issubclass(i, State) and \
                hasattr(i, 'initial_state') and i.initial_state:
            initial_states.append(i)

    if not initial_states:
        raise Exception('{0}\'s initial state is not found.'\
                        .format(cls.__name__))
    if len(initial_states) > 1:
        raise Exception('%s has too much default state: {1}'\
                    .format(cls.__name__, initial_states))

    initial_state = initial_states[0]

    old__init__ = cls.__init__
    if hasattr(cls, '__getattr__'):
        old__getattr__ = getattr(cls, '__getattr__')
    else:
        old__getattr__ = getattr(cls, '__getattribute__')

    def __init__(self, *args, **kwargs):
        self.__state__ = initial_state
        self.__state__.enter_state(self)
        return old__init__(self, *args, **kwargs)

    def switch(self, new_state):
        self.__state__.exit_state(self)
        self.__state__ = new_state
        new_state.enter_state(self)

    @property
    def cur_state(self):
        assert hasattr(self, '__state__')
        return self.__state__

    def __getattr__(self, name):
        try:
            val = old__getattr__(self, name)
        except AttributeError, e:
            pass
        else:
            return val 
        
        try:
            f = getattr(self.__state__, name)
        except AttributeError, e:
            raise e

        if not callable(f):
            raise e
        
        return functools.partial(f, self)

    cls.__init__ = __init__
    cls.__getattr__ = __getattr__
    cls.cur_state = cur_state
    cls.switch = switch
    return cls

action = staticmethod
