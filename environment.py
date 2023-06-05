import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

from action import Action
from constants import AGENT, WIRE, NO_WIRE, AGENT_ON_WIRE, AGENT_ON_NO_WIRE
from state import State


class Environment:
    def __init__(self, image: np.array, pixel_to_mm_ratio):
        cv2.namedWindow("display", cv2.WINDOW_NORMAL)
        self.position = (0, 256)  # TODO: Change to start position
        self.end_position = (512, 256)
        self.orientation = 0
        self.pixel_to_mm_ratio = 1
        self.state = None
        self.image = image
        self.old_positions = []
        self.__current_target_position = None
        self.__last_distance_to_target = None
        self.__current_distance_to_target = None
        self.__old_targets = []
        self.__last_position = (0, 256)
        self.__first_action = True
        self.__do_four_steps()

    def __do_four_steps(self):
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)

    def show_image(self):
        # Mark the current position of the agent in the image
        marked_image = self.image.copy()
        # Convert the image to 8-bit depth
        marked_image = cv2.normalize(marked_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # Convert the image to RGB
        marked_image = cv2.cvtColor(marked_image, cv2.COLOR_GRAY2RGB)
        marked_image = cv2.circle(marked_image, self.position, radius=0, color=(0, 0, 255), thickness=2)
        # Show the image
        cv2.imshow('display', marked_image)
        # Update the window
        cv2.waitKey(1)

    def do_action(self, action):
        # action is a tuple of (x, y, orientation)
        print("Action: ", action)
        if not self.__first_action:
            self.image[self.position[0], self.position[1]] = self.image[self.position[0], self.position[1]] - AGENT
        self.position = (self.position[0] + action.value[0], self.position[1] + action.value[1])

        # Check if the agent is out of bounds
        if self.position[0] < 0 or self.position[0] >= self.image.shape[0] or self.position[1] < 0 or self.position[1] >= self.image.shape[1]:
            self.position = self.__last_position
            return True
        self.__last_position = self.position

        self.orientation = (self.orientation + action.value[2]) % 360
        self.image[self.position[0], self.position[1]] = self.image[self.position[0], self.position[1]] + AGENT
        is_closer = self.update_distance_to_target()
        self.update_target()
        self.state = State(self.image, self.position, self.orientation, self.pixel_to_mm_ratio, self.__current_target_position)
        self.__first_action = False
        if not self.__first_action:
            self.add_old_position(action)
        self.show_image()

        return False

    def add_old_position(self, action):
        if action == Action.TURN_LEFT or action == Action.TURN_RIGHT:
            return

        offsets = {
            Action.RIGHT: [(-1, 0), (-1, 1), (-1, -1)],
            Action.LEFT: [(1, 0), (1, 1), (1, -1)],
            Action.UP: [(0, 1), (1, 1), (-1, 1)],
            Action.DOWN: [(0, -1), (1, -1), (-1, -1)]
        }

        for offset in offsets[action]:
            self.old_positions.append((self.position[0] + offset[0], self.position[1] + offset[1]))


    def reset_agent(self):
        self.position = (0, 256)  # TODO: Change to start position
        self.orientation = 0
        # self.image[self.position[0], self.position[1]] = AGENT
        # self.do_action(Action.RIGHT)
        # self.do_action(Action.RIGHT)
        self.__do_four_steps()

    def check_end_position(self):
        if self.position[0] == self.end_position[0] - 2 and self.position[1] == self.end_position[1]:
            self.__do_four_steps()
            return True
        else:
            return False

    def update_target(self):
        """
        This method checks in a 5x5 area around the agent for the nearest pixel with the value WIRE
        """
        # If the target is already found, return
        if self.position is not self.__current_target_position:
            return

        self.__old_targets.append(self.__current_target_position)

        # Get the area around the agent
        area = self.image[self.position[0] - 2:self.position[0] + 3, self.position[1] - 2:self.position[1] + 3]

        # Get the indices of the pixels with the value WIRE
        indices = np.where(area == WIRE)

        # If there are no pixels with the value WIRE, return
        if len(indices[0]) == 0:
            return

        indices = []
        # Get the indeces of the pixel with the value WIRE that is in the area around the agent
        for i in range(len(area)):
            for j in range(len(area[i])):
                if area[i][j] == WIRE:
                    indices.append((i, j))

        # Sort the indices according to the distance to the agent

        indx_with_distance = {}
        for index in indices:
            distance = np.sqrt((index[0] - 2) ** 2 + (index[1] - 2) ** 2)
            indx_with_distance[index] = distance

        sorted_indices = sorted(indx_with_distance.items(), key=lambda x: x[1])


        # Iterate over the indx_with_distance until there is an index that is not in the old targets
        for index in sorted_indices:
            pos = (self.position[0] - 2 + index[0][0], self.position[1] - 2 + index[0][1])
            if pos not in self.__old_targets:
                self.__current_target_position = pos
                break

        self.__current_distance_to_target = 0
        self.__last_distance_to_target = self.__current_distance_to_target

    def update_distance_to_target(self):
        """
        This method calculates the distance to the target
        """
        self.__current_distance_to_target = np.sqrt((self.position[0] - self.__current_target_position[0]) ** 2 + (self.position[1] - self.__current_target_position[1]) ** 2)
        is_closer = self.__current_distance_to_target < self.__last_distance_to_target
        self.__last_distance_to_target = self.__current_distance_to_target

        return is_closer






