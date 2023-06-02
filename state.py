# import numpy as np
# from image_generator import ImageGenerator
# # TODO: fix wire detection
# # TODO: implement fct for detecting out of bounds
#
# # For now the class still uses the old attributes. Change later, when the new attributes (nxn array) are implemented.
# class State:
#     def __init__(self, image, position: tuple, orientation: int, pixel_to_mm_ratio: float):
#
#         roi_size = 50 # in mm
#         self.matrix = np.zeros((5,5))
#
#         # two different ways of getting the roi
#         roi = image[int(position[0]-roi_size/2*pixel_to_mm_ratio):int(position[0]+roi_size/2*pixel_to_mm_ratio),int(position[1]-roi_size/2*pixel_to_mm_ratio):int(position[1]+roi_size/2*pixel_to_mm_ratio)]
#         # roi = image[(position[0] - 2):(position[0]+2),(position[1] - 2):(position[1]+2)]
#
#         num_of_pixels_vert = roi.shape[0]
#         num_of_pixels_hor = roi.shape[1]
#
#         # add wire to matrix from image so that 1 entry in the matrix equals 1cm
#         for row in range(5):
#             for col in range(5):
#
#                 # check if area in roi is wire
#                 if np.sum(roi[int(row*num_of_pixels_vert/5):int((row+1)*num_of_pixels_vert/5)][int(col*num_of_pixels_hor/5):int((col+1)*num_of_pixels_hor/5)]) > 0:
#                     self.matrix[row][col] = 1
#
#         if orientation % 180 == 0:
#             self.matrix[0][2] = 2 if self.matrix[0][2] == 0 else 3
#             self.matrix[4][2] = 2 if self.matrix[4][2] == 0 else 3
#         elif orientation % 180 == 45:
#             self.matrix[4][0] = 2 if self.matrix[4][0] == 0 else 3
#             self.matrix[0][4] = 2 if self.matrix[0][4] == 0 else 3
#         elif orientation % 180 == 90:
#             self.matrix[2][0] = 2 if self.matrix[2][0] == 0 else 3
#             self.matrix[2][4] = 2 if self.matrix[2][4] == 0 else 3
#         elif orientation % 180 == 135:
#             self.matrix[0][0] = 2 if self.matrix[0][0] == 0 else 3
#             self.matrix[4][4] = 2 if self.matrix[4][4] == 0 else 3
#
#     def is_collided(self):
#         return 3 in self.matrix
#
#     def __str__(self) -> str:
#         # replace 1 with "w", 2 with "e" and 3 with "c"
#         matrix_str = np.array(self.matrix, dtype=str)
#         matrix_str = np.where(matrix_str == "1.0", "w", matrix_str)
#         matrix_str = np.where(matrix_str == "2.0", "e", matrix_str)
#         matrix_str = np.where(matrix_str == "3.0", "c", matrix_str)
#         matrix_str = np.where(matrix_str == "0.0", " ", matrix_str)
#
#         print_str = ""
#         print_str += str((5*4+1)*"-")
#         print_str += str("\n")
#
#         for i in range(5):
#             for j in range(5):
#                 print_str += str(f"| {matrix_str[i][j]} ")
#             print_str += str("| \n")
#             print_str += str((5*4+1)*"-")
#             print_str += str("\n")
#
#         return print_str
#
#     def __hash__(self):
#         return hash(self.matrix.data.tobytes())
#
#     def __eq__(self, other):
#         if not isinstance(other, State):
#             return False
#         return self.__hash__() == other.__hash__()
#
#
# if __name__ == "__main__":
#     # test
#     img_gen  = ImageGenerator(512,512)
#     img = img_gen.generate_image()
#     state = State(img, (256,256), 0, 1)
#     hash = state.__hash__()
#     print(state)
#     img_gen.show_image()