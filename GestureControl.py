import cv2
import numpy as np
import mediapipe as mp
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm

wcam = 640
hcam = 480

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

curTime = 0
prevTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

vol=0
volPercent=0
volBar=400


while True:
    success, img = cap.read()
    img = detector.findHands(img,False)
    lmlist = detector.findPos(img)

    if len(lmlist) !=0:
        # print(lmlist[4]) 
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]

        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(340,80,100),3)
        cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        print(length)
        if length<25:
            cv2.circle(img,(cx,cy),10,(254,255,187),cv2.FILLED)

        
        vol = np.interp(length,[30,240],[minVol,maxVol])
        volBar = np.interp(length,[30,240],[400,150])
        volPercent = np.interp(length,[30,240],[0,100])
        volume.SetMasterVolumeLevel(vol, None)


    curTime = time.time()
    fps = 1/(curTime-prevTime)
    prevTime = curTime

    cv2.putText(img,f'{int(volPercent)}%',(45,450),cv2.FONT_ITALIC,1,(0,0,255),3)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)

    cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_ITALIC,1,(0,0,255),3)
    cv2.imshow('Camera',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break