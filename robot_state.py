from enum import Enum
import cv2
import numpy as np
import math
import os

from constants import AGENT, EFFECTOR1, EFFECTOR2


class RobotState:
    def __init__(self, start_position, start_angle):
        self.position = start_position
        self.angle = start_angle
        self.movement_area = None
        self.effector1_pos = None
        self.effector2_pos = None
        self.effector1_area = None
        self.effector2_area = None
        self.load_image()

    def load_image(self):
        # Load the image
        path = os.getcwd() + '/training_images/image.png'
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        # Convert to numpy array
        self.movement_area = np.asarray(img)

        # Normalize the array
        self.movement_area = self.movement_area / 255

        # Invert the array
        self.movement_area = 1 - self.movement_area

    def update_area(self, agent_pos, agent_angle):
        # Add agent to starting position and angle
        self.movement_area[agent_pos[0], agent_pos[1]] = AGENT

        # Add effectors to the array
        effector_distance = 10  # distance from agent to effectors
        effector_angle = math.radians(agent_angle)  # convert angle to radians
        self.effector1_pos = (agent_pos[0] + int(effector_distance * math.cos(effector_angle + math.pi / 4)),
                         agent_pos[1] + int(effector_distance * math.sin(effector_angle + math.pi / 4)))
        self.effector2_pos = (agent_pos[0] + int(effector_distance * math.cos(effector_angle - math.pi / 4)),
                         agent_pos[1] + int(effector_distance * math.sin(effector_angle - math.pi / 4)))
        self.movement_area[self.effector1_pos[0], self.effector1_pos[1]] = EFFECTOR1  # example value for effector 1
        self.movement_area[self.effector2_pos[0], self.effector2_pos[1]] = EFFECTOR2  # example value for effector 2

    def do_action(self, action):
        # action is a tuple of (x, y, angle)
        self.position = (self.position[0] + action[0], self.position[1] + action[1])
        self.angle = (self.angle + action[2]) % 360
        self.update_area(self.position, self.angle)
        self.update_effector_area()

    def check_collision(self):
        # Check if one of the effectors is on a wire
        if self.movement_area[self.effector1_pos[0], self.effector1_pos[1]] == 1 or \
                self.movement_area[self.effector2_pos[0], self.effector2_pos[1]] == 1:
            return True
        else:
            return False

    def update_effector_area(self):
        # Check if there is wire in a 5x5 area around the effectors
        self.effector1_area = self.movement_area[self.effector1_pos[0] - 2:self.effector1_pos[0] + 3,
                                            self.effector1_pos[1] - 2:self.effector1_pos[1] + 3]
        self.effector2_area = self.movement_area[self.effector2_pos[0] - 2:self.effector2_pos[0] + 3,
                                            self.effector2_pos[1] - 2:self.effector2_pos[1] + 3]



class Action(Enum):
    LEFT = (-1, 0, 0)
    RIGHT = (1, 0, 0)
    UP = (0, -1, 0)
    DOWN = (0, 1, 0)
    TURN_LEFT = (0, 0, -45)
    TURN_RIGHT = (0, 0, 45)
