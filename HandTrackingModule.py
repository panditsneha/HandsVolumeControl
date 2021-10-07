import cv2
import numpy as np
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRgb)

        if self.results.multi_hand_landmarks:
            for handLandMark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handLandMark, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPos(self,img,handNo=0,draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int (lm.y*h)
                lmList.append([id,cx,cy])
                # if we want to to some stuffs on a perticular landmark
                # if draw:
                #     cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
        return lmList
    


def main():
    curTime = 0
    prevTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPos(img)

        if len(lmlist) !=0:
           print(lmlist[4]) 

        curTime = time.time()
        fps = 1/(curTime-prevTime)
        prevTime = curTime

        cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_ITALIC,3,(255,0,255),3)
        cv2.imshow('Camera',img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break


if __name__ == "__main__":
    main()