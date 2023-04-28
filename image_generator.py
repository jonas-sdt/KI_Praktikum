import cv2
import numpy as np
import random
from spline import spline as generate_spline
import os

""" This class is responsible to generate a black image with a spline drawn on it.
"""
class ImageGenerator:
    
    def __init__(self, width: int, height: int):

        # Create a black background image
        self.height = height
        self.width = width
        self.img = np.zeros((self.height, self.width, 1), np.uint8)
        
    def generate_image(self):
        
        spline = generate_spline(self.width, self.height)
        
        # Create a black background image
        self.img = np.zeros((self.height, self.width, 1), np.uint8)
        
        # Draw the spline
        self.img = cv2.polylines(self.img, [np.int32(spline)], False, (255, 255, 255))
        
        return self.img

    def show_image(self):
        
        # Display the image
        cv2.imshow('Generated Image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self):
        path = os.getcwd()
        cv2.imwrite(path + '/training_images/image.png', self.img)


if __name__ == '__main__':
    img_gen = ImageGenerator(512, 512)
    img_gen.generate_image()
    img_gen.show_image()
    img_gen.save_image()