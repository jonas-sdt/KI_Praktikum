import numpy as np

from constants import LOCAL_GOAL, ELECTRODE_1, ELECTRODE_2


# For now the class still uses the old attributes. Change later, when the new attributes (nxn array) are implemented.
class State:
    def __init__(self, position: tuple, orientation: int, local_goal_position: tuple, segmented_image):
        self.image = segmented_image.copy()
        self.matrix = np.zeros((5, 5))
        self.orientation = orientation
        self.local_goal_position = local_goal_position
        self.segmented_image = segmented_image
        self.position = position
        # mark the local goal position in the image
        self.image[local_goal_position] = LOCAL_GOAL

        for i in range(5):
            for j in range(5):
                # Check if value is out of bounds
                if position[0] - 2 + i < 0 or position[0] - 2 + i >= self.image.shape[0] or position[1] - 2 + j < 0 or \
                        position[1] - 2 + j >= self.image.shape[1]:
                    self.matrix[i][j] = 0
                else:
                    self.matrix[i][j] = self.image[position[0] - 2 + i, position[1] - 2 + j]

        orientation_mapping = {
            0: [(0, 2), (4, 2)],
            45: [(0, 0), (4, 4)],
            90: [(2, 0), (2, 4)],
            135: [(4, 0), (0, 4)],
            180: [(4, 2), (0, 2)],
            225: [(4, 4), (0, 0)],
            270: [(2, 4), (2, 0)],
            315: [(0, 4), (4, 0)]
        }

        for angle, positions in orientation_mapping.items():
            if orientation == angle:
                self.matrix[positions[0][0]][positions[0][1]] += ELECTRODE_1
                self.matrix[positions[1][0]][positions[1][1]] += ELECTRODE_2

    def is_collided(self):
        # Find the positions of ELECTRODE_1 and ELECTRODE_2
        electrode1_pos = np.where(self.matrix == ELECTRODE_1 + 3)
        electrode2_pos = np.where(self.matrix == ELECTRODE_2 + 4)

        if len(electrode1_pos[0]) == 0 or len(electrode2_pos[0]) == 0:
            return True
        else:
            return False

    # Added, because we want to save only the matrix hash in the q table and not the instance itself
    def get_hash(self):
        return np.array_str(self.matrix)

    def __str__(self):
        # Pretty print the matrix with the correct values
        return str(self.matrix)
