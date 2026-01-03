from dataclasses import dataclass, field
from functools import wraps


@dataclass
class FuncParams:
    args: list | tuple = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)


@dataclass
class ExpectedException:
    exception: type = Exception
    message: str | None = None


def _get_tested_function(test_fn):
    name = test_fn.__name__
    if name.startswith("test_"):
        name = name[5:]
    globals = test_fn.__globals__
    return globals[name]


def _apply(f, args):
    match args:
        case tuple() | list():
            return f(*args)
        case dict():
            return f(**args)
        case FuncParams(args=a, kwargs=kw):
            return f(*a, **kw)
        case _:
            raise ValueError("Arguments must be tuple, list, dict, or FuncParams")


def _run_test_case(f, args, expected):
    match expected:
        case ExpectedException(exception=exc, message=msg):
            try:
                result = _apply(f, args)
                assert False, f"Test failed: {args} did not raise {exc}"
            except exc as e:
                if msg is not None:
                    assert msg in str(
                        e
                    ), f"Test failed: {args} raised {e}, expected message containing '{msg}'"
                else:
                    pass  # Exception raised as expected
        case _:
            # Regular return value
            result = _apply(f, args)
            assert (
                result == expected
            ), f"Test failed: {args} => {result}, expected {expected}"


def _run_test_cases(f, test_fn):
    test_cases = test_fn()
    for args, expected in test_cases:
        _run_test_case(f, args, expected)


def _wrap_test_case_fn(test_fn, f=None):
    @wraps(test_fn)
    def wrapper():
        func = f if f is not None else _get_tested_function(test_fn)
        _run_test_cases(func, test_fn)

    return wrapper


def fn_test(f=None):
    def decorator(test_fn):
        return _wrap_test_case_fn(test_fn, f=f)

    return decorator
