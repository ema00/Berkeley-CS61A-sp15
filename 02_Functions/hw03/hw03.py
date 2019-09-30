HW_SOURCE_FILE = 'hw03.py'

#############
# Questions #
#############

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g', ['While', 'For'])
    True
    """
    if n <= 3:
        return n
    else:
        return g(n - 1) + 2 * g(n - 2) + 3 * g(n - 3)


def g_iter(n):
    """Return the value of G(n), computed iteratively.

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'g_iter', ['Recursion'])
    True
    """
    g = 0
    g1, g2, g3 = 1, 2, 3
    g_3, g_2, g_1 = g1, g2, g3
    if n == 1: g = g1
    elif n == 2: g = g2
    elif n == 3: g = g3
    for term in range(4, n + 1):
        g = g_1 + 2 * g_2 + 3 * g_3     # g = g(n-1) + 2 * g(n-2) + 3 * g(n-3)
        g_3, g_2, g_1 = g_2, g_1, g     # g(n-3) = g(n-2), g(n-2) = g(n-1) ,...
    return g


def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(2734)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """
    if k == 0:
        return False
    else:
        return  abs(k) % 10 == 7 or has_seven(k // 10)


def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    def is_bounce(step, elem):
        return step % 7 == 0 or has_seven(step)

    def move_up(step, elem, end):
        if step == end:
            return elem
        else:
            if is_bounce(step, elem):
                return move_down(step + 1, elem - 1, end)
            else:
                return move_up(step + 1, elem + 1, end)

    def move_down(step, elem, end):
        if step == end:
            return elem
        else:
            if is_bounce(step, elem):
                return move_up(step + 1, elem + 1, end)
            else:
                return move_down(step + 1, elem - 1, end)

    return move_up(1, 1, n)


def count_change(amount):
    """Return the number of ways to make change for amount.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    """
    coins = [pow(2, x) for x in range(0, amount//2 + 1) if pow(2, x) <= amount]

    def count_rec(amount, index):
        if index < 0:
            return 0
        if amount < 0:
            return 0
        if amount == 0:
            return 1
        else:
            with_coin = count_rec(amount - coins[index], index)
            without_coin = count_rec(amount, index - 1)
            return with_coin + without_coin

    return count_rec(amount, len(coins) - 1)


def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)


def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"

    def move(n, start, aux, end):
        if n == 1:
            print_move(start, end)
        else:
            move(n - 1, start, end, aux)
            move(1, start, aux, end)
            move(n - 1, aux, start, end)

    aux = [x for x in range(1,4) if (x != start and x != end)][0]
    move(n, start, aux, end)


def flatten(lst):
    """Returns a flattened version of lst.

    >>> flatten([1, 2, 3])     # normal list
    [1, 2, 3]
    >>> x = [1, [2, 3], 4]      # deep list
    >>> flatten(x)
    [1, 2, 3, 4]
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> flatten(x)
    [1, 1, 1, 1, 1, 1]
    """
    def is_list(item):
        return type(item) == list

    result = []
    i = 0
    while i < len(lst):
        if not is_list(lst[i]):
            result = result + [lst[i]]
        else:
            result = result + flatten(lst[i])
        i = i + 1
    return result
#flatten([[[-2, -1, [0]], 1], 2, 3, [4, 5, 6], 7, [8, 9, [10, 11]]])


def merge(lst1, lst2):
    """Merges two sorted lists.

    >>> merge([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge([], [2, 4, 6])
    [2, 4, 6]
    >>> merge([1, 2, 3], [])
    [1, 2, 3]
    >>> merge([5, 7], [2, 4, 6])
    [2, 4, 5, 6, 7]
    """
    len1, len2 = len(lst1), len(lst2)
    i, i1, i2 = 0, 0, 0
    lst = []
    while i < (len1 + len2):
        if i1 == len1:                  # list1 empty
            elem = lst2[i2]
            i2 = i2 + 1
        elif i2 == len2:                # list2 empty
            elem = lst1[i1]
            i1 = i1 + 1
        elif lst1[i1] < lst2[i2]:       # elem1 < elem2
            elem = lst1[i1]
            i1 = i1 + 1
        else:                           # elem1 > elem2
            elem = lst2[i2]
            i2 = i2 + 1
        lst = lst + [elem]
        i = i + 1
    return lst


def mergesort(seq):
    """Mergesort algorithm.

    >>> mergesort([4, 2, 5, 2, 1])
    [1, 2, 2, 4, 5]
    >>> mergesort([])     # sorting an empty list
    []
    >>> mergesort([1])   # sorting a one-element list
    [1]
    """
    if len(seq) <= 1:
        return seq
    else:
        middle = len(seq) // 2
        half1 = mergesort(seq[:middle])
        half2 = mergesort(seq[middle:])
        return merge(half1, half2)
