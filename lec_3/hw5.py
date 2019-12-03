from __future__ import division

import math
from functools import reduce
from time import time

import fibonacci


def profiling(counter_name):
    def decorator(f):
        def wrapper(*args, **kwargs):
            counter = globals()[counter_name]
            counter['amount'] += 1
            if not counter['running']:
                counter['running'] = True
                ts = time()
                result = f(*args, **kwargs)
                te = time()
                time_delta = te - ts
                counter['time'] += time_delta
                counter['running'] = False
            else:
                result = f(*args, **kwargs)
            return result
        return wrapper
    return decorator


@profiling('recur_counter')
def fibonacci_recur(n):
    if n in [1, 2]:
        return 1
    else:
        return fibonacci_recur(n - 1) + fibonacci_recur(n - 2)


@profiling('recur_with_memory_counter')
def fibonacci_recur_with_memory(n, fib={1: 1, 2: 1}):
    if n not in fib:
        fib[n] = fibonacci_recur_with_memory(
            n-1, fib) + fibonacci_recur_with_memory(n-2, fib)
    return fib[n]


@profiling('list_counter')
def fibonacci_list(n):
    if n < 3:
        return 1
    else:
        fib = [1, 1]
        i = 2
        while i < n:
            fib.append(fib[i-1]+fib[i-2])
            i += 1
        return fib.pop()


def gen_fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


@profiling('gen_counter')
def fibonacci_gen(n):
    return list(gen_fibonacci(n)).pop()


@profiling('lambda_counter')
def fibonacci_lambda(n):
    return reduce(
        lambda fib, n: [fib[1], fib[0]+fib[1]], range(n-1), [1, 1])[0]


@profiling('lib_counter')
def fibonacci_lib(n):
    return fibonacci.fibo(n)


def matrix_mul(a, b):
    return [[
        a[0][0] * b[0][0] + a[0][1] * b[1][0],
        a[0][0] * b[0][1] + a[0][1] * b[1][1]
    ], [
        a[1][0] * b[0][0] + a[1][1] * b[1][0],
        a[1][0] * b[0][1] + a[1][1] * b[1][1]
    ]]


def power(p):
    m = [[1, 1], [1, 0]]
    t = [[1, 0], [0, 1]]
    while p:
        if p % 2:
            t = matrix_mul(t, m)
        m = matrix_mul(m, m)
        p //= 2
    return t


@profiling('matrix_counter')
def fibonacci_matrix(n):
    return power(n)[1][0]


@profiling('binet_counter')
def fibonacci_binet(n):
    sqrt5 = math.sqrt(5)
    phi = (sqrt5 + 1) / 2
    return int(phi ** n / sqrt5 + 0.5)


# n = 30: time of all functions except fibonacci_recur is equal 0
#         time of fibonacci_recur is 0.58845
#         fibonacci_recur is eliminated
#
# n = 500: correct value: 139423224561 697880139724382870407283950070256587...
#  fibonacci_binet value: 139423224561 700228711116466856628305532793116368...
#         fibonacci_binet is eliminated
#
# n = 1001: fibonacci_recur_with_memory: RecursionError: maximum recursion
#           depth exceeded while calling a Python object
#           fibonacci_recur_with_memory is eliminated
#               (besides she had the worst time at n = 500)
#
# n = 100000:  results:
#              fibonacci_matrix time:  0.011933088302612305   -winner
#              fibonacci_lib time:     0.08556795120239258
#              fibonacci_lambda time:  0.09772157669067383
#              fibonacci_gen time:     0.30317163467407227
#              fibonacci_list time:    0.3231692314147949


if __name__ == '__main__':
    recur_counter = {'amount': 0, 'running': False, 'time': 0}
    recur_with_memory_counter = {'amount': 0, 'running': False, 'time': 0}
    list_counter = {'amount': 0, 'running': False, 'time': 0}
    gen_counter = {'amount': 0, 'running': False, 'time': 0}
    lambda_counter = {'amount': 0, 'running': False, 'time': 0}
    lib_counter = {'amount': 0, 'running': False, 'time': 0}
    matrix_counter = {'amount': 0, 'running': False, 'time': 0}
    binet_counter = {'amount': 0, 'running': False, 'time': 0}
