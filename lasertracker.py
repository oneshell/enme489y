# ENME 489Y: Remote Sensing

# import the necessary packages
from collections import deque
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import imutils
import cv2
import time
import datetime

# construct the argument parse and parse the arguments
# ADJUST THE VALUE OF default=1 (try 10, 20, etc)
# TO SEE THE TAIL AS YOU MOVE ACROSS THE SCREEN
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=1,
               help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the
# green laser light (circle) in the HSV color space, then initialize the
# list of tracked points
# Note: use colorpicker.py to create a new HSV mask
colorLower = (39, 69, 75)
colorUpper = (129, 225, 255)

pts = deque(maxlen=args["buffer"])

# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (1280,720)
# set the camera.framerate = 32 if using a monitor, or = 20 if using VNC with ethernet cable
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(1280,720))

# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('stoplight.avi',fourcc,1,(1280,720))

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):

	# grab the current frame
	image = frame.array

	# pause
	time.sleep(0.1)

	# resize the frame, blur it, and convert to the HSV
	# color space
	image = imutils.resize(image, width=1280)
 	blurred = cv2.GaussianBlur(image, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
#	mask = cv2.erode(mask, None, iterations=2)
#	mask = cv2.dilate(mask, None, iterations=2)

	# find counters in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# proceed regardless to keep video streaming
	if len(cnts) >= 0:

	        # find the largest contour in the mask, then use
        	# it to compute the minimum enclosing circle and
        	# centroid
		if len(cnts) > 0:
       			c = max(cnts, key=cv2.contourArea)
       			((x, y), radius) = cv2.minEnclosingCircle(c)
       			M = cv2.moments(c)
       			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		else:
			x = 11
			y = 11
			radius = 1

    # only proceed if given criteria are met
		# OPTION 1: (x,y) coordinates are within certain range

		# print the (x,y) coordinates of the laser spot to the screen
		font = cv2.FONT_HERSHEY_COMPLEX_SMALL
		cv2.putText(image, str(x)+","+str(y), (645,25), font, 1, (0,0,255),2)

		# plot crosshairs on each frame for laser alignment
		cv2.line(image, (640,0), (640,720), (0,0,150),1)
		cv2.line(image, (620,360), (660,360), (0,0,150),1)
		# plot bounding lines for the y-dimension
		# feel free to adjust as desired
		# goal is to illustrate the y-coordinate bounds of the system
		cv2.line(image, (0,340), (1280,340), (0,0,150),1)
		cv2.line(image, (0,380), (1280,380), (0,0,150),1)

		# feel free to alter the x, y bounds defined in the next 'if' statement
		# these set the range over which the RPi tracks the imaged laser spot
		if x > 640 and y < 600 and y > 200:
		# OPTION 2: radius of beam is above threshold radius
#        	if radius > 0:
		        # draw the circle and centroid on the frame
           	        # then update the list of tracked points
#			cv2.circle(image, (int(x), int(y)), int(radius),
#                       		(0, 255, 255), 2)
                	cv2.circle(image, center, 2, (0, 0, 255), -1)
			
			# write (x,y) coordinates of laser spot to file
			# for post-processing
			f = open('laserlog.txt','a')
			now = datetime.datetime.now()
			timestamp = now.strftime("%Y/%m/%d %H:%M")
			outstring = str(timestamp)+" "+ str(x)+" "+str(y)+"\n"
			print(outstring)
			f.write(outstring)
			f.close()

		# write the frame to video file
		# UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
#		out.write(image)

		# show the frame to our screen
		cv2.imshow("Frame", image)
		key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# press the 'q' key to stop the video stream
		if key == ord("q"):
        		break









