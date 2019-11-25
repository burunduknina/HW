def make_it_count(func, counter_name):
    def func_plus(*args, **kwargs):
        globals()[counter_name] += 1
        return func(*args, **kwargs)
    return func_plus


if __name__ == '__main__':
    counter = 0
    sum_count = make_it_count(sum, 'counter')
    isinstance_count = make_it_count(isinstance, 'counter')
    assert(sum_count([-4, 3]) == -1 and counter == 1)
    assert(isinstance_count(5, int) and counter == 2)
