from modelset import ModelSet


class ManagerDescriptor(object):
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance != None:
            raise AttributeError
        return self.manager


class Manager(object):
    def __init__(self, model_class):
        self.model_class = model_class

    def get_model_set(self):
        return ModelSet(self.model_class)

    def get_by_id(self, id):
        if self.model_class.exists(id):
            instance = self.model_class()
            instance.id = str(id)
            return instance
        else:
            return None

    def all(self):
        return self.get_model_set()

    def create(self, **kwargs):
        return self.get_model_set().create(**kwargs)