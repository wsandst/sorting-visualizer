import special_types
from special_types import SInt, SList, ThreadManagment

import threading

class SortingAlgorithm():
    """
        Represents a Sorting Algorithm and handles its unique thread and related info
    """
    def __init__(self, func, name, lst):
        self.lst = SList(lst)
        self.thread = threading.Thread(target = func, args = (self.lst,))
        self.thread.daemon = True
        self.name = name
        self.sorting_active = False
    
    def run(self):
        self.thread.start()
        self.sorting_active = True

    def get_comparisons(self):
        return ThreadManagment.cmp_cnt_by_thread.get(self.thread.ident, 0)

    def get_reads(self):
        return self.lst.read_cnt

    def get_writes(self):
        return self.lst.write_cnt

    def get_sound_index(self):
        # Return difference between the two last compared elements
        lhs = ThreadManagment.last_cmp_left_by_thread.get(self.thread.ident, 0)
        #rhs = ThreadManagment.last_cmp_right_by_thread.get(self.thread.ident, 0)
        #return round((lhs + rhs) / 2)
        return lhs

    def requires_rendering(self):
        if self.sorting_active: 
            # This is to ensure the last frame when the thread is complete is still rendered
            self.sorting_active = self.thread.is_alive()
            return True
        else:
            return False

    def is_thread_locked(self):
        if self.thread.ident in ThreadManagment.thread_locks:
            return ThreadManagment.thread_locks[self.thread.ident]
        else:
            return False

    def unlock(self):
        ThreadManagment.thread_locks[self.thread.ident] = False

    def get_coloring(self):
        """ Return an array representing coloring of specific indices """
        colors = [0] * len(self.lst)
        if not self.sorting_active: # Don't want any colors on the last frame
            return colors
        # Last read
        if self.lst.get_last_read_key() >= 0:
            colors[self.lst.get_last_read_key()] = 2
        # Last write
        if self.lst.get_last_write_key() >= 0:
            colors[self.lst.get_last_write_key()] = 2
        # Last lhs comparison
        last_cmp_left_value = ThreadManagment.last_cmp_left_by_thread.get(self.thread.ident,-1)
        for i in range(len(self.lst)):
            if int(self.lst.getitem_no_count(i)) == int(last_cmp_left_value):
                colors[i] = 3
                break
        # Last rhs comparison
        last_cmp_right_value = ThreadManagment.last_cmp_right_by_thread.get(self.thread.ident,-1)
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