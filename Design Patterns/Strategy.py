from typing import Callable


class Context:
    def __init__(self, strategy: Callable[[int, int], int]):
        self.strategy = strategy

    def execute(self, a: int, b: int) -> int:
        return self.strategy(a, b)


def add(x: int, y: int) -> int:
    return x + y


def multiply(x: int, y: int) -> int:
    return x * y


if __name__ == "__main__":
    context = Context(add)
    print(context.execute(2, 3))
    context.strategy = multiply
    print(context.execute(2, 3))
