
import math

sort_name = "Radix Sort"
sort_func_name = "radix_lsd_sort"

def get_digit(num, base, digit):
    return int((num / pow(base, digit)) % base)

def counting_sort(lst, base, digit):
    count_per_digit = [0] * base
    for j in range(len(lst)):
        val = lst[j]
        i = get_digit(val, base, digit)
        count_per_digit[i] += 1

    index_for_digit = [0] * base
    current_index = 0
    for i, count in enumerate(count_per_digit):
        index_for_digit[i] = current_index
        current_index += count
    return index_for_digit


def lsd_sort(lst, base, digit):
    index_for_digit = counting_sort(lst, base, digit)

    lst_buffer = [0] * len(lst)
    for val in lst:
        i = get_digit(val, base, digit)
        lst_buffer[index_for_digit[i]] = val
        index_for_digit[i] += 1
    return lst_buffer

def radix_lsd_sort(lst):
    base = 2
    mx = max(lst)

    digits = math.floor(math.log(mx, base))
    for digit in range(digits+1):
        buffer = lsd_sort(lst, base, digit)
        for i in range(len(lst)):
            lst[i] = buffer[i]