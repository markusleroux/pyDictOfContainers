#!/usr/bin/env python

class ContainerDict(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    class _Container(dict):
        def __init__(self, outer_obj, outer_key, *args, **kwargs):
            self._outer_obj = outer_obj
            self._outer_key = outer_key
            super().__init__(*args, **kwargs)

        def __delitem__(self, key):
            super().__delitem__(key)
            if len(self._outer_obj[self._outer_key]) == 0:
                del self._outer_obj[self._outer_key]

    def __setitem__(self, key, item):
        if isinstance(item, dict):
            super().__setitem__(key, self._Container(self, key, item))
        else:
            raise ValueError("Expected type dict, got type {}".format(type(item)))

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __repr__(self):
        return '{\n' + '\n'.join('{}: {}'.format(key, subdict) for key, subdict in self.items()) + '\n}'

    # def __len__(self):
        # pass

    # def __delitem__(self):
        # pass

    # def __clear__(self):
        # pass

    # def copy(self):
        # pass

    # def has_key(self, key):
        # pass

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("Expected at most one argument, got {}".format(len(args)))

            other = dict(args[0])
            for key in other:
                self[key] = other[key]

        for key in kwargs:
            self[key] = kwargs[key]

    # def keys(self):
        # pass

    # def values(self):
        # pass

    # def items(self):
        # pass

    # def pop(self, *args):
        # pass

    # def __contains__(self, item):
        # pass

    # def __iter__(self):
        # pass

    # def __unicode__(self):
        # pass

