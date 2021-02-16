#!/usr/bin/env python

'''
DictOfContainer.py
------------
A dictionary of dictionaries with automatic maintanence to remove empty dictionary values.

Done: Clearly need a better solution to overriding methods in wrapper
        - Really what I need is a hook that wraps all the relevant methods in a check that the length is not 0
        - Maybe a decorator? Probably a decorator...
TODO: Why did the override not work in init body? Tried types.MethodType
TODO: What are the relevant methods that I haven't considered?
TODO: Should cache the _container_factory
DONE: pop should inherit its default from super().pop (would be solved using decorator)
TODO: cast back to base class of _Container when unlinked from dict
TODO: figure out set printing with its type

Decorators can be used to defer work to instantiation time
'''
from collections.abc import Container


def method_decorator(method):
    def new_method(*args, **kwargs):
        result = method(*args, **kwargs)
        self = args[0]
        if len(self) == 0:
            del self._outer_obj[self._outer_key]
        return result
    return new_method


def class_decorator(cls):
    for attr in {'__delitem__', 'pop', 'clear'}:
        if hasattr(cls, attr):
            setattr(cls, attr, method_decorator(getattr(cls, attr)))
    return cls


class DictOfContainer(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    @staticmethod
    def _container_factory(outer_obj, outer_key, item):
        @class_decorator
        class _Container(type(item)):
            def __init__(self, outer_obj, outer_key, item):
                super().__init__(item)
                self._outer_obj = outer_obj
                self._outer_key = outer_key

        return _Container(outer_obj, outer_key, item)

    def __setitem__(self, key, item):
        if isinstance(item, Container):
            if len(item) != 0:
                super().__setitem__(key, self._container_factory(self, key, item))
        else:
            raise ValueError("Expected container type, got type {}".format(type(item)))

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __repr__(self):
        if len(self) == 0:
            return '{}'
        return '{\n' + '\n'.join('{}: {}'.format(key, container) for key, container in self.items()) + '\n}'

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("Expected at most one argument, got {}".format(len(args)))

            other = dict(args[0])
            for key in other:
                if len(other[key]) != 0:
                    self[key] = other[key]

        for key in kwargs:
            if len(other[key]) != 0:
                self[key] = kwargs[key]


d = DictOfContainer({1: {2: 3}, 4: [5, 6], 7: {8, 9}})

# d[1].clear()
# del d[1][2]
d[4].pop()
d[4].pop()
print(d)
print(str(d[7]))
