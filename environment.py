import os

import cv2
import numpy as np

from action import Action
from constants import AGENT
from state import State


class Environment:
    def __init__(self, image_path):
        self.position = (0, 0) # TODO: Change to start position
        self.end_position = (0, 0)
        self.angle = 0
        self.image = None
        self.__load_image(image_path)
        self.__do_two_steps()

    def __load_image(self, path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        # Save the image as a numpy array where 0 is black and 1 is white
        self.image = np.where(img == 0, 0, 1)

    def __do_two_steps(self):
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)

    def do_action(self, action):
        # action is a tuple of (x, y, angle)
        print("Action: ", action)
        self.position = (self.position[0] + action.value[0], self.position[1] + action.value[1])
        self.angle = (self.angle + action.value[2]) % 360
        self.image[self.position[0], self.position[1]] = AGENT

    def reset_agent(self):
        self.position = (0, 0) # TODO: Change to start position
        self.angle = 0
        self.image[self.position[0], self.position[1]] = AGENT

    def get_current_state(self):
        current_state = State(self.position, self.electrode1_pos, self.electrode2_pos, self.agent_area)
        return current_state

    def check_end_position(self):
        if self.position[0] == self.end_position[0] - 2 and self.position[1] == self.end_position[1]:
            self.__do_two_steps()
            return True
        else:
            return False


# main function
if __name__ == '__main__':
    training_image_path = os.path.join(os.getcwd(), "training_images", "image_1.png")
    environment = Environment(training_image_path)
    environment.plot_movement_area()
