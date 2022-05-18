# -*- coding: utf-8 -*-

from os import startfile
import mediapipe as mp
import cv2
import math
import Recogize_text

class Gesture() :

    # hand_landmark에서의 손가락 좌표는 0.0~1.0
    # 화면의 비율에 맞게 수정하기 위한 ratio
    window_x = 0
    window_y = 0

    # 기울기, y 절편
    incline = 0
    intercept = 0

    start = ()
    end = ()

    def set_window_xy(self, x, y):
        self.window_x = x
        self.window_y = y
    
    # 손가락 검지에 대응하는 직선 방정식 구하기
    def Make_equation(self,img, finger7_x, finger7_y, finger8_x, finger8_y):
  
        # y = ax + b
        # incline = a , intercept = b

        self.incline = (finger8_y - finger7_y) / (finger8_x - finger7_x)
        self.intercept = (-1) * (self.incline * finger7_x) + finger7_y
        
        self.start = (finger7_x, finger7_y)

        # text 찾기용
        if finger7_x < finger8_x :
            self.end = (self.window_x , self.window_x*self.incline + self.intercept)
        elif finger7_x > finger8_x :
            self.end = (1,  self.incline + self.intercept) 
        else:
            if finger7_y < finger8_y:
                self.end = (finger7_x, 1)
            else:
                self.end = (finger7_x, self.window_y)
        
        # 그리기용
        #if int(finger8_y) - int(finger7_y) == 0 :
        #    return
    
        #a = int((finger8_y - finger7_y) / (finger8_x - finger7_x))
        #b = int((-1) * (a * finger7_x) + finger7_y)

        #print("Draw : ")
        #print("y = %d x + %d"%(a,b))
        #print()

        #finger7_x = int(finger7_x)
        #finger7_y = int(finger7_y)
    
        #finger8_x = int(finger8_x)
        #finger8_y = int(finger8_y)
   
        #draw_start = (finger7_x, finger7_y)
        #draw_end = ()
        #if finger7_x < finger8_x :
        #    draw_end = (self.window_x , self.window_x*a + b)
        #elif finger7_x > finger8_x :
        #    draw_end = (1,  a + b) 
        #else:
        #    if finger7_y < finger8_y:
        #        draw_end = (finger7_x, 1)
        #    else:
        #        draw_end = (finger7_x, self.window_y)
                
        #cv2.line(img,draw_start,draw_end,(255,255,0),1,cv2.LINE_4,0)
        

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

        # 검지 손가락이 접혀 있으면 return
        if sec_dist < sec_std_dist :
            return

        # 3,4,5 번째 손가락이 접혀있다면 DrawLine(Text 인식)
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


        
        # 가리키는 손동작이라면 진행        
        if point_out_something :     
            
            
            finger8_x = hand_landmarks.landmark[8].x * self.window_x
            finger8_y = hand_landmarks.landmark[8].y * self.window_y
            finger7_x = hand_landmarks.landmark[7].x * self.window_x
            finger7_y = hand_landmarks.landmark[7].y * self.window_y
               
        
            self.Make_equation(image,finger7_x,finger7_y,finger8_x,finger8_y)
 

            tx.DetectText(image,self.incline,self.intercept, self.start, self.end)
        else :
            tx.clear_word()
        