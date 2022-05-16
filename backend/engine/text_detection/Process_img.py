# -*- coding: cp949 -*-
import cv2
import numpy as np
from scipy.ndimage import interpolation as inter

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


    #Skew Correction
    def correct_skew(image, delta=1, limit=5):
        def determine_score(arr, angle):
            data = inter.rotate(arr, angle, reshape=False, order=0)
            histogram = np.sum(data, axis=1)
            score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
            return histogram, score

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

        scores = []
        angles = np.arange(-limit, limit + delta, delta)
        for angle in angles:
            histogram, score = determine_score(thresh, angle)
            scores.append(score)

        best_angle = angles[scores.index(max(scores))]

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
                  borderMode=cv2.BORDER_REPLICATE)
        #print("The Rotation angle is: ", best_angle)
        return rotated

    # Increase Brightness
    def checkDayOrNight(img, thrshld):
        is_light = np.mean(img) > thrshld
        return 0 if is_light else 1 # 0 --> light and 1 -->dark

    def increaseBrightness(img):
        alpha = 1 
        beta = 40
        img=cv2.addWeighted(img, alpha,np.zeros(img.shape,img.dtype), 0 ,beta)
        return img

    def threshold(img):
        # Various thresholding method
        img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  
        img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        img = cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        img = cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        return img

      #Noise reduction
    def noise_removal(img):
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        return img

