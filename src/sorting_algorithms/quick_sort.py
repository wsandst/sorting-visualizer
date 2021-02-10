
sort_name = "Quick Sort"
sort_func_name = "quick_sort"

def quick_sort(lst):
    partition(lst, 0, len(lst))

# LR Pointer implementation
def partition(lst, start, end):
    if (end - start) <= 1:
        return

    pivot_index = (start + end) // 2 # Pivot in middle
    pivot = lst[pivot_index]

    lst[end-1], lst[pivot_index] = lst[pivot_index], lst[end-1] # Put pivot at end


    left_index = start
    right_index = end-2
    # Put elements higher than pivot to the right, lower to the left, meet in middle
    while left_index <= right_index:
        if lst[left_index] < pivot:
            left_index += 1
        else:
            lst[left_index], lst[right_index] = lst[right_index], lst[left_index]
            right_index -= 1

    lst[left_index], lst[end - 1] = lst[end - 1], lst[left_index]
    partition(lst, start, left_index)
    partition(lst, left_index + 1, end)

# Different implemenation
def partition2(lst, start, end):
    if (end - start) <= 1:
        return

    pivot_index = (start + end) // 2 # Pivot in middle
    pivot = lst[pivot_index]
    lst[end], lst[pivot_index] = lst[pivot_index], lst[end] # Put pivot at end

    i = start-1
    # Swap elements from left to right to partition
    for j in range(start, end):
        if lst[j] < pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]

    partition2(lst, start, i)
    partition2(lst, i, end)

# Uses more comparisons but less writes and is janky
"""
        if lst[left_index] < pivot:
            left_index += 1
        else:
            while left_index <= right_index and lst[right_index] >= pivot:
                right_index -= 1
            if left_index <= right_index:
                lst[left_index], lst[right_index] = lst[right_index], lst[left_index]
                right_index -= 1
                left_index += 1
"""