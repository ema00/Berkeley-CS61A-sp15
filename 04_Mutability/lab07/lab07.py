# Control
def same_hailstone(a, b):
    """Return whether a and b are both members of the same hailstone
    sequence.

    >>> same_hailstone(10, 16) # 10, 5, 16, 8, 4, 2, 1
    True
    >>> same_hailstone(16, 10) # order doesn't matter
    True
    >>> result = same_hailstone(3, 19) # return, don't print
    >>> result
    False

    """
    def hailstone(n):
        seq = [n]
        i = n
        while True:
            if i % 2 == 0:
                i = i // 2
            else:
                i = i * 3 + 1
            seq.append(i)
            if i == 1: break
        return seq

    hailstone_a = hailstone(a)
    hailstone_b = hailstone(b)
    return a in hailstone_b or b in hailstone_a


def amicable(n):
    """Return the smallest amicable number greater than positive integer n.

    Every amicable number x has a buddy y different from x, such that
    the sum of the proper divisors of x equals y, and
    the sum of the proper divisors of y equals x.

    For example, 220 and 284 are both amicable because
    1 + 2 + 4 + 5 + 10 + 11 + 20 + 22 + 44 + 55 + 110 is 284, and
    1 + 2 + 4 + 71 + 142 is 220

    >>> amicable(5)
    220
    >>> amicable(220)
    284
    >>> amicable(284)
    1184
    >>> r = amicable(5000)
    >>> r
    5020

    """
    def sum_divisors(x):
        total = 0
        for divisor in range(1, x // 2 + 1):
            if x % divisor == 0:
                total += divisor
        return total

    n = n + 1
    while True:
        m = sum_divisors(n)
        if m != n and n == sum_divisors(m):
            return n
        n = n + 1


# HOF
def cycle(f1, f2, f3):
    """Returns a function that is itself a higher-order function.

    >>> def add1(x):
    ...     return x + 1
    >>> def times2(x):
    ...     return x * 2
    >>> def add3(x):
    ...     return x + 3
    >>> my_cycle = cycle(add1, times2, add3)
    >>> identity = my_cycle(0)
    >>> identity(5)
    5
    >>> add_one_then_double = my_cycle(2)
    >>> add_one_then_double(1)
    4
    >>> do_all_functions = my_cycle(3)
    >>> do_all_functions(2)
    9
    >>> do_more_than_a_cycle = my_cycle(4)
    >>> do_more_than_a_cycle(2)
    10
    >>> do_two_cycles = my_cycle(6)
    >>> do_two_cycles(1)
    19
    """
    def f(n):
        def g(x):
            y = x
            for i in range(1, n + 1):
                if i % 3 == 1:
                    y = f1(y)
                elif i % 3 == 2:
                    y = f2(y)
                else:
                    y = f3(y)
            return y

        return g

    return f


# Recursion
def part(n):
    """Return the number of partitions of positive integer n.

    >>> part(5)
    7
    >>> part(10)
    42
    >>> part(15)
    176
    >>> part(20)
    627
    """
    def count_part(elements, elem):
        if elem == 0:
            return 0
        elif elements < 0:
            return 0
        elif elements == 0:
            return 1
        else:
            return count_part(elements - elem, elem) + count_part(elements, elem - 1)

    return count_part(n, n)


def knapsack(weights, values, c):
    """
    >>> w = [2, 6, 3, 3]
    >>> v = [1, 5, 3, 3]
    >>> knapsack(w, v, 6)
    6
    """
    def generate(index, wghts, current):
        remainder = c - sum([weights[i] for i in current])
        if remainder == 0:
            combinations.append(current[:])
            return
        else:
            w = wghts[:index - 1]
            if remainder >= 0 and index >= 0:
                if not index in current:
                    generate(index, w, current[:] + [index])
                generate(index - 1, w, current[:])
            return

    combinations = []
    value_list = []
    generate(len(weights) - 1, weights, [])
    for combination in combinations:
        value = [values[c] for c in combination]
        value_list = value_list + [sum(value)]
    return max(value_list)



# Trees
# Tree definition

def tree(root, branches=[]):
    """Construct a tree with the given root value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [root] + list(branches)

def root(tree):
    """Return the root value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(root(t)))
    for b in branches(t):
        print_tree(b, indent + 1)


