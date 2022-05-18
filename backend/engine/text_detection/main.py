# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import Detect_gesture
import Recogize_text

def start_Text(filename) :

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    image = cv2.imread(filename) 
   
    
     # gesture
    gs = Detect_gesture.Gesture()
    # text
    tx = Recogize_text.Text()

    # 화면 비율
    window_y, window_x, c = image.shape
    
    
    window_y = window_y/2
    window_x = window_x/2

    image = cv2.resize(image, dsize=(int(window_x), int(window_y)), interpolation=cv2.INTER_AREA)
  
    gs.set_window_xy(window_x, window_y)


    with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
 
    

        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
   
        results = hands.process(image)
  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                # 손모양이 뭔지
                gs.Whatgesture(image,hand_landmarks,tx)

                 # 손 뼈대 Drawing
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                   
                
                if tx.is_detected():
<<<<<<< Updated upstream
                    detected_word = tx.return_word()
                    print(detected_word)
                    return detected_word


                # mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

=======
                    detected_Word = tx.return_word()
                    
                    #print(detected_Word)
                    #cv2.imshow('image', image)
                    #cv2.waitKey(0)
                    return detected_Word
>>>>>>> Stashed changes

               
        #cv2.imshow('image', image)
        #cv2.waitKey(0)
    
        
if __name__ == "__main__":
    detected_word = start_Text("major1.jpg")
    print(detected_word)