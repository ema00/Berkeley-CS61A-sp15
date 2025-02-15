from operator import add, sub

""" For testing use:
python3 ok -q a_plus_abs_b
python3 ok -q two_of_three
python3 ok -q largest_factor
python3 -i hw01.py
python3 ok -q hailstone
"""


def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs.

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    """
    if b < 0:
        f = sub
    else:
        f = add
    return f(a, b)

def two_of_three(a, b, c):
    """Return x*x + y*y, where x and y are the two largest members of the
    positive numbers a, b, and c.

    >>> two_of_three(1, 2, 3)
    13
    >>> two_of_three(5, 3, 1)
    34
    >>> two_of_three(10, 2, 8)
    164
    >>> two_of_three(5, 5, 5)
    50
    """
    return a * a + b * b + c * c - min(a, b, c) * min(a, b, c)

def largest_factor(n):
    """Return the largest factor of n that is smaller than n.

    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    i = 1
    result = 1
    while i <= n // 2:
        if n % i == 0:
            result = i
        i = i + 1
    return result

def if_function(condition, true_result, false_result):
    """Return true_result if condition is a true value, and
    false_result otherwise.

    >>> if_function(True, 2, 3)
    2
    >>> if_function(False, 2, 3)
    3
    >>> if_function(3==2, 3+2, 3-2)
    1
    >>> if_function(3>2, 3+2, 3-2)
    5
    """
    if condition:
        return true_result
    else:
        return false_result

"""Despite the doctests above, the function if_function does not do the same
thing as an if statement in all cases. To prove this fact, write functions c, t,
and f such that with_if_statement returns the number 1, but with_if_function
does not (it can do anything else)."""

def with_if_statement():
    """
    >>> with_if_statement()
    1
    """
    if c():
        return t()
    else:
        return f()

def with_if_function():
    return if_function(c(), t(), f())

def c():
    return True

def t():
    return 1

def f():
    return 1 / 0

def hailstone(n):
    """Print the hailstone sequence starting at n and return its
    length.

    Steps:
    1- Pick a positive integer n as the start.
    2- If n is even, divide it by 2.
    3- If n is odd, multiply it by 3 and add 1.
    4- Continue this process until n is 1.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
    def is_even(n):
        return n % 2 == 0

    length = 1
    while True:
        print(n)
        if n == 1:
            break
        if is_even(n):
            n = n // 2
        else:
            n = 3 * n + 1
        length += 1
    return length
