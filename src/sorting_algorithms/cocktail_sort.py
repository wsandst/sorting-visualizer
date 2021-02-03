import random

def _cocktail_up(lst, start, end):
    last_change = start
    sorting = False
    for i in range(start, end - 1):
        if lst[i] > lst[i + 1]:
            sorting = True
            lst[i], lst[i + 1] = lst[i + 1], lst[i]
            last_change = i + 1
    if sorting:
        return (start, last_change)
    return False

def _cocktail_down(lst, start, end):
    last_change = end - 1
    sorting = False
    for i in range(end - 1, start, -1):
        if lst[i] < lst[i - 1]:
            last_change = i
            sorting = True
            lst[i], lst[i - 1] = lst[i - 1], lst[i]
    if sorting:
        return (last_change, end)
    return False

def cocktail_sort(lst):
    ends = (0, len(lst))
    
    while ends:
        ends = _cocktail_up(lst, ends[0], ends[1])
        if ends:
            ends = _cocktail_down(lst, ends[0], ends[1])