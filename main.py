#! /usr/bin/env python
# -*- coding: utf-8 -*-

from cv2 import cv2
import numpy as np
#from server import Server

class Computer_vision:
    def __init__(self):
        self.video = cv2.VideoCapture('video_cv.mp4')
        
        #self.server = Server('192.168.7.24', 9090)

        #if not self.video.isOpened:
        #    print('Error in file')
        #    return

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

            try:
                self.binary()
            except:
                print("change mode: manual")
                res = self.change_mode()
                if not res:
                    break

    # Бинаризация по синему каналу (в cv2 изображения изначально в BGR пространстве)
    def binary(self):
        threshold = 180  #porog
        binary_image_temp = self.resized[:,:,0]
        binary_image = np.zeros_like(binary_image_temp)
        binary_image[(binary_image_temp > threshold)] = 255
        #cv2.imshow("video2", binary_image)

        # Перевод в HLS пространство, регулирует порог светлости пикселей. 
        resized_hls = cv2.cvtColor(self.resized, cv2.COLOR_BGR2HLS)
        binary_image_temp_2 = resized_hls[:,:,0]
        binary_image2 = np.zeros_like(binary_image_temp_2)
        binary_image2[(binary_image_temp_2 > threshold)] = 255

        self.allBinary = np.zeros_like(binary_image)
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
        self.perspective = cv2.warpPerspective(self.allBinary, perspective_temp, (self.video_width, self.video_height), flags = cv2.INTER_LINEAR)
        cv2.imshow("perspective", self.perspective)

        self.search_white_pixels()

    # Поиск белых пикселей на изображении и выделение линий разметки
    def search_white_pixels(self):
        summ = np.sum(self.perspective[self.perspective.shape[0]//2:,:], axis = 0)
        half_of_summ = summ.shape[0] // 2
        index_whitepixels_l = np.argmax(summ[:half_of_summ])    # поиск самого белого столбца исходя из суммы цветных кодировок
        index_whitepixels_r = np.argmax(summ[half_of_summ:]) + half_of_summ    #argmax returns index in the array

        self.index_l = np.array([], dtype = np.int16)    # массив с координатами белых пикселей,
        self.index_r = np.array([], dtype = np.int16)    # принадлежащих разметке

        array_of_whitepixels = self.perspective.nonzero()     # индексы пикселей - их координаты
        self.white_pixels_y = np.array(array_of_whitepixels[0])    # получение индексов белых пикселей по строкам
        self.white_pixels_x = np.array(array_of_whitepixels[1])    # по столбцам

        # Создание цветного изображения, т.к. self.perspective кодирует цвета 1 числом
        self.out_image = np.dstack((self.perspective, self.perspective, self.perspective))

        amount_windows = 10      # кол-во окон
        half_of_window = 20     
        center_l = index_whitepixels_l      # абсцисса самого белого столбца в изображении
        center_r = index_whitepixels_r
        window_height = np.int(self.perspective.shape[0]/amount_windows)
        
        for window in range(amount_windows):
            # координаты прямоугольников в левой и правой частях
            y1 = self.perspective.shape[0] - (window + 1)*window_height
            y2 = self.perspective.shape[0] - window*window_height
            x1_l = center_l - half_of_window
            x2_l = center_l + half_of_window
            x1_r = center_r - half_of_window
            x2_r = center_r + half_of_window
            
            # индексы пикселей, попавших в окно, из массива координат всех белых пикселей
            index_needful_l = ((self.white_pixels_y >= y1)&(self.white_pixels_y <= y2)&
                (self.white_pixels_x >= x1_l)&(self.white_pixels_x <= x2_l)).nonzero()[0]
            index_needful_r = ((self.white_pixels_y >= y1)&(self.white_pixels_y <= y2)&
                (self.white_pixels_x >= x1_r)&(self.white_pixels_x <= x2_r)).nonzero()[0]
            
            # переопределение абсциссы центра последующего окна (среднее зачение абсцисс
            # белых пикселей разметки); необходимо для смещения окна
            # проверка на кол-во пикселей обязательна, т.к. пикселей в окне может не оказаться и будет valueerror
            if len(index_needful_l) > 0:
                center_l = np.int(np.mean(self.white_pixels_x[index_needful_l]))
            if len(index_needful_r) > 0:
                center_r = np.int(np.mean(self.white_pixels_x[index_needful_r]))

            cv2.rectangle(self.out_image, (x1_l, y1), (x2_l, y2), (0, 0, 255), 1)
            cv2.rectangle(self.out_image, (x1_r, y1), (x2_r, y2), (0, 0, 255), 1)
            cv2.imshow("out", self.out_image)

            self.index_l = np.concatenate((self.index_l, index_needful_l))    # здесь собираются конечные индексы
            self.index_r = np.concatenate((self.index_r, index_needful_r))

        self.center_line()

    def center_line(self):
        # вычисление координат всех относящихся к разметке пикселей
        x_l = self.white_pixels_x[self.index_l]
        y_l = self.white_pixels_y[self.index_l]
        x_r = self.white_pixels_x[self.index_r]
        y_r = self.white_pixels_y[self.index_r]

        line_left = np.polyfit(y_l, x_l, 2)     # x и y перепутаны: в цикле мы итерируемся построчно,
        line_right = np.polyfit(y_r, x_r, 2)    # поэтому при вычислении точки мы будем знать ее y-координату
        line_center = ((line_left + line_right) / 2)
        coord2points = []

        for line in range(self.out_image.shape[0]):
            point = ((line_center[0]) * (line**2) + line_center[1] * line + line_center[2])     # x = ay^2 + by + c
            if line == 0 or line == self.out_image.shape[0]-1:
                coord2points.append(point)
            cv2.circle(self.out_image, (int(point), int(line)), 2, (50, 200, 150), 1)

        if abs(coord2points[0] - coord2points[1]) < 20:
            print("вперед")
            pass
        elif (coord2points[0] - coord2points[1]) < 0:
            print("налево")
            pass
        else:
            print("направо")
            pass
            
        cv2.imshow("center line", self.out_image)
        
    def change_mode(self):
        cond = self.server.start()
        if cond:
            print("change mode: auto")
            return True
        
        print("completion")
        return False


a = Computer_vision()
