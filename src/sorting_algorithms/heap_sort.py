sort_name = "Heap Sort"
sort_func_name = "heap_sort"

def sift_down(lst, i, mx):
    if i*2+1 >= mx:
        return
    swap_index = None
    swap_val = None
    val = lst[i]
    if i*2 + 2 >= mx:
        swap_index = i * 2 + 1
        swap_val = lst[i * 2 + 1]
    else:
        child1 = i * 2 + 1
        child2 = i * 2 + 2
        child1_val = lst[child1]
        child2_val = lst[child2]
        if child1_val >= child2_val:
            swap_index = child1
            swap_val = child1_val
        else:
            swap_index = child2
            swap_val = child2_val
    if swap_index != None and val < swap_val:
        lst[i], lst[swap_index] = swap_val, val
        sift_down(lst, swap_index, mx)

def heapify(lst):
    for i in range(len(lst) - 1, -1, -1):
        sift_down(lst, i, len(lst))


def heap_sort(lst):
    heapify(lst)
    max_i = len(lst) - 1
    while max_i > 0:
        lst[max_i], lst[0] = lst[0], lst[max_i]
        sift_down(lst, 0, max_i)
        max_i -= 1