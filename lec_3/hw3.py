def collatz_steps(n):
    def inner_steps(number, steps):
        return steps if number == 1 else inner_steps(
            number // 2, steps + 1) if number % 2 == 0 else inner_steps(
            number * 3 + 1, steps + 1)
    if isinstance(n, int) and n > 0:
        return inner_steps(n, 0)
    else:
        assert ValueError('N should be a natural number')


if __name__ == '__main__':
    assert collatz_steps(16) == 4
    assert collatz_steps(12) == 9
    assert collatz_steps(1000000) == 152
