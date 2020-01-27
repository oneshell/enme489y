# ENME 489Y: Remote Sensing
# Week 2: Introduction to Python & PyCharm

import numpy as np
import matplotlib
import cv2
import imutils

print("All packages imported properly!")

image = cv2.imread("testudo.jpg")

cv2.imshow("Old School Testudo Logo: Original Dimensions", image)
cv2.waitKey(0)

image = imutils.resize(image, width=400)

cv2.imshow("Old School Testudo Logo: Resized", image)
cv2.waitKey(0)

cv2.imwrite("testimage.jpg", image)

stream = cv2.VideoCapture("test_video.mp4")
while True:
	# grab the frame from the threaded video file stream
	(grabbed, frame) = stream.read()
 
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break
 
	# show the frame and update the FPS counter
	cv2.imshow("Frame", frame)
	cv2.waitKey(33)
