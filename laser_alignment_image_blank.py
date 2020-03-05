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

# Enter distance from wall, entered by the user
d = raw_input("Please enter distance from wall, in inches: ")
print("Confirming the distance you entered is: ", d)

# grab an image from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):

	image = frame.array
	image = cv2.flip(image,-1)

	# plot semi-crosshairs for alignment
	cv2.line(image, (640,0), (640,720), (0,150,150), 1)
	cv2.line(image, (600,360), (1280,360), (0,150,150), 1)

	# display distance from the wall, for reference
	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	red = (0, 0, 255)
	cv2.putText(image, d, (800, 200), font, 10, red, 10)

	# display the image on screen and wait for a keypress
	cv2.imshow("Image", image)
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	# proceed as specified by the user

	# press q to break out of video stream
	if key == ord("q"):
		break

	# press m to save .jpg image with distance as filename
	if key == ord("m"):
		d = int(d)
		filename = "%d.jpg" %d
		cv2.imwrite(filename, image)
		break
