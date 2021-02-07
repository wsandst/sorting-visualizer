
def insertion_sort(lst):
    for j in range(1, len(lst)):
        key = lst[j]
        i = j - 1
        while i >= 0 and key < lst[i]:
            lst[i+1] = lst[i]
            i -= 1
        lst[i+1] = key
    return lst