def is_armstrong(number):
    return sum(list(map(lambda i: i ** len(str(number)), [
        int(elem) for elem in str(number)]))) == number


if __name__ == '__main__':
    assert is_armstrong(153) is True, 'Число Армстронга'
    assert is_armstrong(10) is False, 'Не число Армстронга'
