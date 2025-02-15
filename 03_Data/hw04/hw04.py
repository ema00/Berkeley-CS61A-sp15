HW_SOURCE_FILE = 'hw04.py'

################
# Linked Lists #
################

# Linked List definition

empty = 'empty'  # The empty linked list

def link(first, rest=empty):
    """Construct a linked list from its first element and the rest."""
    assert is_link(rest), 'rest must be a linked list.'
    return [first, rest]

def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s), 'first only applies to linked lists.'
    assert s is not empty, 'empty linked list has no first element.'
    return s[0]

def rest(s):
    """Return the rest of the elements of a linked list s."""
    assert is_link(s), 'rest only applies to linked lists.'
    assert s is not empty, 'empty linked list has no rest.'
    return s[1]

def is_link(s):
    """Returns True if s is a linked list, and False otherwise."""
    return s is empty or (type(s) == list and len(s) == 2 and is_link(s[1]))

def is_empty(s):
    """Returns True if s is the empty linked list, and False otherwise."""
    return s is empty

def print_link(s):
    """Print elements of a linked list s.

    >>> s = link(1, link(2, link(3, empty)))
    >>> print_link(s)
    1 2 3
    """
    line = ''
    while s != empty:
        if line:
            line += ' '
        line += str(first(s))
        s = rest(s)
    print(line)


def change(lst, s, t):
    """Returns a link matching lst but with all instances of s (if any)
    replaced by t.

    >>> lst = link(1, link(2, link(3)))
    >>> new = change(lst, 3, 1)
    >>> print_link(new)
    1 2 1
    >>> newer = change(new, 1, 2)
    >>> print_link(newer)
    2 2 2
    >>> newest = change(newer, 5, 1)
    >>> print_link(newest)
    2 2 2
    """
    if is_empty(lst):
        return lst
    else:
        if first(lst) == s:
            return link(t, change(rest(lst), s, t))
        else:
            return link(first(lst), change(rest(lst), s, t))


def reverse_iterative(s):
    """Return a reversed version of a linked list s.

    >>> primes = link(2, link(3, link(5, link(7, empty))))
    >>> reversed_primes = reverse_iterative(primes)
    >>> print_link(reversed_primes)
    7 5 3 2
    """
    result = empty
    lst = s
    while not is_empty(lst):
        head = first(lst)
        lst = rest(lst)
        result = link(head, result)
    return result


def reverse_recursive(s):
    """Return a reversed version of a linked list s.

    >>> primes = link(2, link(3, link(5, link(7, empty))))
    >>> reversed_primes = reverse_recursive(primes)
    >>> print_link(reversed_primes)
    7 5 3 2
    """
    def reverse(s, r):
        if is_empty(s):
            return r
        else:
            return reverse(rest(s), link(first(s), r))

    lst = s
    return reverse(lst, empty)


def insert(lst, item, index):
    """Returns a link matching lst but with the given item inserted at the
    specified index. If the index is greater than the current length, the item
    is appended to the end of the list.

    >>> lst = link(1, link(2, link(3)))
    >>> new = insert(lst, 9001, 1)
    >>> print_link(new)
    1 9001 2 3
    >>> newer = insert(new, 9002, 15)
    >>> print_link(newer)
    1 9001 2 3 9002
    """
    if is_empty(lst):
        return link(item, empty)        # insert at end if index > length
    else:
        if index == 0:
            return link(item, lst)
        else:
            return link(first(lst), insert(rest(lst), item, index - 1))


#########
# Trees #
#########

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

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(root(t), [copy_tree(b) for b in branches(t)])


def acorn_finder(t):
    """Returns True if t contains a node with the value 'acorn' and
    False otherwise.

    >>> scrat = tree('acorn')
    >>> acorn_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('acorn')]), tree('branch2')])
    >>> acorn_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> acorn_finder(numbers)
    False
    """
    def has_acorn(t):
        return root(t) == "acorn"

    if is_leaf(t):
        return has_acorn(t)
    else:
        subtrees_have_acorns = [acorn_finder(t) for t in branches(t)]
        return has_acorn(t) or any(subtrees_have_acorns)


