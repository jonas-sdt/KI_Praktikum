import os
import pickle
import random
import numpy as np
import atexit

import cv2

from action import Action, Distance
from action import Options
from environment import Environment
import image_generator
from dialogue import main as dialogue_main
from execute_best import ExecuteBest


class QValueAlgorithm:
    def __init__(self):
        self.q_values = {}
        self.epsilon = 1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = list(Action)
        self.episodes = 5
        self.action_number = 0
        atexit.register(self.exit_handler)

    def load_q_values(self):
        pickle_file_path = os.getcwd() + "/q_values_finished.pickle"
        with open(pickle_file_path, 'rb') as file:
            self.q_values = pickle.load(file)


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
        :param emvironment:
        """
        state = environment.state
        if is_out_of_bounds:
            return -100

        if state.is_collided():
            environment.position = environment.old_targets[-1]
            return -100
        elif environment.old_target_reached:
            return 50

        distance_update = environment.update_distance_to_target()

        if  distance_update == Distance.CLOSER:
            return 10
        elif distance_update == Distance.FARTHER:
            return -5
        else:
            return -2

    def update_q_value(self, state, action, reward, state_new):
        """
        This method updates the Q-value for the given state-action pair
        :param state:
        :param action:
        :param reward:
        """
        if state.get_hash() not in self.q_values:
            self.q_values[state.get_hash()] = np.zeros(len(self.action_list))

        if state_new.get_hash() not in self.q_values:
            self.q_values[state_new.get_hash()] = np.zeros(len(self.action_list))

        # self.q_values[state.get_hash()][self.action_list.index(action)] += self.alpha * (reward + self.gamma * np.max(self.q_values[state.get_hash()]) - self.q_values[state.get_hash()][self.action_list.index(action)])
        #self.q_values[state.get_hash()][self.action_list.index(action)] = (1 - self.alpha) * self.q_values[state.get_hash()][self.action_list.index(action)] + self.alpha * (reward + self.gamma * np.max(self.q_values[state.get_hash()]))

        self.q_values[state.get_hash()][self.action_list.index(action)] = (1 - self.alpha) * self.q_values[state.get_hash()][self.action_list.index(action)] + self.alpha * (reward + self.gamma * np.max(self.q_values[state_new.get_hash()]))

    def learn_exec(self, image):
        """
        This method executes the learning process
        """
        environment = Environment(image, 1)
        state = environment.state
        for episode in range(self.episodes):
            while not environment.check_end_position():
                action = self.choose_action(state)
                is_out = environment.do_action(action)
                state_new = environment.state
                reward = self.get_reward(environment, is_out)
                self.update_q_value(state, action, reward, state_new)


                if is_out:
                    #environment.reset_agent()
                    environment.position = environment.old_targets[-1]

                state = state_new

                self.action_number += 1
                if self.action_number % 100 == 0:
                    self.epsilon = self.epsilon * 0.99
                #     print("Epsilon: ", self.epsilon)
                # print("Action number: ", self.action_number)
                # print("Episode: ", episode)
                # print("State: ", state)
                # print("Action: ", action)
                # print("Reward: ", reward)
                # print("Q-values: ", self.q_values)
                # print("---------------------------------------------------")
            environment = Environment(image, 1)
            state = environment.state
            print("Episode: ", episode)
        with open('q_values_finished.pickle', 'wb') as handle:
            pickle.dump(self.q_values, handle, protocol=pickle.HIGHEST_PROTOCOL)



    def learn_training(self):
        image = image_generator.generate_image(512, 512)
        # Convert image from shape (512, 512, 1) to (512, 512)
        #image = image.reshape((512, 512))
        self.learn_exec(image)

    def exit_handler(self):
        print("Saving q_values")
        with open('q_values_finished.pickle', 'wb') as handle:
            pickle.dump(self.q_values, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    q_value_algorithm = QValueAlgorithm()
    decision, number_of_images, use_pre_trained_values = dialogue_main()
    number_of_images = int(number_of_images)
    # print("Decision: ", decision)
    if decision == Options.TRAINING_REAL.value:
        # print("User chose to use real images")
        file_path = ""
        file_name = ""
        try:
            file_path = os.getcwd() + "/real_images"
            file_name = os.listdir(file_path)[0]
            image = cv2.imread(file_path + "/" + file_name)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = image[:, :] / 255
            q_value_algorithm.load_q_values()
            q_value_algorithm.learn_exec(image)
        except FileNotFoundError:
            print("File not found")
            exit(1)

    elif decision == Options.TRAINING_GENERATED.value:
        print("User chose to use generated images")
        if number_of_images <= 0:
            raise ValueError("Number of images must be greater than 0")

        if use_pre_trained_values:
            q_value_algorithm.load_q_values()

        for i in range(number_of_images + 1):
            if i > 0:
                q_value_algorithm.load_q_values()
            q_value_algorithm.learn_training()
    elif decision == Options.EXECUTE_FINAL.value:
        print("User chose to execute the final algorithm")
        execute_best = ExecuteBest()
        execute_best.execute()
    else:
        raise RuntimeError
