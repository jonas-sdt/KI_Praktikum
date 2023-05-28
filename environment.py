import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

from action import Action
from constants import AGENT, WIRE, NO_WIRE, AGENT_ON_WIRE, AGENT_ON_NO_WIRE
from state import State


class Environment:
    def __init__(self, image: np.array, pixel_to_mm_ratio):
        self.position = (0, 256)  # TODO: Change to start position
        self.end_position = (512, 256)
        self.orientation = 0
        self.current_state = None
        self.pixel_to_mm_ratio = 1
        self.next_state = None
        self.image = image
        self.__first_action = True
        self.__do_two_steps()

    def __do_two_steps(self):
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)

    def clean_image(self):
        pixel = self.image[self.position[0], self.position[1]]
        if pixel == AGENT_ON_WIRE:
            pixel = WIRE
        elif pixel == AGENT_ON_NO_WIRE:
            pixel = NO_WIRE
        else:
            print("Error: Invalid pixel value, value: ", pixel, " position: ", self.position, " orientation: ", self.orientation)
            raise Exception

        self.image[self.position[0], self.position[1]] = pixel

    def do_action(self, action):
        # action is a tuple of (x, y, orientation)
        print("Action: ", action)
        if not self.__first_action:
            self.clean_image()
        self.position = (self.position[0] + action.value[0], self.position[1] + action.value[1])
        self.orientation = (self.orientation + action.value[2]) % 360
        self.image[self.position[0], self.position[1]] = self.image[self.position[0], self.position[1]] + AGENT
        self.next_state = State(self.image, self.position, self.orientation, self.pixel_to_mm_ratio)
        self.__first_action = False

    def reset_agent(self):
        self.position = (0, 256) # TODO: Change to start position
        self.orientation = 0
        self.image[self.position[0], self.position[1]] = AGENT
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)

    def check_end_position(self):
        if self.position[0] == self.end_position[0] - 2 and self.position[1] == self.end_position[1]:
            self.__do_two_steps()
            return True
        else:
            return False

    def update_states(self):
        self.current_state = self.next_state


# main function
if __name__ == '__main__':
    training_image_path = os.path.join(os.getcwd(), "training_images", "image_1.png")
    environment = Environment(training_image_path)
