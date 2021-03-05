from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


class TimeSlot:
    def __init__(self, x: float, y: float):
        self.slot = Point(x, y)
        self.register_slot = Point(x + 75, y + 95)