def sprout_leaves(t, vals):
    """Sprout new leaves containing the data in vals at each leaf in
    the original tree t and return the resulting tree.

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    if is_leaf(t):
        subtrees = [tree(v) for v in vals]
        return tree(root(t), subtrees)
    else:
        return tree(root(t), [sprout_leaves(b, vals) for b in branches(t)])


# Lists
def group(seq):
    """Divide a sequence of at least 12 elements into groups of 4 or
    5. Groups of 5 will be at the end. Returns a list of sequences, each
    corresponding to a group.

    >>> group(range(14))
    [range(0, 4), range(4, 9), range(9, 14)]
    >>> group(list(range(17)))
    [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15, 16]]
    """
    num = len(seq)
    assert num >= 12
    if num == 12 or num == 13:          # 444 or 445
        return [seq[:4]] + [seq[4:8]] + [seq[8:]]
    elif num == 14 or num == 15:        # 455
        return [seq[:4]] + [seq[4:9]] + [seq[9:]]
    elif num == 14 or num == 15:        # 555
        return [seq[:5]] + [seq[5:10]] + [seq[10:]]
    else:
        return [seq[:4]] + group(seq[4:])


def deep_len(lst):
    """Returns the deep length of the list.

    >>> deep_len([1, 2, 3])     # normal list
    3
    >>> x = [1, [2, 3], 4]      # deep list
    >>> deep_len(x)
    4
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> deep_len(x)
    6
    >>> x = []
    >>> for i in range(100):
    ...     x = [x] + [i]       # very deep list
    ...
    >>> deep_len(x)
    100
    """
    """
    # ITERATIVE SOLUTION
    length = 0
    for elem in lst:
        if type(elem) == list:
            length += deep_len(elem)
        else:
            length += 1
    return length"""
    # RECURSIVE SOLUTION
    if type(lst) == list and len(lst) == 0:
        return 0
    first = lst[0]
    if type(first) != list:
        return 1 + deep_len(lst[1:])
    else:
        return deep_len(first) + deep_len(lst[1:])


# Linked Lists
# Linked List abstraction

empty = 'X'

def link(first, rest=empty):
    assert is_link(rest), 'rest must be a linked list.'
    return [first, rest]

def first(lnk):
    assert is_link(lnk), 'first only applies to linked lists.'
    assert lnk != empty, 'empty linked list has no first element.'
    return lnk[0]

def rest(lnk):
    assert is_link(lnk), 'rest only applies to linked lists.'
    assert lnk != empty, 'empty linked list has no rest.'
    return lnk[1]

def is_link(lnk):
    return lnk == empty or \
        type(lnk) == list and len(lnk) == 2 and is_link(lnk[1])


# Useful print_link function, used for testing.

def print_link(lnk):
    """Prints out a non-deep linked list."""
    line = ''
    while lnk != empty:
        if line:
            line += ' '
        line += str(first(lnk))
        lnk = rest(lnk)
    print('<{}>'.format(line))


def is_empty(lnk):
	return lnk == empty


def deep_reverse(lnk):
    """Return a reversed version of a possibly deep linked list lnk.

    >>> print_link(deep_reverse(empty))
    <>
    >>> print_link(deep_reverse(link(1, link(2, empty))))
    <2 1>

    >>> deep = link(1, link(link(2, link(3, empty)), empty))
    >>> deep_reversed = deep_reverse(deep)
    >>> print_link(first(deep_reversed))
    <3 2>
    >>> first(rest(deep_reversed))
    1
    >>> rest(rest(deep_reversed)) == empty
    True

    """
    def deep_revert(direct, reversed):
        if is_empty(direct):
            return reversed
        else:
            frst = first(direct)
            if is_link(frst):
                frst = deep_revert(frst, empty)
            return deep_revert(rest(direct), link(frst, reversed))

    return deep_revert(lnk, empty)



def reverse(lnk):
    """
    Reverse linked list.
    This was done in order to test a "flat" reverse before doing deep reverse.

    >>> print_link(reverse(link(1, link(2, empty))))
    <2 1>
    """
    def revert(direct, reversed):
        if is_empty(direct):
            return reversed
        else:
            return revert(rest(direct), link(first(direct), reversed))

    return revert(lnk, empty)
