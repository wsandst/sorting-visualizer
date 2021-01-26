
def bubble_sort_of_doom(lst):
    max_index = len(lst) - 1
    while max_index:
        last_change_index = 0
        for i in range(max_index):
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                last_change_index = i
        max_index = last_change_index
