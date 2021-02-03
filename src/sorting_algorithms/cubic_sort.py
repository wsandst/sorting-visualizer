

def cubic_sort(v):
    """A generator that sorts v in place"""
    direction = 1
    i = len(v)//2
    last_end = 0
    while 1:
        n_i = i + direction
        if n_i >= len(v) or n_i < 0:
            direction *= -1
            if n_i >= len(v):
                if last_end == -1:
                    break
                last_end = 1
            if n_i < 0:
                if last_end == 1:
                    break
                last_end = -1
            continue
        high = max(n_i, i)
        low = min(n_i, i)
        if v[high] < v[low]:
            v[low], v[high] = v[high], v[low]
            direction *= -1
            last_end = 0
            n_i = min(len(v) - 1, max(0, i + direction))
        i = n_i