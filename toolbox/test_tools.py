from dataclasses import dataclass, field
from functools import wraps
from typing import Callable


@dataclass
class FuncParams:
    args: list | tuple = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)


@dataclass
class ExpectedException:
    exception: type[Exception] = Exception
    message: str | None = None


type Returns[T] = Callable[..., T]

type FunctionArgs = list | tuple | dict | FuncParams
type ExpectedOutput[T] = T | ExpectedException
type TestCase[T] = tuple[FunctionArgs, ExpectedOutput[T]]
type TestCases[T] = list[TestCase[T]]
type TestCaseFunction[T] = Callable[[], TestCases[T]]


def _apply[T](f: Returns[T], args: FunctionArgs) -> T:
    match args:
        case tuple() | list():
            return f(*args)
        case dict():
            return f(**args)
        case FuncParams(args=a, kwargs=kw):
            return f(*a, **kw)
        case _:
            raise ValueError("Arguments must be tuple, list, dict, or FuncParams")


def _run_test_case[T](f: Returns[T], args: FunctionArgs, expected: ExpectedOutput[T]):
    match expected:
        case ExpectedException(exception=exc, message=msg):
            try:
                result = _apply(f, args)
                assert False, f"Test failed: {args} did not raise {exc}"
            except Exception as e:
                assert isinstance(
                    e, exc
                ), f"Test failed: {args} raised {type(e)}, expected {exc}"
                if msg:
                    assert msg in str(
                        e
                    ), f"Test failed: {args} raised {e}, expected message containing '{msg}'"
        case _:
            # Regular return value
            result = _apply(f, args)
            assert (
                result == expected
            ), f"Test failed: {args} => {result}, expected {expected}"


def func_test_cases[T](f: Returns[T]) -> Callable:
    def decorator(test_fn: TestCaseFunction[T]) -> Callable:
        @wraps(test_fn)
        def wrapper():
            test_cases = test_fn()
            for args, expected in test_cases:
                _run_test_case(f, args, expected)

        return wrapper

    return decorator
