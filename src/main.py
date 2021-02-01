import gui
from sorting_algorithms import *
from sorting import SortingAlgorithm
from special_types import SList, ThreadManagment


def main():
    lst = SList()
    lst.shuffle_linear(64)
    # Init all the sorting algorithms
    sorting_algos = [SortingAlgorithm(merge_sort.merge_sort, "Merge Sort", lst),
                    #SortingAlgorithm(heap_sort.heap_sort, "Heap Sort", lst),
                    #SortingAlgorithm(bubble_sort.bubble_sort, "Bubble Sort", lst),
                    #SortingAlgorithm(lambda x: py_timsort.timsort(x, ThreadManagment), "Python TimSort", lst),
                    #SortingAlgorithm(insertion_sort.insertion_sort, "Insertion Sort", lst),
                    #SortingAlgorithm(selection_sort.selection_sort, "Selection Sort", lst),
                    SortingAlgorithm(quick_sort.quick_sort, "Quick Sort", lst),
                    #SortingAlgorithm(bogo_sort_of_doom.bogo_sort_of_doom, "Bogo Sort of Doom", lst),
                    #SortingAlgorithm(bogo_sort.bogo_sort, "Bogo Sort", lst),
                    SortingAlgorithm(shell_sort.shell_sort, "Shell Sort", lst),
                    SortingAlgorithm(counting_sort.counting_sort, "Counting Sort", lst)]
                    #SortingAlgorithm(comb_sort.comb_sort, "Comb Sort", lst)]
                    #SortingAlgorithm(bubble_sort_of_doom.bubble_sort_of_doom, "Bubble Sort of Doom", lst)]
                    #SortingAlgorithm(cocktail_sort_of_doom.cocktail_sort, "Cocktail Sort of Doom", lst)]

    application = gui.MainApplication(sorting_algos)
    
if __name__ == "__main__":
    main()

