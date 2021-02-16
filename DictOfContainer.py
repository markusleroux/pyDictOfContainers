#!/usr/bin/env python

'''
DictOfContainer.py
------------
A dictionary of dictionaries with automatic maintanence to remove empty dictionary values.

TODO:
    - Clearly need a better solution to overriding methods in wrapper
        - Why is the override not working? Tried with types.MethodType
        - Really what I need is a hook that wraps all the relevant methods in a check that the length is not 0
        - Maybe a decorator? Probably a decorator...
    - What are the relevant methods that I haven't considered?
    - Should cache the _container_factory
'''
from collections.abc import Container

class DictOfContainer(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    @staticmethod
    def _container_factory(outer_obj, outer_key, item):
        class _Container(type(item)):
            def __init__(self, outer_obj, outer_key, item):
                super().__init__(item)
                self._outer_obj = outer_obj
                self._outer_key = outer_key
                self.flags = (hasattr(item, '__delitem__'), hasattr(item, 'pop'), hasattr(item, 'clear'))

                # if hasattr(self, '__delitem__'):
                #     def __delitem__(self, key):
                #         super().__delitem__(key)
                #         if len(self) == 0:
                #             del self._outer_obj[self._outer_key]
                #     self.__delitem__ = __delitem__

                # if hasattr(self, 'pop'):
                #     def pop(self, key):
                #         super().pop(key)
                #         if len(self) == 0:
                #             del self._outer_obj[self._outer_key]
                #     self.pop = pop

                # if hasattr(self, 'clear'):
                #     def clear(self):
                #         print('ehij')
                #         del self._outer_obj[self._outer_key]
                #     self.clear = clear

            def __delitem__(self, key):
                if self.flags[0]:
                    super().__delitem__(key)
                    if len(self) == 0:
                        del self._outer_obj[self._outer_key]

            def pop(self, key):
                if self.flags[1]:
                    super().pop(key)
                    if len(self) == 0:
                        del self._outer_obj[self._outer_key]

            def clear(self):
                if self.flags[3]:
                    del self._outer_obj[self._outer_key]

        return _Container(outer_obj, outer_key, item)

    def __setitem__(self, key, item):
        if isinstance(item, Container):
            if len(item) != 0:
                # super().__setitem__(key, self._Container(self, key, item))
                super().__setitem__(key, self._container_factory(self, key, item))
        else:
            raise ValueError("Expected type dict, got type {}".format(type(item)))

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __repr__(self):
        if len(self) == 0:
            return '{}'
        return '{\n' + '\n'.join('{}: {}'.format(key, subdict) for key, subdict in self.items()) + '\n}'

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


d = DictOfContainer({1: {2: 3}, 4: [5, 6]})

# d[1].clear()
# del d[1][2]
d[4].pop(-1)
d[4].pop(-1)
print(d)
