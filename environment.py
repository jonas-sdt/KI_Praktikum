import cv2
import numpy as np
import math
import os
import matplotlib.pyplot as plt

from action import Action
from constants import AGENT, ELECTRODE1, ELECTRODE2
from state import State


class Environment:
    def __init__(self):
        self.position = (0, 0)
        self.end_position = (0, 0)
        self.angle = 0
        self.movement_area = None
        self.electrode1_pos = None
        self.electrode2_pos = None
        self.load_image()
        self.update_start_position()
        self.update_end_position()
        self.agent_area = None
        self.do_start_steps()

    def load_image(self):
        # TODO: Move this to different file / class
        # Load the image
        path = os.getcwd() + '/training_images/image.png'
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        # Save the image as a numpy array where 0 is black and 1 is white
        self.movement_area = np.where(img == 0, 0, 1)

    def update_area(self, agent_pos, agent_angle):
        # Add agent to starting position and angle
        self.movement_area[agent_pos[0], agent_pos[1]] = AGENT

        # Add electrodes to the array
        electrode_distance = 10  # distance from agent to electrodes
        electrode_angle = math.radians(agent_angle)  # convert angle to radians
        self.electrode1_pos = (agent_pos[0] + int(electrode_distance * math.cos(electrode_angle + math.pi / 4)),
                               agent_pos[1] + int(electrode_distance * math.sin(electrode_angle + math.pi / 4)))
        self.electrode2_pos = (agent_pos[0] + int(electrode_distance * math.cos(electrode_angle - math.pi / 4)),
                               agent_pos[1] + int(electrode_distance * math.sin(electrode_angle - math.pi / 4)))
        self.movement_area[self.electrode1_pos[0], self.electrode1_pos[1]] = ELECTRODE1  # example value for electrode 1
        self.movement_area[self.electrode2_pos[0], self.electrode2_pos[1]] = ELECTRODE2  # example value for electrode 2
        self.analyse_state()

    def do_action(self, action):
        # action is a tuple of (x, y, angle)
        print("Action: ", action)
        self.position = (self.position[0] + action.value[0], self.position[1] + action.value[1])
        self.angle = (self.angle + action.value[2]) % 360
        self.update_area(self.position, self.angle)

    def check_collision(self):
        # Check if one of the electrodes is on a wire
        if self.movement_area[self.electrode1_pos[0], self.electrode1_pos[1]] == 1 or \
                self.movement_area[self.electrode2_pos[0], self.electrode2_pos[1]] == 1:
            return True
        else:
            return False

    def update_end_position(self):
        # find the indices of rows where the last column has the value 1
        y_coordinate = np.squeeze(np.argwhere(self.movement_area[:, -1] == 1))
        self.end_position = (self.movement_area.shape[0] - 1, y_coordinate.item(0))
        print(self.end_position)

    def update_start_position(self):
        # find the indices of rows where the first column has the value 1
        y_coordinate = np.squeeze(np.argwhere(self.movement_area[:, 0] == 1))
        self.start_position = (0, y_coordinate.item(0))
        self.position = self.start_position
        self.update_area(self.position, self.angle)
        print(self.start_position)

    def plot_movement_area(self):
        plt.imshow(self.movement_area, cmap='gray')
        plt.show()

    def reset(self):
        self.position = self.start_position
        self.angle = 0
        self.update_area(self.position, self.angle)

    def analyse_state(self):
        # Create a new numpy array which is a 5x5 area around the agent with the values from the movement area
        self.agent_area = self.movement_area[self.position[0] - 2:self.position[0] + 3,
                                        self.position[1] - 2:self.position[1] + 3]

    def get_state(self):
        # This method shouldn't be needed later on, when the state is done.
        current_state = State(self.position, self.electrode1_pos, self.electrode2_pos, self.agent_area)
        return current_state

    def check_end_position(self):
        if self.position == self.end_position:
            return True
        else:
            return False

    def do_start_steps(self):
        # Do 2 steps to get the agent away from the start position
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)


# main function
if __name__ == '__main__':
    environment = Environment()
    environment.plot_movement_area()