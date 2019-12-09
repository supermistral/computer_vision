from cv2 import cv2
import numpy as np

class Computer_vision:
    def __init__(self):
        self.video = cv2.VideoCapture('video_cv.mp4')

        if not self.video.isOpened:
            print('Error in file')
            return

        self.video_width = 360
        self.video_height = 200
        self.start_handler()

    def start_handler(self):
        while cv2.waitKey(1) != 27:
            condition, frame = self.video.read()
            if not condition:
                print("End")
                break
            resized = cv2.resize(frame, (self.video_width, self.video_height))
            cv2.imshow("videooo", resized)

a = Computer_vision()