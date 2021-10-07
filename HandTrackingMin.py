import cv2
import numpy as np
import mediapipe as mp
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils
curTime = 0
prevTime = 0
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    # converting the img into RGB image
    imgRgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # processing the frame
    results = hands.process(imgRgb)

    curTime = time.time()
    fps = 1/(curTime-prevTime)
    prevTime = curTime

    cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_ITALIC,3,(255,0,255),3)

    if results.multi_hand_landmarks:
        for handLandMark in results.multi_hand_landmarks:
            for id,lm in enumerate(handLandMark.landmark):
               h,w,c = img.shape
               cx, cy = int(lm.x*w), int (lm.y*h)
               print(id, cx,cy) # printing the pixels

               # if we want to to some stuffs on a p erticular landmark
               if id ==0:
                   cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

            mpdraw.draw_landmarks(img, handLandMark, mpHands.HAND_CONNECTIONS)

    cv2.imshow('Camera',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break