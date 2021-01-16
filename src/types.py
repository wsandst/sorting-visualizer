""" Implements a custom Int and List class which keeps track of various usage statistics"""

comparison_cnt = 0
read_cnt = 0
write_cnt = 0

def inc_cmp_cnt(func):
    def inner(*args, **kwargs):
        global comparison_cnt
        comparison_cnt = comparison_cnt + 1
        return func(*args, **kwargs)
    return inner

def inc_read_cnt(func):
    def inner(*args, **kwargs):
        global read_cnt
        read_cnt = read_cnt + 1
        return func(*args, **kwargs)
    return inner

def inc_write_cnt(func):
    def inner(*args, **kwargs):
        global write_cnt
        write_cnt = write_cnt + 1
        return func(*args, **kwargs)
    return inner


class SInt(int):
    pass

class SList(list):
    pass

def setup_custom_int():
    # Loop through the relevant comparisons functions in SInt which are inherited
    # from int and correspond to the comparison operators and
    # decorate them with function inc_cmp_cnt which increments the comparison counter
    for attr in ["__eq__", "__ge__", "__le__", "__gt__", "__lt__", "__ne__"]:
        decorator = inc_cmp_cnt((getattr(SInt, attr)))
        setattr(SInt, attr, decorator)


def setup_custom_list():
    pass

def setup():
    setup_custom_int()
    setup_custom_list()

    a = SInt(1)
    b = SInt(2)
    print(a < b)
    print(a < b)
    print(comparison_cnt)

if __name__ == "__main__":
    setup()
