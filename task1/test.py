from task1 import retry_on_except


@retry_on_except((ZeroDivisionError, KeyError), max_attempts=3)
def risky_operator(x, y):
    return x / y


if __name__ == "__main__":
    risky_operator(10, 0)
