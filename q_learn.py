import numpy as np
import random

# ε-greedy policy
ε_start = 1.0
ε_end = 0.01
ε_decay = 0.0001

# actions: 0 = left, 1 = right, 2 = up, 3 = down, 4 = rotate cw 45°, 5 = rotate ccw 45°	
Q = np.zeros((1, 6))

ε = ε_start
alpha = 0.3

current_position = (0,0)  # (x,y)  
current_angle = 0

while(True):
    
    # choose action
    if np.random.rand() < ε:
        action = np.random.randint(0, 6)
    else:
        action = np.argmax(Q, axis=1)
    ε = max(ε_end, ε - ε_decay)
    
    # take action
      
    if action == 0:
        current_position = (current_position[0] - 1, current_position[1])
    elif action == 1:
        current_position = (current_position[0] + 1, current_position[1])
    elif action == 2:
        current_position = (current_position[0], current_position[1] - 1)
    elif action == 3:
        current_position = (current_position[0], current_position[1] + 1)
    elif action == 4:
        current_angle += 45
    elif action == 5:
        current_angle -= 45
    else:
        raise RuntimeError("Invalid action")
    
    # collision detection
    collision = False
    
    # goal reached detection
    goal_reached = False
    
    # local goal reached detection
    local_reached = False
    
    # set reward
    if collision:
        r = -100
    
    elif goal_reached:
        r = 100
    
    elif local_reached:
        r = 10
    
    else:
        r = -10
        
    # add new state to Q
    Q = np.append(Q, np.zeros((1, 6)), axis=0)
    
    # Update Q-Value
    # ! todo
    
class state_detection:
    
    def __init__(self, img, current_position: tuple, current_angle:int):
        pass
    
    def collision(self):
        pass

    def goal_reached(self):
        pass

    def local_reached(self):
        pass