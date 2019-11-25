def letters_range(start, stop=None, step=1, **kwargs):
    if not stop:
        stop, start, step = start, 'a', 1
    letters = [chr(i) for i in range(97, 123)]
    for key in kwargs:
        letters[letters.index(key)] = str(kwargs[key])
    return [letters[i]
            for i in range(letters.index(start), letters.index(stop), step)]


if __name__ == '__main__':
    assert(letters_range('b', 'w', 2) == ['b', 'd', 'f', 'h', 'j', 'l', 'n',
                                          'p', 'r', 't', 'v'])
    assert(letters_range('g') == ['a', 'b', 'c', 'd', 'e', 'f'])
    assert(letters_range('g', 'p') == ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                       'o'])
    assert(letters_range(
        'g', 'p', **{'l': 7, 'o': 0}) == [
        'g', 'h', 'i', 'j', 'k', '7', 'm', 'n', '0'
    ])
    assert(letters_range('p', 'g', -2) == ['p', 'n', 'l', 'j', 'h'])
    assert(letters_range('a') == [])
