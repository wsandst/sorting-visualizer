import gui
from sorting import *
from special_types import SList


def main():
    lst = SList()
    lst.randomize_linear(400)

    sorting_algos = [SortingAlgorithm(bubble_sort, "Bubble Sort", lst)]
                    #SortingAlgorithm(bubble_sort_of_doom, "Bubble Sort of Doom", lst)]

    application = gui.MainApplication(sorting_algos)

    #run_sorting(sorting_algos)
    
if __name__ == "__main__":
    main()

