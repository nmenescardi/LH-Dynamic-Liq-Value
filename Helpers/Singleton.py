"""singleton decorator"""


def singleton(cls):
    """Helper function to decorate singleton classes"""

    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper
