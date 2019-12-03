def applydecorator(func):
    def wrapper(f):
        def inner_wrapper(*args, **kwargs):
            return func(f, *args, *kwargs)
        return inner_wrapper
    return wrapper


@applydecorator
def saymyname(f, *args, **kwargs):
    print('Name is', f.__name__)
    return f(*args, **kwargs)


@saymyname
def foo(*whatever):
    return whatever


if __name__ == '__main__':
    print(*(foo(40, 2)))
