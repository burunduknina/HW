from functools import reduce


def problem6():
    """
    Sum square difference
    """
    return sum(range(1, 101)) ** 2 - sum([i ** 2 for i in range(1, 101)])


def problem9():
    """
    Special Pythagorean triplet
    """
    return [
        [a, b, 1000-a-b]
        for a in range(1, 335) for b in range(1, 1000-a)
        if a ** 2 + b ** 2 == (1000-a-b) ** 2
    ]


def problem40():
    """
    Champernowne's constant
    """
    return reduce(
        lambda i, j: i * j, [int(''.join([str(i) for i in range(0, 200000)])[
                                     10 ** i]) for i in range(0, 7)])


def problem48():
    """
    Self powers
    """
    return sum([i ** i for i in range(1, 1001)]) % 10 ** 10
