# -*- coding: cp949 -*-
import cv2
import numpy as np
# from scipy.ndimage import interpolation as inter

#open source exmaple 사용해보기
# 나중에 이해해야됨

class ProcessImage:

    def extract_for_Color(image):
        img_ycrcb = cv2.cvtColor(image,cv2.COLOR_BGR2YCrCb)
        ycrcb_list = cv2.split(img_ycrcb)
        ycrcb_list = list(ycrcb_list)
        ycrcb_list[0] = cv2.equalizeHist(ycrcb_list[0])
        des_img = cv2.merge(ycrcb_list)
        des_img = cv2.cvtColor(des_img,cv2.COLOR_YCrCb2BGR)
        return des_img

    def extract_for_Gray(image):
        gry_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        Hist_img = cv2.equalizeHist(gry_img)
        return Hist_img

