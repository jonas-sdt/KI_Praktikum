import os
import pickle

import cv2
import numpy as np

from action import Action
from environment import Environment


class ExecuteBest:
    def __init__(self):
        # Get the first element from the real_images folder
        self.action_list = list(Action)
        path = os.path.join(os.getcwd(), "real_images")
        self.image = cv2.imread(os.path.join(path, os.listdir(path)[0]), cv2.IMREAD_GRAYSCALE)
        self.image = self.image / 255
        self.all_positions = []
        self.all_actions = []
        self.environment = Environment(self.image, 1)

        self.q_values = self.load_q_values()

    def load_q_values(self):
        pickle_file_path = os.getcwd() + "/q_values_finished.pickle"
        with open(pickle_file_path, 'rb') as file:
            return pickle.load(file)
        
    def execute(self):
        self.environment.do_action(Action.RIGHT)
        self.all_actions.append(Action.RIGHT.name)
        while self.environment.position != self.environment.end_position:
            self.all_positions.append(self.environment.position)
            state = self.environment.state
            best_action = self.get_best_action(state)
            self.all_actions.append(best_action.name)
            self.environment.do_action(best_action)

        # Convert the image to bgr
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

        # Add all positions to the image with the color green
        for position in self.all_positions:
            self.image[position[0]][position[1]] = [0, 255, 0]

        # Show the image
        cv2.imshow("image", self.image)

    def get_best_action(self, state):
        """
        This method returns the action with the highest Q-value for the given state
        :param state:
        """
        max_q_value = np.max(self.q_values[state.get_hash()])
        max_q_value_indicex = np.where(self.q_values[state.get_hash()] == max_q_value)[0]
        return self.action_list[max_q_value_indicex[0]]
