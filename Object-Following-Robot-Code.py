Python 3.7.7 (tags/v3.7.7:d7c567b08f, Mar 10 2020, 10:41:24) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
import cv2
import Jetson.GPIO as GPIO
print(cv2._version_)
import numpy as np
import time

# for 1st motor
ENA = 33
IN1 = 35
IN2 = 37

# for 2nd motor
ENB = 32
IN3 = 36
IN4 = 38

GPIO.setmode (GPIO.BOARD)

# initializing motor 1
GPIO.setup (ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup (IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup (IN2, GPIO.OUT, initial=GPIO.LOW)

# initializing motor 2
GPIO.setup (ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup (IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup (IN4, GPIO.OUT, initial=GPIO.LOW)

def nothing(x):
	pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1320,0)

cv2.createTrackbar('hueLower', 'Trackbars',179,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars',100,179,nothing)

cv2.createTrackbar('hue2Lower', 'Trackbars',0,179,nothing)
cv2.createTrackbar('hue2Upper', 'Trackbars',8,179,nothing)

cv2.createTrackbar('satLow', 'Trackbars',125,255,nothing)
cv2.createTrackbar('satHigh', 'Trackbars',205,255,nothing)
cv2.createTrackbar('valLow','Trackbars',130,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)


image_width=640
image_height=480
center_image_x=image_width/2
center_image_y=image_height/2
minimum_area=250
maximum_area=100000
forward_speed=1.0
turn_speed=1.0
flip=2

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)
#width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
#height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
width=720
height=1080
print('width:',width,'height:',height)

while True:
	ret, frame = cam.read()
	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
	hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')

	hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
	hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')

	Ls=cv2.getTrackbarPos('satLow', 'Trackbars')
	Us=cv2.getTrackbarPos('satHigh', 'Trackbars')

	Lv=cv2.getTrackbarPos('valLow', 'Trackbars')
	Uv=cv2.getTrackbarPos('valHigh', 'Trackbars')

	l_b=np.array([hueLow,Ls,Lv])
	u_b=np.array([hueUp,Us,Uv])

	l_b2=np.array([hue2Low,Ls,Lv])
	u_b2=np.array([hue2Up,Us,Uv])

	FGmask=cv2.inRange(hsv,l_b,u_b)
	FGmask2=cv2.inRange(hsv,l_b2,u_b2)
	FGmaskComp=cv2.add(FGmask,FGmask2)
	cv2.imshow('FGmaskComp',FGmaskComp)
	cv2.moveWindow('FGmaskComp',0,530)

	contours,hierarchy=cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
	object_area = 0
	object_x=0
	object_y=0

	for cnt in contours:
		found_area=cv2.contourArea(cnt)
		(x,y,width,height)=cv2.boundingRect(cnt)
		if found_area>=50:
			#cv2.drawContours(frame,[cnt],0,(255,0,0),3)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
			center_x=x+(width/2)
			center_y=y+(height/2)
		if object_area < found_area:
			object_area = found_area
			object_x = center_x
			object_y = center_y
	if object_area > 0:
		ball_location = [object_area, object_x, object_y]
	else:
		ball_location = None
 
	if ball_location:
		if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
			if ball_location[1] > (center_image_x + (image_width/3)):
				GPIO.output (ENA, 33)
				GPIO.output (IN1, GPIO.LOW)
				GPIO.output (IN2, GPIO.LOW)
				GPIO.output (ENB, 32)
				GPIO.output (IN3, GPIO.HIGH)
				GPIO.output (IN4, GPIO.LOW)
				print("Turning right")
			elif ball_location[1] < (center_image_x - (image_width/3)):
				GPIO.output (ENA, 33)
				GPIO.output (IN1, GPIO.HIGH)
				GPIO.output (IN2, GPIO.LOW)
				GPIO.output (ENB, 32)
				GPIO.output (IN3, GPIO.LOW)
				GPIO.output (IN4, GPIO.HIGH)
				print("Turning left")
			else:
				GPIO.output (ENA, 33)
				GPIO.output (IN1, GPIO.HIGH)
				GPIO.output (IN2, GPIO.LOW)
				GPIO.output (ENB, 32)
				GPIO.output (IN3, GPIO.HIGH)
				GPIO.output (IN4, GPIO.LOW)
				print("Forward")
		elif (ball_location[0] < minimum_area):
			GPIO.output (ENA, 33)
			GPIO.output (IN1, GPIO.LOW)
			GPIO.output (IN2, GPIO.LOW)
			GPIO.output (ENB, 32)
			GPIO.output (IN3, GPIO.LOW)
			GPIO.output (IN4, GPIO.LOW)
			print("Target isn't large enough, searching")
		else:
			GPIO.output (ENA, 33)
			GPIO.output (IN1, GPIO.LOW)
			GPIO.output (IN2, GPIO.LOW)
			GPIO.output (ENB, 32)
			GPIO.output (IN3, GPIO.LOW)
			GPIO.output (IN4, GPIO.LOW)
			print("Target large enough, stopping")
	else:
		GPIO.output (ENA, 33)
		GPIO.output (IN1, GPIO.LOW)
		GPIO.output (IN2, GPIO.LOW)
		GPIO.output (ENB, 32)
		GPIO.output (IN3, GPIO.LOW)
		GPIO.output (IN4, GPIO.LOW)
		print("Target not found, searching")
 

	cv2.imshow('nanoCam',frame)
	cv2.moveWindow('nanoCam',0,0)
	if cv2.waitKey(1)==ord('q'):
		break
cam.release()
cv2.destroyAllWindows()