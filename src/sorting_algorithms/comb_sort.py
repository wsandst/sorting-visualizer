import math

sort_name = "Comb Sort"
sort_func_name = "comb_sort"

def comb_sort(lst):
    gap = len(lst)
    shrink_factor = 1.3
    sorting = True
    while sorting:
        gap = math.floor(gap / shrink_factor)
        if gap <= 1:
            sorting = False
            gap = 1
        for i in range(len(lst)-gap):
            if lst[i] > lst[i+gap]:
                lst[i], lst[i+gap] = lst[i+gap], lst[i]
                sorting = True