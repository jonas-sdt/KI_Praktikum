# import numpy as np
#
# from constants import ELECTRODE1, ELECTRODE2, WIRE
#
#
# class State:
#     def __init__(self, image, position: tuple, orientation: int, pixel_to_mm_ratio: float):
#         self.state_matrix = np.zeros((5, 5))
#         self.position = position
#         self.orientation = orientation
#         self.pixel_to_mm_ratio = pixel_to_mm_ratio
#         self.update_state_matrix(image)
#         self.add_electrods()
#
#     def update_state_matrix(self, image):
#         """
#         This method "cuts out" a 5x5 matrix from the image around the current position
#         :param image:
#         """
#         row, col = self.position
#         half_size = 2  # Half the size of the state matrix
#
#         # Calculate the range of rows and columns to extract from the image
#         start_row = max(0, row - half_size)
#         end_row = min(image.shape[0], row + half_size + 1)
#         start_col = max(0, col - half_size)
#         end_col = min(image.shape[1], col + half_size + 1)
#
#         # Extract the relevant portion from the image
#         extracted_matrix = image[start_row:end_row, start_col:end_col]
#
#         # Update the state matrix with the extracted values
#         self.state_matrix[:extracted_matrix.shape[0], :extracted_matrix.shape[1]] = extracted_matrix
#
#     def add_electrods(self):
#         """
#         This method adds the electrodes to the state matrix by placing them according to the orientation of the robot
#         """
#         orientations_to_positions = {
#             0: ((0, 2), (4, 2)),
#             45: ((0, 0), (4, 4)),
#             90: ((2, 0), (2, 4)),
#             135: ((4, 0), (0, 4)),
#             180: ((4, 2), (0, 2)),
#             225: ((4, 4), (0, 0)),
#             270: ((2, 4), (2, 0)),
#             315: ((0, 4), (4, 0))
#         }
#
#         if self.orientation in orientations_to_positions:
#             pos1, pos2 = orientations_to_positions[self.orientation]
#             self.state_matrix[pos1] = self.state_matrix[pos1] + ELECTRODE1
#             self.state_matrix[pos2] = self.state_matrix[pos1] + ELECTRODE2
#         else:
#             raise ValueError("Invalid orientation value: {}".format(self.orientation))
#
#     def is_collided(self):
#         """
#         This method checks if the robot is collided with an object in the environment by checking if any of the
#         electrodes are touching a white pixel
#         :return: True if the robot is collided, False otherwise
#         """
#
#         # return true if there is no wire in the state matrix
#         if not np.any(self.state_matrix == WIRE):
#             return True
#
#         return np.any(self.state_matrix == ELECTRODE1 + WIRE) or np.any(self.state_matrix == ELECTRODE2 + WIRE)
#
#     def to_bytes(self):
#         """
#         This method converts the state matrix to a byte array
#         :return: A byte array representing the state matrix
#         """
#         return self.state_matrix.tobytes()
#
#     def __hash__(self):
#         return hash(self.state_matrix.data.tobytes())
#
#     def __eq__(self, other):
#         # return np.array_equal(self.state_matrix, other.state_matrix)
#         return hash(self) == hash(other)
