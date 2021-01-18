import special_types
from special_types import SInt, SList

import threading
import time
import random


def bubble_sort(lst):
    sorting = True
    for j in range(len(lst) - 1, -1, -1):
        sorting = False
        for i in range(j):
            if lst[i + 1] < lst[i]:
                sorting = True
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
        if not sorting:
            break
    return lst

class SortingAlgorithm():
    def __init__(self, func, name, lst):
        self.lst = SList(lst)
        self.thread = threading.Thread(target = func, args = (self.lst,))
        self.name = name
    
    def run(self):
        self.thread.start()

    def get_comparisons(self):
        return special_types.cmp_cnt_by_thread[self.thread.ident]

    def is_thread_locked(self):
        return special_types.thread_locks[self.thread.ident]

    def unlock(self):
        special_types.thread_locks[self.thread.ident] = False

def bubble_sort_of_doom(lst):
    max_index = len(lst) - 1
    while max_index:
        last_change_index = 0
        for i in range(max_index):
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                last_change_index = i
        max_index = last_change_index

def display_info(algo):
    print(f'{algo.name}:')
    print(algo.lst)
    print(f'cmp:   {algo.get_comparisons()}')
    print(f'read:  {algo.lst.read_cnt}')
    print(f'write: {algo.lst.write_cnt}')


def start_sorting(sorting_algos):
    for algo in sorting_algos:
        algo.run()

def run_sorting(sorting_algos):
    start_sorting(sorting_algos)
    while True:
        any_thread_alive = False
        for algo in sorting_algos:
            if algo.thread.is_alive():
                any_thread_alive = True
                while not algo.is_thread_locked() and algo.thread.is_alive():
                    time.sleep(0.000001)
                display_info(algo)
                algo.unlock()
                time.sleep(0.000001)
        if not any_thread_alive:
            break
