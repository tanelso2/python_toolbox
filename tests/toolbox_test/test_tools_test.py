from toolbox.test_tools import func_test_cases, ExpectedException, FuncParams


def add(x, y):
    return x + y


@func_test_cases(add)
def test_add():
    return [
        ((1, 2), 3),
        ((-1, 1), 0),
        ((0, 0), 0),
    ]


def divide(x, y):
    return x / y


@func_test_cases(divide)
def test_divide():
    return [
        ((4, 2), 2),
        ((1, 0), ExpectedException(ZeroDivisionError)),
        ({"x": 9, "y": 3}, 3),
        (FuncParams(args=[10, 2]), 5),
        (
            FuncParams(args=[5], kwargs={"y": 0}),
            ExpectedException(ZeroDivisionError, "division by zero"),
        ),
    ]


@func_test_cases(divide)
def test_divide_floats():
    return [
        ((5.0, 2.0), 2.5),
        ((7.5, 2.5), 3.0),
    ]
