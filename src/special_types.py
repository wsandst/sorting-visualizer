""" Implements a custom Int and List class which keeps track of various usage statistics"""

import random

comparison_cnt = 0
read_cnt = 0
write_cnt = 0

class SInt(int):
    pass

def inc_cmp_cnt(func):
    def inner(*args, **kwargs):
        global comparison_cnt
        comparison_cnt = comparison_cnt + 1
        return func(*args, **kwargs)
    return inner

def setup_custom_int():
    # Loop through the relevant comparisons functions in SInt which are inherited
    # from int and correspond to the comparison operators and
    # decorate them with function inc_cmp_cnt which increments the comparison counter
    for attr in ["__eq__", "__ge__", "__le__", "__gt__", "__lt__", "__ne__"]:
        decorator = inc_cmp_cnt((getattr(SInt, attr)))
        setattr(SInt, attr, decorator)

class SList(list):
    def __init__(self, *args, **kwargs):
        self.read_cnt = 0
        self.write_cnt = 0
        self.last_read_key = 0
        self.last_write_key = 0
        super().__init__(*args, **kwargs)
    
    def __getitem__(self, key):
        self.read_cnt = self.read_cnt + 1
        self.last_read_key = key
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.write_cnt = self.write_cnt + 1
        self.last_write_key = key
        return super().__setitem__(key, value)

    def randomize(self, size, upper_bound, lower_bound=1):
        self.__init__([SInt(random.randrange(lower_bound, upper_bound)) for i in range(size)])

setup_custom_int()
