import copy
from abc import ABC, abstractmethod
from math import pi as PI
from typing import Dict


class Shape(ABC):
    """Abstract Shape Class"""

    def __init__(self, x: int = 0, y: int = 0, color: str = "black", name: str = "shape"):
        self.x = x
        self.y = y
        self.color = color
        self.name = name

    @abstractmethod
    def get_area(self):
        ...

    def set_id(self, sid: int) -> None:
        self.id = sid

    def clone(self) -> object:
        return copy.copy(self)


class Rectangle(Shape):
    """Rectangle Shape"""

    def __init__(self, width: int = 0, height: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height

    def get_area(self) -> int:
        return self.width * self.height


class Circle(Shape):
    """Circle Shape"""

    def __init__(self, radius: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def get_area(self) -> float:
        return PI * (self.radius ** 2)


class Prototype:
    """Prototype class"""

    cache: Dict[int, Shape] = {}

    @staticmethod
    def get_shape(sid):
        SHAPE = Prototype.cache.get(sid, None)
        return SHAPE.clone()

    @staticmethod
    def load():
        rect = Rectangle(18, 12, name='Rectangle')
        rect.set_id(1)
        Prototype.cache[rect.id] = rect

        square = Rectangle(11, 11, name='Square')
        square.set_id(2)
        Prototype.cache[square.id] = square

        circle = Circle(14, name='Circle')
        circle.set_id(3)
        Prototype.cache[circle.id] = circle


if __name__ == '__main__':
    Prototype.load()

    shape1 = Prototype.get_shape(1)
    print(shape1.name, shape1.get_area())

    shape2 = Prototype.get_shape(2)
    print(shape2.name, shape2.get_area())

    shape3 = Prototype.get_shape(3)
    print(shape3.name, shape3.get_area())
