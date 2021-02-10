
sort_name = "Bubble Sort"
sort_func_name = "bubble_sort"

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
