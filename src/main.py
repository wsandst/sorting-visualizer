import gui
import sorting_algorithms
import types
from special_types import ThreadManagment

def main():
    #lst.shuffle_linear(40)
    # Init all the sorting algorithms
    sorting_func_map = {}

    # Dynamically import all sorting algo files under sorting_algorithms/
    for sorting_mod in sorting_algorithms.__all__:
        mod = getattr(__import__(f"sorting_algorithms.{sorting_mod}"), sorting_mod)
        sorting_func_map[mod.sort_name] = getattr(mod, mod.sort_func_name)

    # Lambda needed here due to special requirements
    sorting_func_map["Python TimSort"] = (lambda x: sorting_algorithms.py_timsort.timsort(x, ThreadManagment))

    # Sort dict alphabetically, None at top. Python3 dicts are ordered
    sorting_func_map_sorted = {"None": 0}
    sorting_func_map_sorted.update(dict(sorted(sorting_func_map.items())))

    application = gui.MainApplication(sorting_func_map_sorted)
    
if __name__ == "__main__":
    main()

