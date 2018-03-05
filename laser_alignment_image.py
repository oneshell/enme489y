# ENME489Y: Remote Sensing

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import imutils

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280,720)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(1280,720))

# allow the camera to setup
time.sleep(1)

# grab an image from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):

	image = frame.array
	# may need to flip image, depending on mechanical setup of instrument
	image = cv2.flip(image,-1)

	# plot crosshairs, for alignment
	cv2.line(image, (640,0), (640,720), (0,150,150), 1)
	cv2.line(image, (0,360), (1280,360), (0,150,150), 1)
	# plot green vertical lines, for alignment
	for i in range(50, 1300, 50):
		cv2.line(image, (i,0), (i, 720), (0,150,0), 3)

	# display the image on screen and wait for a keypress
	cv2.imshow("Image", image)
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	# break out of video loop when specified by the user
	if key == ord("q"):
		break




