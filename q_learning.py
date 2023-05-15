import os
import random

import cv2
import numpy as np

from action import Action
from environment import Environment
from image_generator import ImageGenerator


class QValueAlgorithm:
    def __init__(self):
        self.q_values = {}
        self.epsilon = 1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = list(Action)
        self.episodes = 1000
        self.action_number = 0

    def get_reward(self, state):
        if state.is_collided():
            return -1000
        else:
            return -1

    def choose_action(self, environment):
        if random.random() < self.epsilon:
            return random.choice(self.action_list)
        else:
            return self.get_best_action(environment.current_state)

    def update_states(self, next_state):
        if next_state not in self.q_values.keys():
            self.q_values[next_state] = np.zeros(len(self.action_list))

    def update_q_values(self, environment, action, reward):
        current_q = self.q_values.get(environment.current_state)[self.action_list.index(action)]
        max_next_q = max(self.q_values.get(environment.next_state))
        updated_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_values.get(environment.current_state)[self.action_list.index(action)] = updated_q

    def learn_training(self):
        igen = ImageGenerator(512, 512)
        image = igen.generate_image()
        self.learn_exec(image)

    def learn_exec(self, image):
        environment = Environment(image, 1)
        self.explore(environment)

    def explore(self, environment):
        for i in range(self.episodes):
            environment.reset_agent()
            environment.update_states()
            current_state = environment.current_state
            self.update_states(environment.next_state)

            while True:
                action = self.choose_action(current_state)
                environment.do_action(action)
                reward = self.get_reward(environment.next_state)
                self.update_states(environment.next_state)
                self.update_q_values(environment, action, reward)

                environment.update_states()
                if environment.check_end_position():
                    break

            self.epsilon -= 0.01

    def get_best_action(self, environment):
        best_action = None
        best_q = float('-inf')
        for action in self.action_list:
            q_value = self.q_values.get(environment.current_state)[self.action_list.index(action)]
            if q_value > best_q:
                best_q = q_value
                best_action = action

        return best_action


if __name__ == '__main__':
    q_value_algorithm = QValueAlgorithm()
    decision = input("Choose A for exec or B for training")
    if decision == "A":
        file_path = ""
        file_name = ""
        try:
            file_path = os.getcwd() + "/real_images"
            file_name = os.listdir(file_path)[0]
        except FileNotFoundError:
            print("File not found")
            exit(1)

        image = cv2.imread(file_path + "/" + file_name)
        q_value_algorithm.learn_exec(image)
    elif decision == "B":
        q_value_algorithm.learn_training()
    else:
        raise RuntimeError
