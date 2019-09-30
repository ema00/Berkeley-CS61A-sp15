from lab03 import *

# Q4
def skip_mul(n):
    """Return the product of n * (n - 2) * (n - 4) * ...

    >>> skip_mul(5) # 5 * 3 * 1
    15
    >>> skip_mul(8) # 8 * 6 * 4 * 2
    384
    """
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return n * skip_mul(n - 2)


# Q5
def count_up(n):
    """Print out all numbers up to and including n in ascending order.

    >>> count_up(5)
    1
    2
    3
    4
    5
    """
    def counter(i):
        print(i)
        if i == n:
            return
        else:
            counter(i + 1)
    counter(1)


# Q6
def is_prime(n):
    """Returns True if n is a prime number and False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """
    def is_prime_rec(n, d):
        if d > (n ** 0.5):
            return True
        else:
            return n % d != 0 and is_prime_rec(n, d + 1)

    return is_prime_rec(n, 2)


# Q7
def interleaved_sum(n, odd_term, even_term):
    """Compute the sum odd_term(1) + even_term(2) + odd_term(3) + ..., up
    to n.

    >>> # 1 + 2^2 + 3 + 4^2 + 5
    ... interleaved_sum(5, lambda x: x, lambda x: x*x)
    29
    """
    # DAMN MUTUAL RECURSION !!!!
    def sum_odd(i):
        if i > n:
            return 0
        else:
            return odd_term(i) + sum_even(i + 1)

    def sum_even(i):
        if i > n:
            return 0
        else:
            return even_term(i) + sum_odd(i + 1)

    return sum_odd(1)


# Q8
def ten_pairs(n):
    """Return the number of ten-pairs within positive integer n.

    >>> ten_pairs(7823952)
    3
    >>> ten_pairs(55055)
    6
    >>> ten_pairs(9641469)
    6
    """
    def count_digit(num, dig):
        count = 0
        while num > 0:
            if num % 10 == dig:
                count = count + 1
            num = num // 10
        return count

    if n < 10:
        return 0
    else:
        return count_digit(n // 10, 10 - n % 10) + ten_pairs(n // 10)
