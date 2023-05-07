import random

import numpy as np

from action import Action
from environment import Environment


class QValueAlgorithm:
    def __init__(self):
        self.q_values = {}
        self.epsilon = 1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = list(Action)
        self.episodes = 1000
        self.environment = Environment()
        self.action_number = 0

    def get_reward(self):
        if self.environment.check_collision():
            return -1000
        elif self.environment.position == self.environment.end_position:
            return 1000
        else:
            return -1

    def choose_action(self, current_state):
        if random.random() < self.epsilon:
            return random.choice(self.action_list)
        else:
            return self.get_best_action(current_state)

    def update_states(self, new_state):
        if new_state not in self.q_values.keys():
            self.q_values[new_state] = np.zeros(len(self.action_list))

    def update_q_values(self, current_state, action, reward, next_state):
        current_q = self.q_values.get(current_state)[self.action_list.index(action)]
        max_next_q = max(self.q_values.get(next_state))
        updated_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_values.get(current_state)[self.action_list.index(action)] = updated_q

    def run(self):
        for i in range(self.episodes):
            self.environment.reset_agent()
            current_state = self.environment.get_current_state()
            self.update_states(current_state)

            while True:
                action = self.choose_action(current_state)
                self.environment.do_action(action)
                reward = self.get_reward()
                next_state = self.environment.get_current_state()
                self.update_states(next_state)
                self.update_q_values(current_state, action, reward, next_state)

                current_state = next_state
                if self.environment.check_end_position():
                    break

            self.epsilon -= 0.01

    def get_best_action(self, current_state):
        best_action = None
        best_q = float('-inf')
        for action in self.action_list:
            q_value = self.q_values.get(current_state)[self.action_list.index(action)]
            if q_value > best_q:
                best_q = q_value
                best_action = action

        return best_action


if __name__ == '__main__':
    q_value_algorithm = QValueAlgorithm()
    q_value_algorithm.run()
    print(q_value_algorithm.q_values)
