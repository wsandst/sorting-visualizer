
def quick_sort(lst):
    partition(lst, 0, len(lst)-1)
    #partition_old(lst, 0, len(lst)-1)

def partition(lst, start, end):
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

    partition(lst, start, i)
    partition(lst, i, end)


# Old more inefficient version (?)
def partition_old(lst, start, end):
    if (end - start) <= 1:
        return

    pivot_index = (start + end) // 2 # Pivot in middle
    pivot = lst[pivot_index]
    lst[end], lst[pivot_index] = lst[pivot_index], lst[end] # Put pivot at end

    right_index = end-1
    left_index = start
    # Put elements higher than pivot to the right, lower to the left, meet in middle
    while left_index < right_index:
        if lst[right_index] < pivot:
            if lst[left_index] > pivot:
                lst[left_index], lst[right_index] = lst[right_index], lst[left_index]
            else:
                left_index += 1
        else:
            right_index -= 1

    partition(lst, start, left_index)
    partition(lst, right_index, end)
