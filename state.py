import numpy as np

# For now the class still uses the old attributes. Change later, when the new attributes (nxn array) are implemented.
class State:
    def __init__(self, image, position: tuple, orientation: int, pixel_to_mm_ratio: float):
        
        roi_size = 50 # in mm
        self.matrix = np.zeros((5,5))
        
        roi = image[int(position[0]-roi_size/2*pixel_to_mm_ratio):int(position[0]+roi_size/2*pixel_to_mm_ratio)][int(position[1]-roi_size/2*pixel_to_mm_ratio):int(position[1]+roi_size/2*pixel_to_mm_ratio)]
        
        num_of_pixels_vert = roi.shape[0]
        num_of_pixels_hor = roi.shape[1]
        
        # add wire to matrix from image so that 1 entry in the matrix equals 1cm
        for row in range(5):
            for col in range(5):

                # check if area in roi is wire
                if np.sum(roi[int(row*num_of_pixels_vert/5):int((row+1)*num_of_pixels_vert/5)][int(col*num_of_pixels_hor/5):int((col+1)*num_of_pixels_hor/5)]) > 0:
                    self.matrix[row][col] = 1

        if orientation % 180 == 0:
            self.matrix[0][2] = 2 if self.matrix[0][2] == 0 else 3
            self.matrix[4][2] = 2 if self.matrix[4][2] == 0 else 3
        elif orientation % 180 == 45:
            self.matrix[4][0] = 2 if self.matrix[4][0] == 0 else 3
            self.matrix[0][4] = 2 if self.matrix[0][4] == 0 else 3
        elif orientation % 180 == 90:
            self.matrix[0][2] = 2 if self.matrix[0][2] == 0 else 3
            self.matrix[4][2] = 2 if self.matrix[4][2] == 0 else 3
        elif orientation % 180 == 135:
            self.matrix[0][0] = 2 if self.matrix[0][0] == 0 else 3
            self.matrix[4][4] == 2 if self.matrix[4][4] == 0 else 3 

    def is_collided(self):
        return 3 in self.matrix

    def __hash__(self):
        return hash(self.matrix)

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.__hash__() == other.__hash__()


if __name__ == "__main__":
    # test
    state = State(np.zeros((100,100)), (50,50), 0, 1)