def same_shape(t1, t2):
    """Return True if t1 is indentical in shape to t2.

    >>> test_tree1 = tree(1, [tree(2), tree(3)])
    >>> test_tree2 = tree(4, [tree(5), tree(6)])
    >>> test_tree3 = tree(1,
    ...                   [tree(2,
    ...                         [tree(3)])])
    >>> test_tree4 = tree(4,
    ...                   [tree(5,
    ...                         [tree(6)])])
    >>> same_shape(test_tree1, test_tree2)
    True
    >>> same_shape(test_tree3, test_tree4)
    True
    >>> same_shape(test_tree2, test_tree4)
    False
    """
    if is_leaf(t1):
        return is_leaf(t2)
    else:
        branches1 = branches(t1)
        branches2 = branches(t2)
        if len(branches1) != len(branches2):
            return False
        else:
            are_equal_subtrees = [same_shape(branches1[i], branches2[i]) for i in range(len(branches1))]
            return all(are_equal_subtrees)


def add_trees(t1, t2):
    """
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), \
    tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    if is_leaf(t1):                             # base case: sum leaf values
        if is_leaf(t2):
            return tree(root(t1) + root(t2))
        elif is_tree(t2):
            return tree(root(t1) + root(t2), copy_tree(branches(t2)))
        else:
            return copy_tree(t1)
    else:                                       # induction step: sum branches
        root_value = root(t1) + root(t2)
        if len(branches(t1)) < len(branches(t2)):
            shortest = branches(t1)
            longest = branches(t2)
        else:
            shortest = branches(t2)
            longest = branches(t1)
        branches1 = [add_trees(shortest[i], longest[i]) for i in range(len(shortest))]
        branches2 = [copy_tree(longest[i]) for i in range(len(shortest), len(longest))]
        return tree(root_value, branches1 + branches2)


###########
# Mobiles #
###########

def mobile(left, right):
    """Construct a mobile from a left side and a right side."""
    return tree(None, [left, right])

def sides(m):
    """Select the sides of a mobile."""
    return branches(m)

def side(length, mobile_or_weight):
    """Construct a side: a length of rod with a mobile or weight at the end."""
    return tree(length, [mobile_or_weight])

def length(s):
    """Select the length of a side."""
    return root(s)

def end(s):
    """Select the mobile or weight hanging at the end of a side."""
    return branches(s)[0]

def weight(size):
    """Construct a weight of some size."""
    assert size > 0
    "*** YOUR CODE HERE ***"
    return tree(size)

def size(w):
    """Select the size of a weight."""
    "*** YOUR CODE HERE ***"
    return root(w)

def is_weight(w):
    """Whether w is a weight, not a mobile."""
    "*** YOUR CODE HERE ***"
    return size(w) != None

def examples():
    t = mobile(side(1, weight(2)),
               side(2, weight(1)))
    u = mobile(side(5, weight(1)),
               side(1, mobile(side(2, weight(3)),
                              side(3, weight(2)))))
    v = mobile(side(4, t), side(2, u))
    return (t, u, v)


def total_weight(m):
    """Return the total weight of m, a weight or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    """
    if is_weight(m):
        return size(m)
    else:
        return sum([total_weight(end(s)) for s in sides(m)])


def balanced(m):
    """Return whether m is balanced.
    A mobile is said to be balanced if the torque applied by
    its left side is equal to that applied by its right side
    (that is, if the length of the left rod multiplied by the
    total weight hanging from that rod is equal to the
    corresponding product for the right side).

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(side(3, t), side(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(side(1, v), side(1, w)))
    False
    >>> balanced(mobile(side(1, w), side(1, v)))
    False
    """
    if is_weight(m):
        return True
    else:
        left = sides(m)[0]
        right = sides(m)[1]
        are_equal_torques = (length(left) * total_weight(end(left)) ==
            length(right) * total_weight(end(right)))
        return are_equal_torques and balanced(end(left)) and balanced(end(right))
