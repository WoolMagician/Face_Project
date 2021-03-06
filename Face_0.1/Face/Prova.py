#!/usr/bin/env python3.2

print '''
 ______                  
 |  ___|                 
 | |_ __ _   ___   ___   
 |  _/ _` | / __| / _ \  
 | || (_| || (__ |  __/_ 
 \_(_)__,_(_)___(_)___(_)
                         
 '''
print 'Starting Environment!'

from Adafruit_PWM_Servo_Driver import PWM
import Tkinter as tk
import cv2
import random
import time
import signal
import curses
import os

pwm = PWM(0x40, debug=False)

eye_ch_x = 10
eye_ch_y = 9
hat_address = 0
servo_x_move = 0
servo_y_move = 0
DOWNSCALE = 8
crepa = 0
faces = 0
state = False
pippo = 0
scrnshot = 122 #F11
photow = 1280 
photoh = 720
photoframe = 0
res = (photow,photoh)

webcam = cv2.VideoCapture(0)
webcam.set(4,photow)
webcam.set(5,photoh)

classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
pwm.setPWMFreq(60) #setting pwm freq to 60Hz

damn = curses.initscr()
damn.nodelay(1) # doesn't keep waiting for a key press

def setEyeX( var1, var2 ):
    xcord = (var1+var2/2)
    if (340 < xcord < 350):
        xcord = (var1+var2/2)
    xmove = (172 * xcord)/1000 + 420
    return xmove

def setEyeY( var1, var2):
    ycord = (var1+var2/3)
    if (200 < ycord < 210):
        ycord = (var1+var2/3)
    ymove = (420 * ycord)/1000 + 330
    return ymove  

def searchForHumans():
    
    xcord = random.randrange(400, 480, 15)
    ycord = random.randrange(400, 510, 15)
    time.sleep(.5)
    pwm.setPWM(eye_ch_x, hat_address, xcord)
    pwm.setPWM(eye_ch_y, hat_address, ycord)
    return 

def faceTracking():
        
        for f in faces:
            x, y, w, h = [ v*DOWNSCALE for v in f ]

            servo_x_move = setEyeX(x,w)
            servo_y_move = setEyeY(y,h)
	    print servo_x_move , ('X')
	    print servo_y_move , ('Y')
            pwm.setPWM(eye_ch_x, hat_address, servo_x_move)
            pwm.setPWM(eye_ch_y, hat_address, servo_y_move)
	return 
        
if webcam.isOpened(): # try to get the first frame
    print 'Initializing...'
    get, frame = webcam.read()
    print 'Done!'    

else:
    get = False
    print 'Error getting image from cam'

while get:
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
    miniframe = cv2.resize(gray, minisize)
    faces = classifier.detectMultiScale(miniframe)
    print "Found {0} faces!" .format(len(faces))    
    faceTracking()
   # searchForHumans()
    c = damn.getch()
    if c > 122:
        newpath = r'Screenshots' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
	photoframe = cv2.resize(frame, res)
        cv2.imwrite('Screenshots/Screenshot{0}.jpg' .format(pippo),photoframe)
        pippo = pippo + 1
   
    get, frame = webcam.read()
    
