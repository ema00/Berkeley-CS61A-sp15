from objects import *

## Iterators

class LinkIterator:
    """
    >>> lnk = Link(1, Link(2, Link(3)))
    >>> lnk_iter = LinkIterator(lnk)
    >>> next(lnk_iter)
    1
    >>> next(lnk_iter)
    2
    """
    def __init__(self, link):
        self.link = link

    def __iter__(self):
        return self

    def __next__(self):
        if self.link == Link.empty:
            raise StopIteration
        else:
            val = self.link.first
            self.link = self.link.rest
            return val


## Generators

def in_order(t):
    """
    Yields the entries of a valid binary search tree in sorted order.

    >>> b = BTree(5, BTree(3, BTree(2), BTree(4)), BTree(6))
    >>> list(in_order(b))
    [2, 3, 4, 5, 6]
    >>> list(in_order(bst([1, 3, 5, 7, 9, 11, 13])))
    [1, 3, 5, 7, 9, 11, 13]
    >>> list(in_order(BTree(1)))
    [1]
    """
    if not t.is_leaf():
        for root in in_order(t.left):
            yield root

    yield t.root

    if not t.is_leaf():
        for root in in_order(t.right):
            yield root
"""
    # alternate solution, shorter
    if not t.is_leaf():
        yield from in_order(t.left)
    yield t.root
    if not t.is_leaf():
        yield from in_order(t.right)
"""


def permutations(lst):
    """Generates all permutations of sequence LST. Each permutation is a
    list of the elements in LST in a different order.

    The order of the permutations does not matter.

    >>> sorted(permutations([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> type(permutations([1, 2, 3]))
    <class 'generator'>
    >>> sorted(permutations((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(permutations("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    if not lst:
        yield []
        return
    if len(lst) == 1:
        yield lst[:]
    else:
        for i in range(len(lst)):
            for sublist_permutation in permutations(list(lst[:i]) + list(lst[i+1:])):
                yield list([lst[i]]) + sublist_permutation

# CALCULATING ALL THE PERMUTATIONS AT ONCE
def perms(lst):
	if len(lst) == 1:
		return [lst[:]]
	else:
		result = []
		for i in range(len(lst)):
			result += [[lst[i]] + subperm for subperm in perms(lst[:i] + lst[i+1:])]
		return result


## Streams

def scale_stream(s, k):
    """Return a stream of the elements of S scaled by a number K.

    >>> ints = make_integer_stream(1)
    >>> s = scale_stream(ints, 5)
    >>> stream_to_list(s, 5)
    [5, 10, 15, 20, 25]
    >>> s = scale_stream(Stream("x", lambda: Stream("y")), 3)
    >>> stream_to_list(s)
    ['xxx', 'yyy']
    >>> stream_to_list(scale_stream(Stream.empty, 10))
    []
    """
    if s == Stream.empty:
        return s
    else:
        return Stream(s.first * k, lambda: scale_stream(s.rest, k))
    #return map_stream(lambda elem: k * elem, s)


def merge(s0, s1):
    """Return a stream over the elements of strictly increasing s0 and s1,
    removing repeats. Assume that s0 and s1 have no repeats.

    >>> ints = make_integer_stream(1)
    >>> twos = scale_stream(ints, 2)
    >>> threes = scale_stream(ints, 3)
    >>> m = merge(twos, threes)
    >>> stream_to_list(m, 10)
    [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    if s0 is Stream.empty:
        return s1
    elif s1 is Stream.empty:
        return s0

    e0, e1 = s0.first, s1.first
    if e0 < e1:
        return Stream(e0, lambda: merge(s1, s0.rest))
    elif e0 > e1:
        return Stream(e1, lambda: merge(s0, s1.rest))
    else:
        return Stream(e0, lambda: merge(s1.rest, s0.rest))


def make_s():
    """Return a stream over all positive integers with only factors 2, 3, & 5.

    >>> s = make_s()
    >>> stream_to_list(s, 20)
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36]
    """
    from math import gcd, log
    def filter_regular_numbers(n):
        """Return True for numbers that are a power of 2, 3 or 5, and also
        for numbers that are divisible by two of 2, 3 and 5.
        Returns False for numbers that are a multiple of 2, 3 or 5 and a prime
        greater than 5.
        Also filters out the primes greater than 5, if passed as argument.
        For powers of any of 2, 3 or 5, and for multiples of 2, 3 or 5 and a
        prime greater than 5, two of the GCDs are 1 (the other is the multiple).
        """
        g2 = gcd(n, 2)
        g3 = gcd(n, 3)
        g5 = gcd(n, 5)
        if (g2 == 1 and g3 == 1):   # True if n is power of 5
            exponent = int(log(n, 5))
            return pow(5, exponent) == n
        elif (g2 == 1 and g5 == 1): # True if n is power of 3
            exponent = int(log(n, 3))
            return pow(3, exponent) == n
        elif (g3 == 1 and g5 == 1): # True if n is power of 2
            exponent = int(log(n, 2))
            return pow(2, exponent) == n
        else:                       # n is multiple of two or three of 2, 3, 5
            return True

    def rest():
        naturals = make_integer_stream(1)
        multiples_2 = scale_stream(naturals, 2)
        multiples_3 = scale_stream(naturals, 3)
        multiples_5 = scale_stream(naturals, 5)
        merged_streams = merge(multiples_2, merge(multiples_3, multiples_5))
        return filter_stream(filter_regular_numbers, merged_streams)
        # EL NÚMERO ES UNA POTENCIA ENTERA DE 2, 3 O 5, O ESTÁ EN 2 DE LAS 3 SECUENCIAS

    s = Stream(1, rest)
    return s

def filter_stream(predicate, s):
    if s is Stream.empty:
        return s
    elif predicate(s.first):
        return Stream(s.first, lambda: filter_stream(predicate, s.rest))
    else:
        return filter_stream(predicate, s.rest)


from operator import add, mul, mod

def make_random_stream(seed, a, c, n):
    """The infinite stream of pseudo-random numbers generated by the
    recurrence r[0] = SEED, r[i+1] = (r[i] * A + C) % N.

    >>> s = make_random_stream(25, 29, 5, 32)
    >>> stream_to_list(s, 10)
    [25, 26, 23, 0, 5, 22, 3, 28, 17, 18]
    >>> s = make_random_stream(17, 299317, 13, 2**20)
    >>> stream_to_list(s, 10)
    [17, 894098, 115783, 383424, 775373, 994174, 941859, 558412, 238793, 718506]
    """
    return Stream(seed, lambda: make_random_stream(mod(seed * a + c, n), a, c, n))


def make_stream_of_streams():
    """
    >>> stream_of_streams = make_stream_of_streams()
    >>> stream_of_streams
    Stream(Stream(1, <...>), <...>)
    >>> stream_of_streams.rest
    Stream(Stream(2, <...>), <...>)
    >>> stream_of_streams.rest.rest
    Stream(Stream(3, <...>), <...>)
    >>> stream_of_streams
    Stream(Stream(1, Stream(2, Stream(3, <...>))), Stream(Stream(2, Stream(3, <...>)), Stream(Stream(3, <...>), <...>)))
    """
    def result(st):
        return Stream(st, lambda: result(st.rest))
    return result(make_integer_stream(1))
