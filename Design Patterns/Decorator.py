class Text:
    def render(self) -> str:
        return "Text"


class BoldDecorator:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def render(self) -> str:
        return f"<b>{self.wrapped.render()}</b>"


class ItalicDecorator:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def render(self) -> str:
        return f"<i>{self.wrapped.render()}</i>"


if __name__ == "__main__":
    simple = Text()
    decorated = BoldDecorator(ItalicDecorator(simple))
    print(decorated.render())
