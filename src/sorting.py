import special_types
from special_types import SInt, SList, ThreadManagment

import threading, time

def sleep_then_run(func, lst):
    # This sleep improves multithreaded performance by releasing the GIL
    time.sleep(0.05)
    func(lst)

class SortingAlgorithm():
    """
        Represents a Sorting Algorithm and handles its unique thread and related info
    """
    def __init__(self, func, name, lst):
        self.lst = SList(lst)
        self.thread = threading.Thread(target = sleep_then_run, args = (func, self.lst))
        self.thread.daemon = True
        self.name = name
        self.sorting_active = False
        self.sorted_lst = sorted([int(i) for i in self.lst])

    def run(self):
        """ Start the thread and start sorting """
        self.thread.start()
        special_types.ThreadManagment.sort_data_by_thread[self.thread.ident] = special_types.SortingMetadata()
        self.sorting_active = True

    def get_comparisons(self):
        return ThreadManagment.sort_data_by_thread[self.thread.ident].cmp_cnt

    def get_reads(self):
        return ThreadManagment.sort_data_by_thread[self.thread.ident].read_cnt

    def get_writes(self):
        return ThreadManagment.sort_data_by_thread[self.thread.ident].write_cnt

    def get_sound_index(self):
        """ Return which the index which the sound effect should be based on """
        # Return difference between the two last compared elements
        lhs = ThreadManagment.sort_data_by_thread[self.thread.ident].last_cmp_left
        #rhs = ThreadManagment.last_cmp_right_by_thread.get(self.thread.ident, 0)
        #return round((lhs + rhs) / 2)
        return lhs

    def requires_rendering(self, skip_bool_switch=False):
        """ Does this sorting thread require rendering? """
        if self.sorting_active: 
            # This is to ensure the last frame when the thread is complete is still rendered
            if (not skip_bool_switch):
                self.sorting_active = self.thread.is_alive()
            return True
        else:
            return False

    def is_thread_locked(self):
        """ Is the thread locked (no longer sorting)?"""
        if self.thread.ident in ThreadManagment.thread_locks:
            return ThreadManagment.thread_locks[self.thread.ident]
        else:
            return False

    def unlock(self):
        ThreadManagment.thread_locks[self.thread.ident] = False

    def get_coloring(self):
        """ Return an array representing coloring of specific element indices """
        colors = dict()
        colors[-1] = 0
        if not self.sorting_active: # Don't want any normal colors on the last frame
            new_list = [int(i) for i in self.lst]
            if self.sorted_lst == new_list: # The list is sorted, color it green
                colors[-1] = 1
                return colors
        # Last  read
        last_read_key = ThreadManagment.sort_data_by_thread[self.thread.ident].last_read_key
        if last_read_key >= 0:
            colors[last_read_key] = 2
        # Last write
        last_write_key = ThreadManagment.sort_data_by_thread[self.thread.ident].last_write_key
        if last_write_key >= 0:
            colors[last_write_key] = 2
        # Last lhs comparison
        last_cmp_left_value = ThreadManagment.sort_data_by_thread[self.thread.ident].last_cmp_left
        for i in range(len(self.lst)):
            if int(self.lst.getitem_no_count(i)) == int(last_cmp_left_value):
                colors[i] = 3
                break
        # Last rhs comparison
        last_cmp_right_value =  ThreadManagment.sort_data_by_thread[self.thread.ident].last_cmp_right
        for i in range(len(self.lst)):
            if int(self.lst.getitem_no_count(i)) == int(last_cmp_right_value):
                colors[i] = 3
                break
        return colors


def start_sorting(sorting_algos):
    """ Start the threads of all the sorting algorithms """
    for algo in sorting_algos:
        algo.run()

def is_sorting_step_complete(sorting_algos):
    """ Is the sorting step complete for all threads? """
    for algo in sorting_algos:
        if not algo.is_thread_locked() and algo.thread.is_alive():
            # At least one algorithm is still running and is not locked, ie not done
            return False
    return True