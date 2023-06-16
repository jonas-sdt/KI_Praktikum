import os

import cv2
import numpy as np

import image_generator
from constants import *

os.environ["PYTHONHASHSEED"] = "42"


# For now the class still uses the old attributes. Change later, when the new attributes (nxn array) are implemented.
class State:
    def __init__(self, image, position: tuple, orientation: int, local_goal_position: tuple, segmented_image):
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

        if orientation == 0:
            self.matrix[0][2] = self.matrix[0][2] + ELECTRODE_1
            self.matrix[4][2] = self.matrix[4][2] + ELECTRODE_2
        elif orientation == 45:
            self.matrix[0][0] = self.matrix[0][0] + ELECTRODE_1
            self.matrix[4][4] = self.matrix[4][4] + ELECTRODE_2
        elif orientation == 90:
            self.matrix[2][0] = self.matrix[2][0] + ELECTRODE_1
            self.matrix[2][4] = self.matrix[2][4] + ELECTRODE_2
        elif orientation == 135:
            self.matrix[4][0] = self.matrix[4][0] + ELECTRODE_1
            self.matrix[0][4] = self.matrix[0][4] + ELECTRODE_2
        elif orientation == 180:
            self.matrix[4][2] = self.matrix[4][2] + ELECTRODE_1
            self.matrix[0][2] = self.matrix[0][2] + ELECTRODE_2
        elif orientation == 225:
            self.matrix[4][4] = self.matrix[4][4] + ELECTRODE_1
            self.matrix[0][0] = self.matrix[0][0] + ELECTRODE_2
        elif orientation == 270:
            self.matrix[2][4] = self.matrix[2][4] + ELECTRODE_1
            self.matrix[2][0] = self.matrix[2][0] + ELECTRODE_2
        elif orientation == 315:
            self.matrix[0][4] = self.matrix[0][4] + ELECTRODE_1
            self.matrix[4][0] = self.matrix[4][0] + ELECTRODE_2

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
        return hash(self.matrix.data.tobytes())

    def __str__(self):
        # Pretty print the matrix with the correct values
        return str(self.matrix)


def paint_state(img, position, orientation, pixel_to_mm_ratio, roi_size):
    # paint square around position in image
    roi_min_x = int(position[0] - roi_size / 2 * pixel_to_mm_ratio) if int(
        position[0] - roi_size / 2 * pixel_to_mm_ratio) > 0 else 0
    roi_max_x = int(position[0] + roi_size / 2 * pixel_to_mm_ratio) if int(
        position[0] + roi_size / 2 * pixel_to_mm_ratio) < img.shape[0] else img.shape[0]
    roi_min_y = int(position[1] - roi_size / 2 * pixel_to_mm_ratio) if int(
        position[1] - roi_size / 2 * pixel_to_mm_ratio) > 0 else 0
    roi_max_y = int(position[1] + roi_size / 2 * pixel_to_mm_ratio) if int(
        position[1] + roi_size / 2 * pixel_to_mm_ratio) < img.shape[1] else img.shape[1]

    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    roi = np.zeros((roi_max_y - roi_min_y, roi_max_x - roi_min_x, 3))
    roi[:, :, 0] = 255

    img_rgb[roi_min_y:roi_max_y, roi_min_x:roi_max_x] = roi

    return img_rgb


if __name__ == "__main__":
    # test
    img = image_generator.generate_image(512, 512)
    state = State(img, (0, 256), 0, 1, (1, 256))
    hash = state.__hash__()
    print(state)

    image_generator.show_image(paint_state(img, (0, 256), 0, 1, 50))
