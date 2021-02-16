#!/usr/bin/env python

'''
DictOfDict.py
------------
A dictionary of dictionaries with automatic maintanence to remove empty dictionary values.


'''


class DictOfDict(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    class _Container(dict):
        def __init__(self, outer_obj, outer_key, *args, **kwargs):
            self._outer_obj = outer_obj
            self._outer_key = outer_key
            super().__init__(*args, **kwargs)

        def __delitem__(self, key):
            super().__delitem__(key)
            if len(self) == 0:
                del self._outer_obj[self._outer_key]

        def pop(self, key):
            super().pop(key)
            if len(self) == 0:
                del self._outer_obj[self._outer_key]

        def clear(self):
            del self._outer_obj[self._outer_key]

    def __setitem__(self, key, item):
        if isinstance(item, dict):
            if len(item) != 0:
                super().__setitem__(key, self._Container(self, key, item))
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
