import random

from action import Action
from robot_state import RobotState
from state import State


class q_value_algorithm:
    def __init__(self):
        self.q_values = []
        self.states = []
        self.epsilon = 1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = [Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN, Action.TURN_LEFT, Action.TURN_RIGHT]
        self.episodes = 1000
        self.robot_state = RobotState()
        self.action_number = 0

    def get_reward(self):
        if self.robot_state.check_collision():
            return -1000
        elif self.robot_state.position == self.robot_state.end_position:
            return 1000
        else:
            return -1

    def choose_action(self):
        if random.random() < self.epsilon:
            return random.choice(self.action_list)
        else:
            return self.action_list[self.q_values[-1].index(max(self.q_values[-1]))]

    def update_states(self, new_state):
        for state in self.states:
            if state.is_equal(new_state):
                return
        self.states.append(new_state)

    def run(self):
        episodes = 1000
        for i in range(episodes):
            current_state = self.robot_state.get_state()

            while True:
                action = self.choose_action()
                self.robot_state.do_action(action)
                self.get_reward()
                self.epsilon -= 0.01
                new_state = self.robot_state.get_state()




