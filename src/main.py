import gui
from sorting_algorithms import *
from sorting import SortingAlgorithm
from special_types import SList


def main():
    lst = SList()
    lst.shuffle_linear(50)
    # Init all the sorting algorithms
    sorting_algos = [SortingAlgorithm(bubble_sort.bubble_sort, "Bubble Sort", lst),
                    SortingAlgorithm(bubble_sort_of_doom.bubble_sort_of_doom, "Bubble Sort of Doom", lst),
                    SortingAlgorithm(cocktail_sort_of_doom.cocktail_sort, "Cocktail Sort of Doom", lst)]

    application = gui.MainApplication(sorting_algos)
    
if __name__ == "__main__":
    main()

