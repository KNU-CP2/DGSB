# -*- coding: utf-8 -*-

import mediapipe as mp
import cv2
import math
from .Recogize_text import *

class Gesture() :

    window_x = 0
    window_y = 0

    incline = 0
    intercept = 0

    start = ()
    end = ()

    def set_window_xy(self, x, y):
        self.window_x = x
        self.window_y = y

    def Make_equation(self,img, finger7_x, finger7_y, finger8_x, finger8_y):
  
        # y = ax + b
        # incline = a , intercept = b

        self.incline = (finger8_y - finger7_y) / (finger8_x - finger7_x)
        self.intercept = (-1) * (self.incline * finger7_x) + finger7_y
        
        self.start = (finger7_x, finger7_y)

        if finger7_x < finger8_x :
            self.end = (self.window_x , self.window_x*self.incline + self.intercept)
        elif finger7_x > finger8_x :
            self.end = (1,  self.incline + self.intercept) 
        else:
            if finger7_y < finger8_y:
                self.end = (finger7_x, 1)
            else:
                self.end = (finger7_x, self.window_y)
        

    # Return distacne between two coordinates
    def dist(self,x1, y1 ,x2 ,y2):
        return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
 

    def Whatgesture(self,image, hand_landmarks, tx):
    
        point_out_something = True

        wrist_x = hand_landmarks.landmark[0].x
        wrist_y = hand_landmarks.landmark[0].y

        sec_x = hand_landmarks.landmark[8].x
        sec_y = hand_landmarks.landmark[8].y
        sec_std_x = hand_landmarks.landmark[6].x
        sec_std_y = hand_landmarks.landmark[6].y

        sec_dist = self.dist(sec_x,sec_y, wrist_x,wrist_y)
        sec_std_dist = self.dist(sec_std_x,sec_std_y, wrist_x,wrist_y)

        if sec_dist < sec_std_dist :
            return

        tip_pos = 12
        std_pos = 10
        
        for i in range(0,3):
            tip_x = hand_landmarks.landmark[tip_pos].x
            tip_y = hand_landmarks.landmark[tip_pos].y
            std_x = hand_landmarks.landmark[std_pos].x
            std_y = hand_landmarks.landmark[std_pos].y

            tip_dist = self.dist(tip_x,tip_y,wrist_x,wrist_y)
            std_dist = self.dist(std_x,std_y,wrist_x,wrist_y)

            if tip_dist > std_dist :
                point_out_something = False
                break
            tip_pos = tip_pos + 4
            std_pos = std_pos + 4



        if point_out_something :     
            
            
            finger8_x = hand_landmarks.landmark[8].x * self.window_x
            finger8_y = hand_landmarks.landmark[8].y * self.window_y
            finger7_x = hand_landmarks.landmark[7].x * self.window_x
            finger7_y = hand_landmarks.landmark[7].y * self.window_y
               
        
            self.Make_equation(image,finger7_x,finger7_y,finger8_x,finger8_y)
 

            tx.DetectText(image,self.incline,self.intercept, self.start, self.end)
        else :
            tx.clear_word()
        