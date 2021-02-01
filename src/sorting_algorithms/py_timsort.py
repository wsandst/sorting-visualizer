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
    thread_management_ref = 0

def custom_cmp(lhs, rhs):
    if CounterWrapper.cmp_counter >= CounterWrapper.cmp_limit:
        # Record the lhs and rhs for visualization
        CounterWrapper.thread_management_ref.sort_data_by_thread[threading.get_ident()].last_cmp_left = lhs
        CounterWrapper.thread_management_ref.sort_data_by_thread[threading.get_ident()].last_cmp_right = rhs
        raise TimBreak # Interupt if counter exceeded
    CounterWrapper.cmp_counter += 1
    return lhs - rhs

def timsort(lst, thread_management_ref):
    """ 
    This is a special type of sort, in order to track list.sort() 
    sort() is stopped after a set amount of comparisons using exceptions.
    By successively increasing this limit and resetting the list every time,
    we can inspect the state of the list after every comparison for visualization
    """
    CounterWrapper.thread_management_ref = thread_management_ref
    lst.__init__([int(i) for i in lst]) # Remove the custom int class from the list to prevent standard behaviour

    orig_list = lst.copy()
    while True:
        CounterWrapper.cmp_counter = 0
        CounterWrapper.cmp_limit += thread_management_ref.cmp_before_lock # Do x more comparisons next run
        thread_management_ref.sort_data_by_thread[threading.get_ident()].cmp_cnt = CounterWrapper.cmp_limit
        lst.__init__(orig_list.copy()) # Reset list to unsorted state
        try:
            lst.sort(key=cmp_to_key(custom_cmp)) # Sort list using custom compare function
        except TimBreak:
            wait_for_thread_unlock(thread_management_ref.thread_locks) # Lock thread after exception to allow for GUI update
        else:
            # No exception raised -> no comparisons -> list sorted, we are done
            wait_for_thread_unlock(thread_management_ref.thread_locks)
            break

# Wait until the GUI thread allows for more sorting
def wait_for_thread_unlock(thread_locks):
    thread_locks[threading.get_ident()] = True
    while thread_locks[threading.get_ident()]:
        time.sleep(0.000001)