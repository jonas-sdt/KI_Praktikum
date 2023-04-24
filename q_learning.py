import random
from action import Action
from robot_state import RobotState


class QValueAlgorithm:
    def __init__(self):
        self.q_values = {}
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
            return max(self.action_list, key=lambda a: self.q_values.get((self.robot_state.get_state(), a), 0))

    def update_states(self, new_state):
        for state in self.states:
            if state.is_equal(new_state):
                return
        self.states.append(new_state)

    def update_q_values(self, current_state, action, reward, next_state):
        current_q = self.q_values.get((current_state, action), 0)
        max_next_q = max(self.q_values.get((next_state, a), 0) for a in self.action_list)
        updated_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_values[(current_state, action)] = updated_q

    def run(self):
        for i in range(self.episodes):
            self.robot_state.reset()
            current_state = self.robot_state.get_state()
            self.update_states(current_state)

            while True:
                action = self.choose_action()
                self.robot_state.do_action(action)
                reward = self.get_reward()
                next_state = self.robot_state.get_state()
                self.update_states(next_state)
                self.update_q_values(current_state, action, reward, next_state)

                current_state = next_state
                if self.robot_state.check_end_position():
                    break

            self.epsilon -= 0.01


if __name__ == '__main__':
    q_value_algorithm = QValueAlgorithm()
    q_value_algorithm.run()
    print(q_value_algorithm.q_values)
