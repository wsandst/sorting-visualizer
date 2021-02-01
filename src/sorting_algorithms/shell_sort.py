import math

def shell_sort(lst):
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap,len(lst)): 
            # add a[i] to the elements that have been gap sorted 
            # save a[i] in temp and make a hole at position i 
            temp = lst[i] 

            # shift earlier gap-sorted elements up until the correct 
            # location for a[i] is found 
            j = i 
            while  j >= gap and lst[j-gap] >temp: 
                lst[j] = lst[j-gap] 
                j -= gap 

            # put temp (the original a[i]) in its correct location 
            lst[j] = temp 