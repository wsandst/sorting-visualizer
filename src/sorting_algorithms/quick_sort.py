
import random

def quick_sort(lst):
    partition(lst, lst[10], 10, 0, len(lst)-1)

def partition(lst, pivot, pivot_index, start, end):
    if (end - start) <= 1:
        return
    lst[end], lst[pivot_index] = lst[pivot_index], lst[end] # Put pivot at end
    right_index = end-1
    left_index = start
    while left_index < right_index:
        if lst[right_index] < pivot:
            if lst[left_index] > pivot:
                lst[left_index], lst[right_index] = lst[right_index], lst[left_index]
            else:
                left_index += 1
        else:
            right_index -= 1 
    new_pivot1_index = (start + left_index) // 2 # random.randint(start,left_index)
    new_pivot2_index = (left_index + end) // 2 # random.randint(left_index, end)
    partition(lst, lst[new_pivot1_index], new_pivot1_index, start, left_index)
    partition(lst, lst[new_pivot2_index], new_pivot2_index, right_index, end)
