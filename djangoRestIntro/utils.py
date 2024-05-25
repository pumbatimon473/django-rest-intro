from datetime import datetime


def debug(func):
    def wrapper(*args, **kwargs):
        print(':: DEBUG ::', datetime.now(), '::', end=' ')
        func(*args, **kwargs)
    return wrapper


@debug
def log(*args):
    print(*args)

