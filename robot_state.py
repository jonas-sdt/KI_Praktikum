import cv2
import numpy as np
import math
import os
import matplotlib.pyplot as plt

from constants import AGENT, ELECTRODE1, ELECTRODE2


class RobotState:
    def __init__(self):
        self.position = (0, 0)
        self.end_position = (0, 0)
        self.angle = 0
        self.movement_area = None
        self.electrode1_pos = None
        self.electrode2_pos = None
        self.electrode1_area = None
        self.electrode2_area = None
        self.load_image()
        self.update_start_position()
        self.update_end_position()

    def load_image(self):
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

    def do_action(self, action):
        # action is a tuple of (x, y, angle)
        print("Action: ", action)
        self.position = (self.position[0] + action[0], self.position[1] + action[1])
        self.angle = (self.angle + action[2]) % 360
        self.update_area(self.position, self.angle)
        self.update_electrode_area()

    def check_collision(self):
        # Check if one of the electrodes is on a wire
        if self.movement_area[self.electrode1_pos[0], self.electrode1_pos[1]] == 1 or \
                self.movement_area[self.electrode2_pos[0], self.electrode2_pos[1]] == 1:
            return True
        else:
            return False

    def update_electrode_area(self):
        # Check if there is wire in a 5x5 area around the electrodes
        self.electrode1_area = self.movement_area[self.electrode1_pos[0] - 2:self.electrode1_pos[0] + 3,
                               self.electrode1_pos[1] - 2:self.electrode1_pos[1] + 3]
        self.electrode2_area = self.movement_area[self.electrode2_pos[0] - 2:self.electrode2_pos[0] + 3,
                               self.electrode2_pos[1] - 2:self.electrode2_pos[1] + 3]

    def update_end_position(self):
        # find the indices of rows where the last column has the value 1
        y_coordinate = np.squeeze(np.argwhere(self.movement_area[:, -1] == 1))
        self.end_position = (self.movement_area.shape[0] - 1, y_coordinate.item(0))
        print(self.end_position)

    def update_start_position(self):
        # find the indices of rows where the first column has the value 1
        y_coordinate = np.squeeze(np.argwhere(self.movement_area[:, 0] == 1))
        self.start_position = (0, y_coordinate.item(0))
        print(self.start_position)

    def plot_movement_area(self):
        plt.imshow(self.movement_area, cmap='gray')
        plt.show()

    def reset(self):
        self.position = self.start_position
        self.angle = 0
        self.update_area(self.position, self.angle)
        self.update_electrode_area()


# main function
if __name__ == '__main__':
    robot_state = RobotState()
    robot_state.plot_movement_area()