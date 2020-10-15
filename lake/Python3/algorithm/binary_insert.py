# https://docs.python.org/3.6/library/bisect.html

import bisect

bisect.bisect_left(a, x, lo=0, hi=len(a))  # bisect.bisect_left([2, 4, 4, 6], 4) -> 1

bisect.bisect_right(a, x, lo=0, hi=len(a))  # bisect.bisect_left([2, 4, 4, 6], 4) -> 3

bisect.insort_left(a, x, lo=0, hi=len(a))  # same as a.insert(bisect.bisect_left(a, x, lo, hi), x)

bisect.insort_right(a, x, lo=0, hi=len(a))
