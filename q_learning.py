import os
import random

import cv2

from action import Action
from environment import Environment
from image_generator import ImageGenerator


class QValueAlgorithm:
    def __init__(self):
        self.__out_of_bounds = False
        self.q_values = {}
        self.epsilon = 1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = list(Action)
        self.episodes = 1000
        self.action_number = 0

    def get_reward(self, environment):
        if self.__out_of_bounds:
            return -100

        if environment.next_state.is_collided():
            return -100
        else:
            return -1

    def choose_action(self, environment):
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.action_list)
        else:
            action = self.get_best_action(environment)

        self.check_action_validity(environment, action)

        return action

    def get_q_value(self, environment, action):
        if environment.current_state not in self.q_values:
            self.q_values[environment.current_state] = [0] * len(self.action_list)
        if environment.next_state not in self.q_values:
            self.q_values[environment.next_state] = [0] * len(self.action_list)

        value = (1 - self.alpha) * self.q_values[environment.current_state][
            self.action_list.index(action)] + self.alpha * (
                            self.get_reward(environment) + self.gamma * max(self.q_values[environment.next_state]))
        return value

    def update_q_values(self, environment, action):
        if environment.next_state not in self.q_values:
            self.q_values[environment.next_state] = [0] * len(self.action_list)

        self.q_values[environment.current_state][self.action_list.index(action)] = self.get_q_value(environment, action)

    def check_action_validity(self, environment, action):
        ROWS, COLS = environment.image.shape[:2]

        if environment.position[0] == 0 and action == Action.LEFT:
            self.__out_of_bounds = True
        elif environment.position[0] == ROWS - 1 and action == Action.RIGHT:
            self.__out_of_bounds = True
        elif environment.position[1] == 0 and action == Action.UP:
            self.__out_of_bounds = True
        elif environment.position[1] == COLS - 1 and action == Action.DOWN:
            self.__out_of_bounds = True

    def learn_training(self):
        igen = ImageGenerator(512, 512)
        image = igen.generate_image()
        self.learn_exec(image)

    def learn_exec(self, image):
        environment = Environment(image, 1)
        self.explore(environment)

    def explore(self, environment):
        for i in range(self.episodes):
            environment.update_states()
            while not environment.check_end_position():
                action = self.choose_action(environment)
                if self.__out_of_bounds:
                    print("Invalid action, out of bounds")
                    self.__out_of_bounds = False
                    break
                environment.do_action(action)
                self.update_q_values(environment, action)
                environment.update_states()

                self.epsilon -= 0.01

            self.epsilon = 1
            print("Episode: " + str(i) + " finished")
            environment.reset_agent()

        print("Training finished")
        print(self.q_values)

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
