""" Implements a custom Int and List class which keeps track of various usage statistics"""

import random
import time
import threading

cmp_cnt_by_thread = dict()
thread_locks = dict()
cmp_lock_counter = 0
cmp_before_lock = 10

class SInt(int):
    pass

def inc_cmp_cnt(func):
    def inner(*args, **kwargs):
        global cmp_cnt_by_thread
        global thread_locks
        global cmp_lock_counter

        cmp_cnt_by_thread.setdefault(threading.get_ident(), 0)
        cmp_cnt_by_thread[threading.get_ident()] += 1
        
        # Handle thread locking if exceeding comparisons
        cmp_lock_counter = cmp_lock_counter + 1
        if cmp_lock_counter >= cmp_before_lock:
            cmp_lock_counter = 0
            thread_locks[threading.get_ident()] = True
            # Wait until main thread unlocks this thread
            while thread_locks[threading.get_ident()]:        
                time.sleep(0.000001)

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
        random.seed(783248976)
        self.__init__([SInt(random.randrange(lower_bound, upper_bound+1)) for i in range(size)])

setup_custom_int()
