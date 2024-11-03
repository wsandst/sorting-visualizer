import random, math

sort_name = "BogoPre Insertion Sort"
sort_func_name = "bogo_pre_insertion_sort"

def bogo_pre_insertion_sort(lst):
    for j in range(len(lst)*int(math.log2(len(lst)))):
        i1 = random.randint(0,len(lst)-2)
        i2 = random.randint(i1+1,len(lst)-1)
        if lst[i2] < lst[i1]:
            lst[i1], lst[i2] = lst[i2], lst[i1]
    for j in range(1, len(lst)):
        key = lst[j]
        i = j - 1
        while i >= 0 and lst[i] >= key:
            lst[i+1] = lst[i]
            i -= 1
        lst[i+1] = key
    return lst