from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):
    def draw(self):
        print("Circle")


class Square(Shape):
    def draw(self):
        print("Square")


class ShapeFactory:
    def get_shape(self, shape_type: str) -> Shape:
        if shape_type == "circle":
            return Circle()
        if shape_type == "square":
            return Square()
        raise ValueError("Unknown shape")


def client_code():
    factory = ShapeFactory()
    shape1 = factory.get_shape("circle")
    shape1.draw()
    shape2 = factory.get_shape("square")
    shape2.draw()


if __name__ == "__main__":
    client_code()
