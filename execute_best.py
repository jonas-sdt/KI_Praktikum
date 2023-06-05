import os
import pickle

from environment import Environment


class ExecuteBest:
    def __init__(self):
        # Get the first element from the real_images folder
        path = os.path.join(os.getcwd(), "real_images")
        self.image = os.listdir(path)[0]

        self.environment = Environment(self.image, 1)

        self.q_values = self.load_q_values()

    def load_q_values(self):
        pickle_file_path = os.getcwd() + "/q_values_finished.pickle"
        with open(pickle_file_path, 'rb') as file:
            return pickle.load(file)
        
    def execute(self):
        state = self.environment.state
        while True:
            action = self.choose_best_action(state)
            is_out = self.environment.do_action(action)
            state = self.environment.state
            if is_out:
                break

    def choose_best_action(self, state):
        q_values = self.q_values[state]
        best_action_index = q_values.index(max(q_values))
        return self.environment.action_list[best_action_index]



if __name__ == '__main__':
    pass