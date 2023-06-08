import numpy as np
import image_generator
import cv2
from constants import *

# For now the class still uses the old attributes. Change later, when the new attributes (nxn array) are implemented.
class State:
    def __init__(self, image, position: tuple, orientation: int, pixel_to_mm_ratio: float, local_goal_position: tuple):

        position = (int(position[1]), int(position[0])) # I did little "pfusch" here, because I don't want to change the whole code :D

        if len(image.shape) != 2:
            raise ValueError("Image must be a 2D array")
                
        self.orientation = orientation
        
        roi_size = 50 # in mm
        self.matrix = np.zeros((5,5))
        
        # calculate indices of ROI
        roi_min_x = int(position[0] - roi_size/2*pixel_to_mm_ratio)
        roi_max_x = int(position[0] + roi_size/2*pixel_to_mm_ratio)
        roi_min_y = int(position[1] - roi_size/2*pixel_to_mm_ratio)
        roi_max_y = int(position[1] + roi_size/2*pixel_to_mm_ratio)

        # check if ROI goes beyond image boundaries
        if roi_min_x < 0 or roi_max_x > image.shape[1] or roi_min_y < 0 or roi_max_y > image.shape[0]:
            roi = np.zeros((roi_size, roi_size))
            
            # calculate number of pixels that go beyond image boundaries
            out_of_bounds_x_min = 0 if roi_min_x >= 0 else -roi_min_x
            out_of_bounds_x_max = 0 if roi_max_x <= image.shape[1] else roi_max_x - image.shape[1]
            out_of_bounds_y_min = 0 if roi_min_y >= 0 else -roi_min_y
            out_of_bounds_y_max = 0 if roi_max_y <= image.shape[0] else roi_max_y - image.shape[0]
            
            # calculate indices of ROI for this row and column
            roi_min_row = int(out_of_bounds_y_min)
            roi_max_row = int(roi_size - out_of_bounds_y_max)
            roi_min_col = int(out_of_bounds_x_min)
            roi_max_col = int(roi_size - out_of_bounds_x_max)

            roi[roi_min_row:roi_max_row, roi_min_col:roi_max_col] = image[roi_min_y if roi_min_y>=0 else 0:roi_max_y if roi_max_y<=image.shape[0] else image.shape[0], roi_min_x if roi_min_x>=0 else 0:roi_max_x if roi_max_x<=image.shape[1] else image.shape[1]]
        else:
            roi = image[roi_min_y:roi_max_y, roi_min_x:roi_max_x]

        num_of_pixels_vert = roi.shape[0]
        num_of_pixels_hor = roi.shape[1]
        
        # add wire to matrix from image so that 1 entry in the matrix equals 1cm
        for row in range(5):
            for col in range(5):

                # calculate indices of ROI for this row and column
                roi_min_row = int(row*num_of_pixels_vert/5)
                roi_max_row = int((row+1)*num_of_pixels_vert/5)
                roi_min_col = int(col*num_of_pixels_hor/5)
                roi_max_col = int((col+1)*num_of_pixels_hor/5)

                # check if area in roi is wire
                if np.sum(roi[roi_min_row:roi_max_row, roi_min_col:roi_max_col]) > 0:
                    self.matrix[row][col] = 1

        if orientation % 180 == 0:
            self.matrix[0][2] = ELECTRODE_1 if self.matrix[0][2] == NO_WIRE else COLLISION
            self.matrix[4][2] = ELECTRODE_2 if self.matrix[4][2] == NO_WIRE else COLLISION
        elif orientation % 180 == 45:
            self.matrix[4][0] = ELECTRODE_1 if self.matrix[4][0] == NO_WIRE else COLLISION
            self.matrix[0][4] = ELECTRODE_2 if self.matrix[0][4] == NO_WIRE else COLLISION
        elif orientation % 180 == 90:
            self.matrix[2][0] = ELECTRODE_1 if self.matrix[2][0] == NO_WIRE else COLLISION
            self.matrix[2][4] = ELECTRODE_2 if self.matrix[2][4] == NO_WIRE else COLLISION
        elif orientation % 180 == 135:
            self.matrix[0][0] = ELECTRODE_1 if self.matrix[0][0] == NO_WIRE else COLLISION
            self.matrix[4][4] = ELECTRODE_2 if self.matrix[4][4] == NO_WIRE else COLLISION 
            
        # add local goal to matrix
        # TODO

    def is_collided(self):
        # detect if wire is in between the two electrodes. if not, electrodes must have collided
        if self.orientation % 180 == 0:
            if np.sum(self.matrix[1:3,2]) == 0:
                return True
        elif self.orientation % 180 == 45:
            if np.sum(self.matrix[1:3,1:3]) == 0:
                return True
        elif self.orientation % 180 == 90:
            if np.sum(self.matrix[2,1:3]) == 0:
                return True
        elif self.orientation % 180 == 135:
            if np.sum(self.matrix[2:4,1:3]) == 0:
                return True
        else:
            return 3 in self.matrix
    
    def __str__(self) -> str:
        # replace 1 with "w", 2 with "e" and 3 with "c"
        matrix_str = np.array(self.matrix, dtype=str)
        matrix_str = np.where(matrix_str == "1.0", "w", matrix_str)
        matrix_str = np.where(matrix_str == "4.0", "e", matrix_str)
        matrix_str = np.where(matrix_str == "5.0", "E", matrix_str)
        matrix_str = np.where(matrix_str == "3.0", "c", matrix_str)
        matrix_str = np.where(matrix_str == "0.0", " ", matrix_str)
        
        print_str = ""
        print_str += str((5*4+1)*"-")
        print_str += str("\n")

        for i in range(5):
            for j in range(5):
                print_str += str(f"| {matrix_str[i][j]} ")
            print_str += str("| \n")
            print_str += str((5*4+1)*"-")
            print_str += str("\n")
        
        return print_str
    
    def __hash__(self):
        return hash(self.matrix.data.tobytes())

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.__hash__() == other.__hash__()

    # Added, because we want to save only the matrix hash in the q table and not the instance itself
    def get_hash(self):
        return hash(self.matrix.data.tobytes())

def paint_state(img, position, orientation, pixel_to_mm_ratio, roi_size):
    # paint square around position in image
    roi_min_x = int(position[0] - roi_size/2*pixel_to_mm_ratio) if int(position[0] - roi_size/2*pixel_to_mm_ratio) > 0 else 0
    roi_max_x = int(position[0] + roi_size/2*pixel_to_mm_ratio) if int(position[0] + roi_size/2*pixel_to_mm_ratio) < img.shape[0] else img.shape[0]
    roi_min_y = int(position[1] - roi_size/2*pixel_to_mm_ratio) if int(position[1] - roi_size/2*pixel_to_mm_ratio) > 0 else 0
    roi_max_y = int(position[1] + roi_size/2*pixel_to_mm_ratio) if int(position[1] + roi_size/2*pixel_to_mm_ratio) < img.shape[1] else img.shape[1]

    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    roi = np.zeros((roi_max_y - roi_min_y, roi_max_x - roi_min_x, 3))
    roi[:,:,0] = 255

    img_rgb[roi_min_y:roi_max_y, roi_min_x:roi_max_x] = roi

    return img_rgb

if __name__ == "__main__":
    # test
    img = image_generator.generate_image(512,512)
    state = State(img, (0,256), 0, 1, (1,256))
    hash = state.__hash__()
    print(state)


    image_generator.show_image(paint_state(img, (0,256), 0, 1, 50))
