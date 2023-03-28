from enum import Enum


class Action(Enum):
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 0)
    UP = (0, -1, 0)
    DOWN = (0, 1, 0)
    TURN_LEFT = (0, 0, -45)
    TURN_RIGHT = (0, 0, 45)
