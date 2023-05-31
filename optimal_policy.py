import numpy as np
from action import Action
from q_learning import QValueAlgorithm

if __name__ == '__main__':
    q_learning = QValueAlgorithm()
    q_learning.run()

    # Determine optimal policy
    optimal_policy = {}
    for state, q_values in q_learning.q_values.items():
        best_action_index = np.argmax(q_values)
        best_action = q_learning.action_list[best_action_index]
        optimal_policy[state] = best_action
    print("Optimal Policy:")
    for state, action in optimal_policy.items():
        print(f"State: {state} -> Action: {action}")
