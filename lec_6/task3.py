""""
Реализовать контекстный менеджер, который подавляет переданные исключения
with Suppressor(ZeroDivisionError):
    1/0
print("It's fine")
"""


class Suppressor:
    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return isinstance(exc_value, self.exceptions)


if __name__ == "__main__":
    with Suppressor(ZeroDivisionError):
        1 / 0
    print("It's fine")
