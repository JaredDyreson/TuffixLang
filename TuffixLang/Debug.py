import inspect

# source of where I found it, did not write it but very helpful
# https://stackoverflow.com/questions/6200270/decorator-to-print-function-call-details-parameters-names-and-effective-values

def dump_args(func):
    """Decorator to print function call details - parameters names and effective values.
    """
    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str =  ', '.join('{} = {!r}'.format(*item) for item in func_args.items())
        print(f'{func.__module__}.{func.__qualname__} ( {func_args_str} )')
        return func(*args, **kwargs)
    return wrapper

@dump_args
def test(a, b=4, c='blah-blah', *args, **kwargs):
    pass
