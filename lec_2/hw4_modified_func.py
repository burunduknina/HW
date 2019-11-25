import inspect
from lec_2.hw1_letters_range import letters_range


def modified_func(func, *fixated_args, **fixated_kwargs):
    def wrapped(*args, **kwargs):
        nonlocal fixated_args
        func_args = args + fixated_args
        func_kwargs = fixated_kwargs.copy()
        for kwarg, value in kwargs.items():
            func_kwargs[kwarg] = value
        return func(*func_args, **func_kwargs)
    wrapped.__name__ = f'func_{func.__name__}'
    try:
        code = inspect.getsource(func)
    except TypeError:
        code = 'Source code cannot be retrieved.'
    args = inspect.signature(
        wrapped).bind(*fixated_args, **fixated_kwargs).arguments
    doc = f'A func implementation of {func.__name__}'\
        f'with pre-applied arguments being:\n'\
        f'fixated_args: {args.get("args")}\n'\
        f'fixated_kwargs: {args.get("kwargs")}\n'\
        f'source_code:\n'\
        f'{code}'
    wrapped.__doc__ = doc

    return wrapped


if __name__ == '__main__':
    letters_range_plus = modified_func(letters_range, 'c', stop='k', step=2)
    assert letters_range_plus.__name__ == 'func_letters_range'
    assert letters_range_plus.__doc__.find('def letters_range') != -1
    assert letters_range_plus(step=3) == ['c', 'f', 'i']
    min_plus = modified_func(min, default=15)
    assert min_plus.__name__ == 'func_min'
    assert min_plus.__doc__.find('Source code cannot be retrieved.') != -1
    assert min_plus([]) == 15
    assert min_plus([1, 2]) == 1
