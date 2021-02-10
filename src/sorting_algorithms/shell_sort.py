import math

sort_name = "Shell Sort"
sort_func_name = "shell_sort"

def shell_sort(lst):
    gaps = [1750, 701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        # Insertion sort
        for i in range(gap,len(lst)): 
            temp = lst[i] 

            j = i 
            while  j >= gap and lst[j-gap] >temp: 
                lst[j] = lst[j-gap] 
                j -= gap 

            lst[j] = temp 