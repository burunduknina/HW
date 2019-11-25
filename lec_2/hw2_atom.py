def atom(value=None):
    current_value = value

    def get_value():
        return current_value

    def set_value(new_value):
        nonlocal current_value
        current_value = new_value
        return current_value

    def process_value(*functions):
        nonlocal current_value
        for func in functions:
            current_value = func(current_value)
        return current_value

    def delete_value():
        nonlocal current_value
        current_value = None
    return get_value, set_value, process_value, delete_value


if __name__ == '__main__':
    test = 5
    test_gv, test_sv, test_pv, test_dv = atom(test)
    assert(test_gv() == 5)
    assert(test_sv(-6) == -6)
    assert(test_pv(abs, str) == '6')
    assert(test_dv() is None)
