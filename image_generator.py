import cv2
import numpy as np
from spline import spline as generate_spline
import os
        
def generate_image(width, height):

    spline = generate_spline(width, height)
    
    # Create a black background image
    img = np.zeros((height, width, 1), np.uint8)
    
    # Draw the spline
    img = cv2.polylines(img, [np.int32(spline)], False, (255, 255, 255))

    return img[:,:,0] / 255

def show_image(img):
    # Display the image
    cv2.imshow('Generated Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image(img):
    path = os.getcwd()
    cv2.imwrite(path + '/training_images/image.png', img)

if __name__ == '__main__':
    for img in generate_image(2, 512, 512):
        show_image(img)