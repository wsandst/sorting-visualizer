
def counting_sort(lst):
    # Find max to determine table size
    max_val = max(lst)

    table = [0]*(max_val+1)
    for i in lst:
        table[i] += 1
    j = 0
    for i, count in enumerate(table):
        while count > 0:
            lst[j] = i
            count -= 1
            j += 1

def counting_sort_better_mem(lst):
    # Find max and min
    min_val = min(lst)
    max_val = max(lst)

    table = [0]*(max_val-min_val+1)
    for i in lst:
        table[i-min_val] += 1
    j = 0
    for i, count in enumerate(table):
        while count > 0:
            lst[j] = i+min_val
            count -= 1
            j += 1