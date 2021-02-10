import gui
from sorting_algorithms import *
from special_types import SList, ThreadManagment

def main():
    lst = SList()
    #lst.shuffle_linear(40)
    # Init all the sorting algorithms
    sorting_func_map = {}

    # Naive
    sorting_func_map["Insertion Sort"] = insertion_sort.insertion_sort
    sorting_func_map["Selection Sort"] = selection_sort.selection_sort
    sorting_func_map["Bubble Sort"] = bubble_sort.bubble_sort
    sorting_func_map["Bubble Sort of Doom"] = bubble_sort_of_doom.bubble_sort_of_doom
    sorting_func_map["Cocktail Sort"] = cocktail_sort.cocktail_sort
    sorting_func_map["Gnome Sort"] = gnome_sort.gnome_sort

    # Divide and Conquer
    sorting_func_map["Merge Sort"] = merge_sort.merge_sort
    sorting_func_map["Heap Sort"] = heap_sort.heap_sort
    sorting_func_map["Quick Sort"] = quick_sort.quick_sort

    # Gap based
    sorting_func_map["Shell Sort"] = shell_sort.shell_sort
    sorting_func_map["Comb Sort"] = comb_sort.comb_sort

    # Non-comparison sorts
    sorting_func_map["Counting Sort"] = counting_sort.counting_sort
    sorting_func_map["Radix LSD Sort"] = radix_lsd_sort.radix_lsd_sort

    # Other
    sorting_func_map["Python TimSort"] = lambda x: py_timsort.timsort(x, ThreadManagment)
    sorting_func_map["Bogo Sort of Doom"] = bogo_sort_of_doom.bogo_sort_of_doom
    sorting_func_map["Bogo Sort"] = bogo_sort.bogo_sort
    sorting_func_map["Cubic Sort"] = cubic_sort.cubic_sort

    # Sort dict alphabetically, None at top. Python3 dicts are ordered
    sorting_func_map_sorted = {"None": 0}
    sorting_func_map_sorted.update(dict(sorted(sorting_func_map.items())))

    application = gui.MainApplication(sorting_func_map_sorted)
    
if __name__ == "__main__":
    main()

