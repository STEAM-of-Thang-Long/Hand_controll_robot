import pygame
import socket
import urllib.request
import cv2
import numpy as np
import time
import math
from calendar import c
from handDetector import HandDetector

handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)

pygame.init()
pygame.font.init()
pygame.display.set_caption('VIABot controller')
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

CONTROL_IP = "192.168.4.100"
CONTROL_PORT = 9999
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sk.settimeout(3000)

CAM_URL = "http://192.168.4.1:80"
stream = urllib.request.urlopen(CAM_URL)
bytes = bytes()

def set_speed(left_wheel, right_wheel): 
    """Set speed for robot wheel

    Args:
        left_wheel (int): [-100, 100]. -100 -> 0: Reverse, 0 -> 100: Forward
        right_wheel (int): [-100, 100]. -100 -> 0: Reverse, 0 -> 100: Forward
    """
    control_msg = "CONTROL_WHEEL {} {}".format(
        left_wheel, right_wheel).encode('ascii')
    sk.sendto(control_msg, (CONTROL_IP, CONTROL_PORT))

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
origin_x = rect.x
origin_y = rect.y
run = True

#RUNININGG
while run:
# xử lý dữ liệu tay
    cv2.imshow("Image", image)
    cv2.waitKey(1)
    show = ''
    count = 0
    check = 0
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    if(len(handLandmarks) != 0):
        RT = handLandmarks[4][1] - handLandmarks[3][1]#Right Thumb
 
        ID = handLandmarks[8][2] - handLandmarks[6][2]#Index finger

        MF = handLandmarks[12][2] - handLandmarks[10][2]#Middle finger

        RF = handLandmarks[16][2] - handLandmarks[14][2]#Ring finger

        LT = handLandmarks[20][2] - handLandmarks[18][2]#Little finger
 
# code from VSC 2021       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))

    keys = pygame.key.get_pressed()

    color = (255, 0, 0)
    if ID > 0 and RT*MF*RF*LT <= 0 :
        rect.x = origin_x
        rect.y = origin_y - 50
        set_speed(30, 30)
        color = (0, 0, 255)
    elif LT*ID > 0 and ID*MF*RF*RT <= 0:
        rect.x = origin_x
        rect.y = origin_y + 50
        set_speed(-30, -30)
        color = (0, 0, 255)
    elif RT > 0 and LT*MF*RF*ID <= 0:
        rect.x = origin_x - 50
        rect.y = origin_y
        set_speed(-30, 30)
        color = (0, 0, 255)
    elif LT > 0 and ID*MF*RF*RT <= 0:
        rect.x = origin_x + 50
        rect.y = origin_y
        set_speed(30, -30)
        color = (0, 0, 255)
    else:
        rect.x = origin_x
        rect.y = origin_y
        set_speed(0, 0)
        color = (255, 0, 0)

    rect.centerx = rect.centerx % window.get_width()
    rect.centery = rect.centery % window.get_height()

    window.fill((60, 60, 60))

    pygame.draw.circle(window, (255, 255, 255), (window.get_width() // 2, window.get_height() // 2), 30)
    pygame.draw.rect(window, color, rect)
    
    font = pygame.font.SysFont('Comic Sans MS', 16)
    text = font.render('Use arrow keys or w,a,s,d to move', False, (0, 255, 0))
    window.blit(text, (10, 10))

    pygame.display.flip()

    # Get and display image
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        hinh_anh = bytes[a:b+2]
        bytes = bytes[b+2:]
        try:
            hinh_anh = cv2.imdecode(np.frombuffer(
                hinh_anh, dtype=np.uint8), cv2.IMREAD_COLOR)
        except:
            continue

# hiện ra màn hình
    cv2.putText(image, show , (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (237,142,83), 10)
    cv2.imshow("STEM of Thang Long", image)
    cv2.imshow("Image", hinh_anh)
    if cv2.waitKey(5) & 0xFF == 27:
        break        
    
pygame.quit()
exit()
