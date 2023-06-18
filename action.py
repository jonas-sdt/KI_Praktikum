from enum import Enum


class Action(Enum):
    L = (0, -1, 0)
    R = (0, 1, 0)
    U = (-1, 0, 0)
    D = (1, 0, 0)
    W = (0, 0, 45)
    C = (0, 0, -45)


class Options(Enum):
    TRAINING_GENERATED = "Train on generated data"
    TRAINING_REAL = "Train on real data"
    EXECUTE_FINAL = "Execute final model"

class Distance(Enum):
    CLOSER = 1
    FARTHER = 0
    SAME = 2
