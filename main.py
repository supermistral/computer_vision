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
        self.figure_pts_0 = np.float32([[20, 200], [60, 120], [300, 120], [340, 200]])
        self.figure_pts = np.array(self.figure_pts_0, dtype = np.int32)
        self.dst = np.float32([[0, self.video_height-1], [0, 0], [self.video_width-1, 0], [self.video_width-1, self.video_height-1]])
        self.start_handler()

    # Чтение ролика покадрово и вывод на экран с бинаризацией
    def start_handler(self):
        while cv2.waitKey(1) != 27:
            condition, frame = self.video.read()
            if not condition:
                print("End")
                break
            self.resized = cv2.resize(frame, (self.video_width, self.video_height))
            cv2.imshow("videooo", self.resized)

            self.binary()

    # Бинаризация по синему каналу (в cv2 изображения изначально в BGR пространстве)
    def binary(self):
        binary_image_temp = self.resized[:,:,0]
        binary_image = np.zeros_like(binary_image_temp)
        binary_image[(binary_image_temp > 200)] = 255
        #cv2.imshow("video2", binary_image)

        #Перевод в HLS пространство, регулирует порог светлости пикселей. 
        resized_hls = cv2.cvtColor(self.resized, cv2.COLOR_BGR2HLS)
        binary_image_temp_2 = resized_hls[:,:,0]
        binary_image2 = np.zeros_like(binary_image_temp_2)
        binary_image2[(binary_image_temp_2 > 200)] = 255

        self.allBinary = np.zeros_like(self.resized)
        self.allBinary[((binary_image == 255)|(binary_image2 == 255))] = 255
        cv2.imshow("binary", self.allBinary)

        self.polyline()
    
    # Масштабирование изображения, чтобы линии разметки попадали в область и находились под прямым углом
    def polyline(self):
        # Рисование линий на холсте, фактически бесполезная вещь
        '''self.allBinary_copy = self.allBinary.copy()
        cv2.polylines(self.allBinary_copy, [self.figure_pts], True, 255) 
        cv2.imshow("line", self.allBinary_copy)'''

        perspective_temp = cv2.getPerspectiveTransform(self.figure_pts_0, self.dst)
        perspective = cv2.warpPerspective(self.allBinary, perspective_temp, (self.video_width, self.video_height), flags = cv2.INTER_LINEAR)
        cv2.imshow("perspective", perspective)

a = Computer_vision()