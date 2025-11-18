import functools
import time


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])


waste_some_time(5000)


# Class decorator
class Power(object):
    def __init__(self, arg):
        self._arg = arg

    def __call__(self, a, b):
        retval = self._arg(a, b)
        return retval**2


@Power
def multiply_together(a, b):
    return a * b


print(multiply_together)
print(multiply_together(2, 2))


# Class decorator that accepts parameters
class Power(object):
    def __init__(self, arg):
        self._arg = arg

    def __call__(self, *param_arg):
        """If there are decorator arguments, __call__() is only called once
        as part of the decoration process. You can only give it a single argument,
        which is the function object
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        if len(param_arg) == 1:

            def wrapper(a, b):
                retval = param_arg[0](a, b)
                return retval**self._arg

            return wrapper
        else:
            expo = 2
            retval = self._arg(param_arg[0], param_arg[1])
            return retval**expo


@Power(3)
def multiply_together(a, b):
    return a * b


class Decorator(object):
    def __init__(self, *decorator_args, **decorator_kwargs):
        print(
            f"inside __init__() with input function with args {decorator_args} and kwargs {decorator_kwargs}"
        )

    def __call__(self, f):
        print(f"inside __call__() with function {f.__name__}")

        def wrapped(*args, **kwargs):
            print(f"inside wrapped with args {args} and kwargs {kwargs}")
            return f(*args, **kwargs)

        return wrapped


@Decorator("decorator arg 1", "decorator arg 2")
def my_funcion(a, b, c):
    print("inside my_funcion()")


@Decorator("decorator arg 3", "decorator arg 4")
def my_funcion_no_call(a, b, c):
    print("inside my_funcion_no_call()")


print("finished decorating my_funcion()")
my_funcion(1, 2, 3)


# Without classes
def decorator(*decorator_args, **decorator_kwargs):
    print(f"inside decorator with args {decorator_args} and kwargs {decorator_kwargs}")

    def inner(f):
        print(f"inside inner(f) with function {f.__name__}")

        def wrapped(*args, **kwargs):
            print(f"inside wrapped with args {args} and kwargs {kwargs}")
            return f(*args, **kwargs)

        return wrapped

    return inner


@decorator("decorator arg 1", "decorator arg 2")
def my_funcion(a, b, c):
    print("inside my_funcion()")


@decorator("decorator arg 3", "decorator arg 4")
def my_funcion_no_call(a, b, c):
    print("inside my_funcion_no_call()")


print("finished decorating my_funcion()")
my_funcion(1, 2, 3)
print("immediately after my_function() line")
