
def insertion_sort(lst):
    for j in range(len(lst)-1):
        for i in range(j+1):
            if lst[j-i] > lst[j-i+1]: # Swap down if smaller
                lst[j-i], lst[j-i+1] = lst[j-i+1], lst[j-i]
            else:
                break