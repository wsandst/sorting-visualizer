""" 
Visualizes Pythons inbuilt sorting, TimSort
The array can be left in a partially sorted state using interrupts, to visualize
Inspiration for interrupting from https://corte.si/posts/code/timsort/
"""

import time
import threading

from functools import cmp_to_key

class TimBreak(Exception): pass

# Avoiding globals
class CounterWrapper:
    cmp_counter = 0
    cmp_limit = 0

def custom_cmp(lhs, rhs):
    if CounterWrapper.cmp_counter >= CounterWrapper.cmp_limit:
        raise TimBreak
    CounterWrapper.cmp_counter += 1
    return lhs - rhs

def timsort(lst, ThreadManagment):
    """ This is a special type of sort, need to do some weird stuff """
    lst.__init__([int(i) for i in lst]) # Remove the custom int class from the list to prevent standard behaviour

    orig_list = lst.copy()
    while True:
        CounterWrapper.cmp_counter = 0
        CounterWrapper.cmp_limit += ThreadManagment.cmp_before_lock # Do x more comparisons next run
        lst.__init__(orig_list.copy()) # Reset list to unsorted state
        try:
            lst.sort(key=cmp_to_key(custom_cmp))
        except TimBreak:
            wait_for_thread_unlock(ThreadManagment.thread_locks) # Lock thread after exception to allow for GUI update
        else:
            break

def wait_for_thread_unlock(thread_locks):
    thread_locks[threading.get_ident()] = True
    while thread_locks[threading.get_ident()]:
        time.sleep(0.000001)