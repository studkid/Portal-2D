from abc import ABC, abstractmethod

class PhysObj():
    # Constructor
    # x y = coordinates
    # weight = weight of the object
    def __init__(self, x, y, weight) -> None:
        self.x = x
        self.y = y
        self.weight = weight

    

class TestObj(PhysObj):
    def __init__(self, x, y, weight, radius) -> None:
        super().__init__(x, y, weight)
        self.radius = radius

    def toString(self) -> str:
        return f"({self.x}, {self.y}) Weight: {self.weight} Radius: {self.radius}"