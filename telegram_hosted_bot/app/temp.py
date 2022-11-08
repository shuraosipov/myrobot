import functools


def auth_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Authenticating...")
        func(*args, **kwargs)
    return wrapper

@auth_decorator
def echo(text):
    print(text)

echo("Hello World")