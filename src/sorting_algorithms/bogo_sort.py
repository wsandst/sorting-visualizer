
import random

sort_name = "Bogo Sort"
sort_func_name = "bogo_sort"

def bogo_sort(lst):
    sorted_list = [int(i) for i in lst.copy()]
    sorted_list.sort()
    while sorted_list != [int(i) for i in lst.copy()]:
        i1 = random.randint(0,len(lst)-1)
        i2 = random.randint(0,len(lst)-1)
        lst[i1], lst[i2] = lst[i2], lst[i1]
        # Do comparison to hit counter
        lst[i1] < lst[i2]