
def selection_sort(lst):
    index = 0
    for i in range(len(lst)):
        min_index = index
        # Find min in range that is not sorted
        for i in range(index, len(lst)):
            if lst[i] < lst[min_index]:
                min_index = i
        # Swap in min
        lst[index], lst[min_index] = lst[min_index], lst[index]
        index += 1
    

