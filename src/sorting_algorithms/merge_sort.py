
"""def insertion_sort(lst, start, end):
    for j in range(end-start-1):
        for i in range(j+1):
            if lst[start+j-i] > lst[start+j-i+1]: # Swap down if smaller
                lst[start+j-i], lst[start+j-i+1] = lst[start+j-i+1], lst[start+j-i]
            else:
                break
    return lst[start:end]"""

def merge_sort(lst):
    divide(lst, 0, len(lst)-1)

def divide(lst, start, end):
    middle = (end + start) // 2 
    if start >= end:
        return
    divide(lst, start, middle)
    divide(lst, middle+1, end)
    merge(lst[start:middle+1], lst[middle+1:end+1], lst, start, end)

def merge(lst1, lst2, lst, start, end):
    lst1_index = 0
    lst2_index = 0
    for i in range(end-start+1):
        if lst2_index >= len(lst2) or (lst1_index < len(lst1) and lst1[lst1_index] < lst2[lst2_index]):
            lst[start+i] = lst1[lst1_index]
            lst1_index += 1
        else:
            lst[start+i] = lst2[lst2_index]
            lst2_index += 1