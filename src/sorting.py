import special_types
from special_types import SInt, SList

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
    
    def run(self):
        self.thread.start()

    def get_comparisons(self):
        return special_types.cmp_cnt_by_thread[self.thread.ident]

    def get_reads(self):
        return self.lst.read_cnt

    def get_writes(self):
        return self.lst.write_cnt

    def is_thread_locked(self):
        if self.thread.ident in special_types.thread_locks:
            return special_types.thread_locks[self.thread.ident]
        else:
            return False

    def unlock(self):
        special_types.thread_locks[self.thread.ident] = False

    def get_coloring(self):
        """ Return an array representing coloring of specific indices """
        colors = [0] * len(self.lst)
        if self.lst.last_read_key >= 0:
            colors[self.lst.last_read_key] = 2
        if self.lst.last_write_key >= 0:
            colors[self.lst.last_write_key] = 2
        return colors


def start_sorting(sorting_algos):
    """ Start the threads of all the sorting algorithms """
    for algo in sorting_algos:
        algo.run()

def run_sorting_step(sorting_algos):
    """ Run sorting for x comparisons, then lock the thread as defined in special_types """
    any_thread_alive = False
    for algo in sorting_algos:
        if not algo.is_thread_locked():
            return False
        any_thread_alive = any_thread_alive or algo.thread.is_alive()
    if not any_thread_alive:
        return False