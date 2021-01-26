""" 
Implements a custom Int and List class which keeps track of various usage statistics related to sorting
The implementation is quite ugly, but by using these custom classes instead of Pythons own Int
we can completely track and display a sorting algorithm function which written identical to a native
implementation, without messy yields and such.
Every sorting algorithm is on its own thread and can be locked by the user "invisible" cmp function.
"""

import random
import time
import threading

# Dictionaries which hold thread related info, such as locks
# They are indexed by the thread id. These have to be global to allow communication
# Between the Int Cmp function and the rest of the program
cmp_cnt_by_thread = dict()
thread_locks = dict()
cmp_lock_counter = 0
cmp_before_lock = 1

class SInt(int):
    """ Custom Int class. All custom functionality is created through decorators in setup_custom_int """
    pass

def inc_cmp_cnt(func):
    """ Decorator for incrementing the comparison counter and handle thread locking """
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
                # Sleep for a short time to improve multithreaded performance by releasing GIL
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
    """ Custom List function which keeps track of reads and writes """
    def __init__(self, *args, **kwargs):
        self.read_cnt = 0
        self.write_cnt = 0
        self.last_read_key = -1
        self.last_write_key = -1

        if len(args) > 0: 
            # If the list is being initialized by another list, find out the max of the list
            # without counting reads and writes. This saves computation later.
            lst = list(args[0])
            lst = [int(i) for i in lst]
            self.max = max(lst)

        super().__init__(*args, **kwargs)
    
    def __getitem__(self, key):
        self.read_cnt = self.read_cnt + 1
        self.last_read_key = key
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.write_cnt = self.write_cnt + 1
        self.last_write_key = key
        return super().__setitem__(key, value)

    # Helper functions
    def randomize(self, size, upper_bound, lower_bound=1):
        """ Randomize list completely """
        random.seed(783248976)
        self.__init__([SInt(random.randrange(lower_bound, upper_bound+1)) for i in range(size)])

    def shuffle_linear(self, size, lower_bound=1):
        """ Shuffle a linear array """
        random.seed(783248976)
        lst = [lower_bound+i for i in range(size)]
        random.shuffle(lst)
        self.__init__([SInt(i) for i in lst])

setup_custom_int()
