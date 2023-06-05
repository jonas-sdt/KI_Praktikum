import os
import pickle
import random
import numpy as np

import cv2

from action import Action
from environment import Environment
import image_generator
from dialogue import main as dialogue_main


class QValueAlgorithm:
    def __init__(self):
        self.q_values = {}
        self.epsilon = 1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = list(Action)
        self.episodes = 1000
        self.action_number = 0


    def choose_action(self, state):
        """
        This method chooses an action based on the epsilon-greedy policy
        :param state:
        """
        if random.random() < self.epsilon:
            return random.choice(self.action_list)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        """
        This method returns the action with the highest Q-value for the given state
        :param state:
        """
        max_q_value = np.max(self.q_values[state.get_hash()])
        max_q_value_indicex = np.where(self.q_values[state.get_hash()] == max_q_value)[0]
        return self.action_list[max_q_value_indicex[0]]

    def get_reward(self, environment, is_out_of_bounds=False):
        """
        This method returns the reward for the given state, if collided return -100, if in position return 10, else return -2
        :param state:
        """
        state = environment.state
        if is_out_of_bounds:
            return -100

        if state.is_collided():
            return -100
        elif environment.update_distance_to_target():
            return 10
        else:
            return -2

    def update_q_value(self, state, action, reward):
        """
        This method updates the Q-value for the given state-action pair
        :param state:
        :param action:
        :param reward:
        """
        if state not in self.q_values:
            self.q_values[state.get_hash()] = np.zeros(len(self.action_list))

        self.q_values[state.get_hash()][self.action_list.index(action)] += self.alpha * (reward + self.gamma * np.max(self.q_values[state.get_hash()]) - self.q_values[state.get_hash()][self.action_list.index(action)])

    def learn_exec(self, image):
        """
        This method executes the learning process
        """
        environment = Environment(image, 1)
        state = environment.state
        for episode in range(self.episodes):
            while not environment.check_end_position() and not state.is_collided():
                action = self.choose_action(state)
                is_out = environment.do_action(action)
                state = environment.state
                reward = self.get_reward(environment, is_out)
                self.update_q_value(state, action, reward)

                if is_out:
                    environment.reset_agent()

                self.action_number += 1
                if self.action_number % 100 == 0:
                    self.epsilon = self.epsilon * 0.99
                    print("Epsilon: ", self.epsilon)
                print("Action number: ", self.action_number)
                print("Episode: ", episode)
                print("State: ", state)
                print("Action: ", action)
                print("Reward: ", reward)
                print("Q-values: ", self.q_values)
                print("---------------------------------------------------")
            environment = Environment(image, 1)
            state = environment.state
        with open('q_values.pickle', 'wb') as handle:
            pickle.dump(self.q_values, handle, protocol=pickle.HIGHEST_PROTOCOL)



    def learn_training(self):
        image = image_generator.generate_image(512, 512)
        # Convert image from shape (512, 512, 1) to (512, 512)
        image = image.reshape((512, 512))
        self.learn_exec(image)

    def explore(self):
        pass



if __name__ == '__main__':
    q_value_algorithm = QValueAlgorithm()
    decision = dialogue_main()
    if decision:
        print("User chose to use real images")
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
    elif not decision:
        print("User chose to use generated images")
        q_value_algorithm.learn_training()
    else:
        raise RuntimeError
