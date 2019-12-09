import numpy as np
import cv2

class Computer_vision:
    def __init__(self):
        self.video = cv2.VideoCapture('video_cv.mp4')

        if self.video.isOpened == False:
            print('Error in file')
            return

        video_width = 360
        video_height = 200