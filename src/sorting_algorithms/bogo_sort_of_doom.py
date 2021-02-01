
""" Bogo sort which only swaps elements if they make the list more sorted """
import random

def bogo_sort_of_doom(lst):
    sorted_list = [int(i) for i in lst.copy()]
    sorted_list.sort()
    while sorted_list != [int(i) for i in lst.copy()]:
        i1 = random.randint(0,len(lst)-1)
        i2 = random.randint(i1,len(lst)-1)
        if lst[i2] < lst[i1]:
            lst[i1], lst[i2] = lst[i2], lst[i1]