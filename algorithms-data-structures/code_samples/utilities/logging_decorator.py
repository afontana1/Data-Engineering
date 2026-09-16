"""
Code Inspired from:
https://ankitbko.github.io/blog/2021/04/logging-in-python/

The final example given in the article (I believe) is unnecessary
"""

import functools
import logging
from typing import Union

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()




def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


@log
def foo(a, b):
    c = a + b
    raise Exception("Something went wrong")


class MyLogger:
    """This logger can be customized depending on your scenario

    See logger.py for an example of a custom logger
    """

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def get_logger(self, name=None):
        return logging.getLogger(name)


def get_default_logger():
    return MyLogger().get_logger()


def log(_func=None, *, my_logger: Union[MyLogger, logging.Logger] = None):
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if my_logger is None:
                logger = get_default_logger()
            else:
                if isinstance(my_logger, MyLogger):
                    logger = my_logger.get_logger(func.__name__)
                else:
                    logger = my_logger
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(f"function {func.__name__} called with args {signature}")
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.exception(
                    f"Exception raised in {func.__name__}. exception: {str(e)}"
                )
                raise e

        return wrapper

    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)


@log(my_logger=MyLogger())
def sum(a, b=10):
    return a + b


lg = MyLogger().get_logger()


@log(my_logger=lg)
def sum(a, b=10):
    return a + b
