# -*- coding: cp949 -*-

import cv2
import mediapipe as mp
from .Detect_gesture import Gesture
from .Recogize_text import *

def get_detected_text(file_name):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # cap = cv2.VideoCapture(0)
    image = cv2.imread('raw/'+file_name)

    # gesture
    gs = Gesture()
    # text
    tx = Text()

    with mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        # sx,sy,window_x,window_y = cv2.getWindowImageRect('image')
        window_y, window_x, c = image.shape
        gs.set_window_xy(window_x, window_y)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gs.Whatgesture(image, hand_landmarks, tx)

                if tx.is_detected():
                    detected_word = tx.return_word()
                    print(detected_word)
                    return detected_word


                # mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


if __name__ == "__main__":
    print(get_detected_text())
