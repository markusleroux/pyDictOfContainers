#!/usr/bin/env python

'''
DictOfContainer.py
------------
A dictionary of containers with automatic maintanence to remove empty container values.

Note: values are copied into the dictionary.
--------------------------


'''

from collections.abc import Container


class WrapperMetaClass(type):
    cache: dict[str, type] = dict()

    def __call__(self, *args, **kwargs):
        item = args[2]

        if type(item).__name__ not in self.cache:
            def obj_constructor(self, outer_obj, outer_key, item):
                super(type(self), self).__init__(item)
                self._outer_obj = outer_obj
                self._outer_key = outer_key

            _Wrapper = type(type(item).__name__ + 'Wrapper', (type(item),),
                            type(item).__dict__ | {'__init__': obj_constructor})

            for attr in {'__delitem__', 'pop', 'clear'}:
                if hasattr(_Wrapper, attr):
                    setattr(_Wrapper, attr, method_decorator(getattr(_Wrapper, attr)))

            self.cache[type(item).__name__] = _Wrapper
        else:
            _Wrapper = self.cache[type(item).__name__]

        return _Wrapper(*args, **kwargs)


def method_decorator(method):
    def new_method(*args, **kwargs):
        result = method(*args, **kwargs)
        self = args[0]
        if len(self) == 0:
            del self._outer_obj[self._outer_key]
        return result
    return new_method


class DictOfContainer(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    class WrapperFactory(metaclass = WrapperMetaClass):
        ...

    def __setitem__(self, key, item):
        if isinstance(item, Container):
            if len(item) != 0:
                super().__setitem__(key, self.WrapperFactory(self, key, item))
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
