import numpy as np
from action import Action
from q_value_algorithm import QValueAlgorithm

if __name__ == '__main__':
    q_value_algorithm = QValueAlgorithm()
    q_value_algorithm.run()

    # Determine optimal policy
    optimal_policy = {}
    for state, q_values in q_value_algorithm.q_values.items():
        best_action_index = np.argmax(q_values)
        best_action = q_value_algorithm.action_list[best_action_index]
        optimal_policy[state] = best_action

    print("Optimal Policy:")
    for state, action in optimal_policy.items():
        print(f"State: {state} -> Action: {action}")
