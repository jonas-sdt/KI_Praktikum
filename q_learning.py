import random

from action import Action
from robot_state import RobotState
from state import State


class q_value_algorithm:
    def __init__(self):
        self.q_values = []
        self.states = []
        self.epsilon = 0.1
        self.alpha = 0.3
        self.gamma = 0.9
        self.action_list = [Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN, Action.TURN_LEFT, Action.TURN_RIGHT]
        self.episodes = 1000
        self.robot_state = RobotState()

    def get_reward(self):
        if self.robot_state.check_collision():
            return -1000
        elif self.robot_state.position == self.robot_state.end_position:
            return 1000
        else:
            return -1

    def get_q_value(self, state, action):
        for i in range(len(self.states)):
            if self.states[i].is_equal(state):
                return self.q_values[i][action.value]
        return 0

    def get_max_q_value(self, state):
        max_q_value = 0
        for action in self.action_list:
            q_value = self.get_q_value(state, action)
            if q_value > max_q_value:
                max_q_value = q_value
        return max_q_value

    def get_action(self, state):
        if random.random() < self.epsilon:
            # Check if the one of the electrodes or the agent hit one of the walls
            action = random.choice(self.action_list)
            if action == Action.LEFT and self.robot_state.position[0] == 0:
                return self.get_action(state)
            elif action == Action.UP and self.robot_state.position[1] == 0:
                return self.get_action(state)
            elif action == Action.DOWN and self.robot_state.position[1] == 511:
                return self.get_action(state)
            return action
        else:
            max_q_value = self.get_max_q_value(state)
            for action in self.action_list:
                if self.get_q_value(state, action) == max_q_value:
                    return action

    def update_q_value(self, state, action, reward, new_state):
        max_q_value = self.get_max_q_value(new_state)
        for i in range(len(self.states)):
            if self.states[i].is_equal(state):
                self.q_values[i][action.value] = self.get_q_value(state, action) + self.alpha * (reward + self.gamma * max_q_value - self.get_q_value(state, action))
                return
        self.states.append(state)
        self.q_values.append([0, 0, 0, 0, 0, 0])
        self.update_q_value(state, action, reward, new_state)

    def run(self):
        for i in range(self.episodes):
            self.robot_state.reset()
            while not self.robot_state.check_collision() and self.robot_state.position != self.robot_state.end_position:
                state = State(self.robot_state.position, self.robot_state.electrode1_pos, self.robot_state.electrode2_pos, self.robot_state.agent_area)
                action = self.get_action(state)
                self.robot_state.do_action(action)
                new_state = State(self.robot_state.position, self.robot_state.electrode1_pos, self.robot_state.electrode2_pos, self.robot_state.agent_area)
                reward = self.get_reward()
                self.update_q_value(state, action, reward, new_state)
        return self.q_values, self.states


if __name__ == "__main__":
    q_value_algorithm = q_value_algorithm()
    q_values, states = q_value_algorithm.run()
    print(q_values)
    print(states)