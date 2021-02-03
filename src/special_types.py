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



# Avoiding globals
class ThreadManagment:
    thread_locks = dict()
    cmp_lock_counter = 0
    read_lock_counter = 0
    write_lock_counter = 0
    lock_type = 2
    cmp_before_lock = 1
    # Sorting information by thread
    sort_data_by_thread = dict()

def sleep_if_needed():
    lock = False
    if ThreadManagment.lock_type == 0: # Lock by cmps
        if ThreadManagment.cmp_lock_counter >= ThreadManagment.cmp_before_lock:
            ThreadManagment.cmp_lock_counter = 0
            lock = True
    elif ThreadManagment.lock_type == 1: # Lock by reads
        if ThreadManagment.read_lock_counter >= ThreadManagment.cmp_before_lock:
            ThreadManagment.read_lock_counter = 0
            lock = True
    elif ThreadManagment.lock_type == 2: # Lock by writes
        if ThreadManagment.write_lock_counter >= ThreadManagment.cmp_before_lock:
            ThreadManagment.write_lock_counter = 0
            lock = True
    if lock:
        ThreadManagment.thread_locks[threading.get_ident()] = True
        # Wait until main thread unlocks this thread
        while ThreadManagment.thread_locks[threading.get_ident()]:        
            # Sleep for a short time to improve multithreaded performance by releasing GIL
            time.sleep(0.000001)

class SortingMetadata:
    """ Stores metadata connected to sorting such as cmp count """
    def __init__(self):
        self.cmp_cnt = 0
        self.last_cmp_left = 0
        self.last_cmp_right = 0
        self.write_cnt = 0
        self.read_cnt = 0
        self.last_write_key = 0
        self.last_read_key = 0
        self.mem_usage = 0

class SInt(int):
    """ Custom Int class. All custom functionality is created through decorators in setup_custom_int """
    pass

def inc_cmp_cnt(func):
    """ Decorator for incrementing the comparison counter and handle thread locking """
    def inner(*args, **kwargs):
        ThreadManagment.sort_data_by_thread[threading.get_ident()].cmp_cnt += 1
        # Handle thread locking if exceeding comparisons
        ThreadManagment.cmp_lock_counter += 1
        sleep_if_needed()
        # Save the two numbers being compared
        ThreadManagment.sort_data_by_thread[threading.get_ident()].last_cmp_left = args[0]
        ThreadManagment.sort_data_by_thread[threading.get_ident()].last_cmp_right = args[1]
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
        if len(args) > 0: 
            # If the list is being initialized by another list, find out the max of the list
            # without counting reads and writes. This saves computation later.
            lst = list(args[0])
            lst = [int(i) for i in lst]
            self.max = max(lst)

        super().__init__(*args, **kwargs)
    
    def __getitem__(self, key):
        ThreadManagment.sort_data_by_thread[threading.get_ident()].read_cnt += 1
        ThreadManagment.read_lock_counter += 1
        sleep_if_needed()
        ret_val = super().__getitem__(key)
        if isinstance(ret_val, list):
            return SList(ret_val)
            
        if isinstance(key, int):
            ThreadManagment.sort_data_by_thread[threading.get_ident()].last_read_key = key

        return ret_val

    def getitem_no_count(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        ThreadManagment.sort_data_by_thread[threading.get_ident()].write_cnt += 1
        ThreadManagment.write_lock_counter += 1
        sleep_if_needed()
        if isinstance(key, int):
            ThreadManagment.sort_data_by_thread[threading.get_ident()].last_write_key = key
        return super().__setitem__(key, value)

    # Helper functions
    def get_last_read_key(self):
        return ThreadManagment.sort_data_by_thread[threading.get_ident()].last_read_key

    def get_last_write_key(self):
        return ThreadManagment.sort_data_by_thread[threading.get_ident()].last_write_key

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
