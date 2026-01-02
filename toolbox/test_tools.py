from functools import wraps
def defntest(test_fn, f=None):
    @wraps(test_fn)
    def ret():
        test_cases = test_fn()
        for 
