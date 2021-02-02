import gui
from sorting_algorithms import *
from sorting import SortingAlgorithm
from special_types import SList, ThreadManagment


def main():
    lst = SList()
    lst.shuffle_linear(100)
    # Init all the sorting algorithms
    sorting_algos = []

    # Naive
    sorting_algos.append(SortingAlgorithm(insertion_sort.insertion_sort, "Insertion Sort", lst))
    sorting_algos.append(SortingAlgorithm(selection_sort.selection_sort, "Selection Sort", lst))
    #sorting_algos.append(SortingAlgorithm(bubble_sort.bubble_sort, "Bubble Sort", lst))
    #sorting_algos.append(SortingAlgorithm(bubble_sort_of_doom.bubble_sort_of_doom, "Bubble Sort of Doom"))
    #sorting_algos.append(SortingAlgorithm(cocktail_sort_of_doom.cocktail_sort, "Cocktail Sort of Doom", lst))

    # Divide and Conquer
    sorting_algos.append(SortingAlgorithm(merge_sort.merge_sort, "Merge Sort", lst))
    #sorting_algos.append(SortingAlgorithm(heap_sort.heap_sort, "Heap Sort", lst))
    sorting_algos.append(SortingAlgorithm(quick_sort.quick_sort, "Quick Sort", lst))

    # Gap based
    sorting_algos.append(SortingAlgorithm(shell_sort.shell_sort, "Shell Sort", lst))
    sorting_algos.append(SortingAlgorithm(comb_sort.comb_sort, "Comb Sort", lst))

    # Non-comparison sorts
    #sorting_algos.append(SortingAlgorithm(counting_sort.counting_sort, "Counting Sort", lst))

    # Other
    #sorting_algos.append(SortingAlgorithm(lambda x: py_timsort.timsort(x, ThreadManagment), "Python TimSort", lst))
    #sorting_algos.append(SortingAlgorithm(bogo_sort_of_doom.bogo_sort_of_doom, "Bogo Sort of Doom", lst))
    #sorting_algos.append(SortingAlgorithm(bogo_sort.bogo_sort, "Bogo Sort", lst))

    application = gui.MainApplication(sorting_algos)
    
if __name__ == "__main__":
    main()

