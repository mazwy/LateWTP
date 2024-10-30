import logging as log


# TODO Rework for database logging
def logfunction(func: callable) -> callable:
    """
    This function is used to log the function.
    :param func: Function to log.
    :return: Function with logging.
    """
    def wrapper(*args, **kwargs):
        log.debug(f'Function {func.__name__} called with args: {args} and kwargs: {kwargs}')
        return func(*args, **kwargs)

    return wrapper


def logclass(cls: type) -> type:
    """
    This function is used to log all the functions in the class.
    :param cls: Class to log functions for.
    :return: Class with logged functions.
    """
    for name, obj in vars(cls).items():
        if callable(obj):
            setattr(cls, name, logfunction(obj))
    return cls


def handleexceptions(func: callable):
    """
    This function is used to handle basic exceptions in the function.
    :param func: Function to handle exceptions for.
    :return: result of the function or None if an exception occurred.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error(f'Error in function {func.__name__}: {e}')
            return None

    return wrapper
