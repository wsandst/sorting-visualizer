import gui

import special_types
from special_types import SInt, SList

def main():

    lst = SList()
    lst.randomize(100, 100)
    lst.sort()

    lst[0] = lst[1]

    print(f'cmp:   {special_types.comparison_cnt}')
    print(f'read:  {lst.read_cnt}')
    print(f'write: {lst.write_cnt}')

    #application = gui.MainApplication()
    
if __name__ == "__main__":
    main()

