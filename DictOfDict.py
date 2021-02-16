#!/usr/bin/env python

'''
DictOfDict.py
------------
A dictionary of dictionaries with automatic maintanence to remove empty dictionary values.


'''

from typing import Container, TypeVar, Generic


# class InnerContainer(type):
#     def __new__(metaclass, class_name, bases, attr):
#         if hasattr(bases[0], '__delitem__'):
#             def __delitem__(self, key):
#                 super().__delitem__(key)
#                 if len(self) == 0:
#                     del self._outer_obj[self._outer_key]

#             attr['__delitem__'] = __delitem__

#         if hasattr(bases[0], 'pop'):
#             def pop(self, key):
#                 super().pop(key)
#                 if len(self) == 0:
#                     del self._outer_obj[self._outer_key]

#             attr['pop'] = pop

#         if hasattr(bases[0], 'clear'):
#             def clear(self):
#                 del self._outer_obj[self._outer_key]

#             attr['clear'] = clear

#         return type.__new__(metaclass, class_name, bases, attr)


C = TypeVar('C', bound=Container)


class DictOfContainer(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    class _Container(Generic[C]):
        def __init__(self, cls, outer_obj, outer_key, *args, **kwargs):
            self._outer_obj = outer_obj
            self._outer_key = outer_key
            self.__class__ = cls
            # print(cls)
            # super(cls, self).__init__(*args, **kwargs)

            if hasattr(self, '__delitem__'):
                def __delitem__(self, key):
                    super().__delitem__(key)
                    if len(self) == 0:
                        del self._outer_obj[self._outer_key]

            if hasattr(self, 'pop'):
                def pop(self, key):
                    super().pop(key)
                    if len(self) == 0:
                        del self._outer_obj[self._outer_key]

            if hasattr(self, 'clear'):
                def clear(self):
                    del self._outer_obj[self._outer_key]

    def __setitem__(self, key, item):
        if isinstance(item, dict):
            if len(item) != 0:
                super().__setitem__(key, self._Container(type(item), self, key, item))
        else:
            raise ValueError("Expected type dict, got type {}".format(type(item)))

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __repr__(self):
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


d = DictOfContainer({1: {2: 3}})
print(isinstance(d[1], dict))
