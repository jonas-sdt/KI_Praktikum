import cv2
import numpy as np

from action import Action
from action import Distance
from constants import WIRE, NO_WIRE
from state import State
from skimage import segmentation


class Environment:
    def __init__(self, image: np.array, pixel_to_mm_ratio):
        cv2.namedWindow("display", cv2.WINDOW_NORMAL)

        self.position = (256, 0)  # TODO: Change to start position

        self.end_position = (256, 511)
        self.orientation = 0

        self.image = image

        self.segmented_image = image.copy()
        self.segment_image()

        self.__current_target_position = (256, 0)
        self.state = State(self.position, self.orientation, self.__current_target_position, self.segmented_image)
        self.__last_distance_to_target = 0
        self.__current_distance_to_target = 0
        self.old_targets = []
        self.old_target_reached = False
        self.__last_position = (256, 0)
        self.__first_action = True
        self.update_target()

    def show_image(self):
        # Mark the current position of the agent in the image
        marked_image = self.image.copy()
        # Convert the image to 8-bit depth
        marked_image = cv2.normalize(marked_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # Convert the image to RGB
        marked_image = cv2.cvtColor(marked_image, cv2.COLOR_GRAY2RGB)
        image_position = (self.position[1], self.position[0])
        marked_image = cv2.circle(marked_image, image_position, radius=0, color=(0, 0, 255), thickness=2)

        # Add a line to the image to show the orientation of the agent
        # Calculate the end point of the line
        end_point = (int(image_position[0] + 10 * np.cos(np.deg2rad(self.orientation))),
                     int(image_position[1] + 10 * (-np.sin(np.deg2rad(self.orientation)))))
        marked_image = cv2.line(marked_image, image_position, end_point, color=(0, 0, 255), thickness=1)

        # Show the image
        cv2.imshow('display', marked_image)
        # Update the window
        cv2.waitKey(1)

    def do_action(self, action):
        # action is a tuple of (x, y, orientation)
        self.position = (self.position[0] + action.value[0], self.position[1] + action.value[1])

        # Check if the agent is out of bounds
        if self.position[0] < 0 or self.position[0] >= self.image.shape[0] or self.position[1] < 0 or self.position[
            1] >= self.image.shape[1]:
            self.position = self.__last_position
            return True
        self.__last_position = self.position

        self.orientation = (self.orientation + action.value[2]) % 360
        self.update_target()
        self.state = State(self.position, self.orientation, self.__current_target_position, self.segmented_image)
        self.__first_action = False
        self.show_image()

        return False

    def check_end_position(self):
        if self.position == self.end_position or self.position == (self.end_position[0] - 1, self.end_position[1]):
            return True
        else:
            return False

    def update_target(self):
        """
        This method checks in a 5x5 area around the agent for the nearest pixel with the value WIRE
        """
        # If the target is already found, return
        if self.position != self.__current_target_position:
            self.old_target_reached = False
            return

        self.old_targets.append(self.__current_target_position)

        area = np.zeros((5, 5))

        for i in range(5):
            for j in range(5):
                # Check if value is out of bounds
                if self.position[0] - 2 + i < 0 or self.position[0] - 2 + i >= self.image.shape[0] or self.position[
                    1] - 2 + j < 0 or self.position[1] - 2 + j >= self.image.shape[1]:
                    area[i][j] = 0
                else:
                    area[i][j] = self.image[self.position[0] - 2 + i, self.position[1] - 2 + j]

        # Get the indices of the pixels with the value WIRE
        indices = np.where(area == WIRE)

        # If there are no pixels with the value WIRE, return
        if len(indices[0]) == 0:
            return

        indices = []
        # Get the indeces of the pixel with the value WIRE that is in the area around the agent
        for i in range(len(area)):
            for j in range(len(area[i])):
                if area[i][j] == WIRE:
                    indices.append((i, j))

        # Sort the indices according to the distance to the agent

        indx_with_distance = {}
        for index in indices:
            distance = np.sqrt((index[0] - 2) ** 2 + (index[1] - 2) ** 2)
            indx_with_distance[index] = distance

        sorted_indices = sorted(indx_with_distance.items(), key=lambda x: x[1])

        # Iterate over the indx_with_distance until there is an index that is not in the old targets
        for index in sorted_indices:
            pos = (self.position[0] - 2 + index[0][0], self.position[1] - 2 + index[0][1])
            if pos not in self.old_targets:
                self.__current_target_position = pos
                break

        self.__current_distance_to_target = 0
        self.__last_distance_to_target = self.__current_distance_to_target
        self.old_target_reached = True

    def update_distance_to_target(self):
        """
        This method calculates the distance to the target
        """
        self.__current_distance_to_target = np.sqrt((self.position[0] - self.__current_target_position[0]) ** 2 + (
                self.position[1] - self.__current_target_position[1]) ** 2)
        value_to_return = None

        if self.__current_distance_to_target < self.__last_distance_to_target:
            value_to_return = Distance.CLOSER
        elif self.__current_distance_to_target > self.__last_distance_to_target:
            value_to_return = Distance.FARTHER
        else:
            value_to_return = Distance.SAME

        self.__last_distance_to_target = self.__current_distance_to_target

        return value_to_return

    def segment_image(self):
        self.segmented_image = segmentation.flood_fill(self.segmented_image, (0, 0), 3, connectivity=1)
        self.segmented_image = segmentation.flood_fill(self.segmented_image, (511, 511), 4, connectivity=1)
