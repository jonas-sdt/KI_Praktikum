import unittest

import cv2

from action import Action
from environment import Environment


# class TestEnvironment(unittest.TestCase):
#     def __init__(self):
#         super().__init__()
#         test_image = cv2.imread("test_image.png")
#         self.environment = Environment(test_image, 1)
#
#     def test_target_position(self):
#         print(self.environment._Environment__target_position)

class TestEnvironment():
    def __init__(self):
        test_image = cv2.imread("test_image.png")
        # Remove the last line of the image and add a new line at the top
        test_image = test_image[:,:,0]
        # Norm to 0 and 1
        test_image = test_image / 255
        self.environment = Environment(test_image, 1)

    def test_target_position(self):
        assert self.environment._Environment__current_target_position == (256, 1)
        print(self.environment.state)
        self.environment.do_action(Action.RIGHT)
        print(self.environment.state)
        assert self.environment._Environment__current_target_position == (256, 2)
        self.environment.do_action(Action.RIGHT)
        print(self.environment.state)
        assert self.environment._Environment__current_target_position == (257, 3)
        self.environment.do_action(Action.DOWN)
        print(self.environment.state)
        assert self.environment._Environment__current_target_position == (257, 3)
        self.environment.do_action(Action.RIGHT)
        assert self.environment._Environment__current_target_position == (258, 4)
        self.environment.do_action(Action.RIGHT)
        assert self.environment._Environment__current_target_position == (258, 4)
        self.environment.do_action(Action.DOWN)
        assert self.environment._Environment__current_target_position == (258, 5)
        self.environment.do_action(Action.DOWN)
        self.environment.do_action(Action.DOWN)
        self.environment.do_action(Action.DOWN)
        self.environment.do_action(Action.DOWN)
        print(self.environment.state.is_collided())


if __name__ == '__main__':
    test_environment = TestEnvironment()
    test_environment.test_target_position()
