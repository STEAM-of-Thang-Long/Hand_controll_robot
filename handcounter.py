from calendar import c
from handDetector import HandDetector
import cv2
import math
import numpy as np
import time

handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)
print('oke')

def check_fin ():
    while True:
        show = ''
        count = 0
        check = 0
        status, image = webcamFeed.read()
        handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
        if(len(handLandmarks) != 0):
            #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
            #details: https://google.github.io/mediapipe/solutions/hands
            
            '''if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
                count = count+1
            elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
                count = count+1
            if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
                count = count+1
            if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
                count = count+1
            if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
                count = count+1 
            if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
                count += 1
                '''
            check = handLandmarks[14][2] - handLandmarks[16][2]
            count = handLandmarks[18][2] - handLandmarks[20][2]
        if -15  <= count <= 15 and count != 0 and -5 <= check <= 20 :
            show = "I love STEM ^_^"
        else:
            show = ''  
           

        cv2.putText(image, show , (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (237,142,83), 10)
        cv2.imshow("STEM of Thang Long", image)
        if cv2.waitKey(5) & 0xFF == 27:
          break        
check_fin()

