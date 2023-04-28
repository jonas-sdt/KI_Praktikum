# Method that takes an image at the time using opencv
import datetime
import os

import cv2

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"


def take_image():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    if not ret:
        print("Unable to capture video")
        return None
    cap.release()
    return frame


def save_image(img):
    time = datetime.datetime.now()
    path_to_save = os.getcwd() + "\\real_images"
    cv2.imwrite(f"{path_to_save}\\image_{str(time.date())}_{time.hour}_{time.minute}_{time.second}.png", img)

    print(type(img))
    cv2.imshow('image', img)
    cv2.waitKey(0)

    print("Image saved at: " + path_to_save + "\\image_" + str(time) + ".png")


if __name__ == '__main__':
    img = take_image()
    save_image(img)
