# ENME 489Y: Remote Sensing

# Python script tracks green 'stoplight'
# and saves .avi video of trackinng to stoplight.avi

# import the necessary packages
from collections import deque
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
# ADJUST THE VALUE OF default=1 (try 10, 20, etc)
# TO SEE THE TAIL AS YOU MOVE ACROSS THE SCREEN
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=1,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the
# green light (circle) in the HSV color space, then initialize the
# list of tracked points
colorLower = (29, 70, 6)
colorUpper = (75, 255, 255)

pts = deque(maxlen=args["buffer"])

# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = 640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('stoplight.avi',fourcc,5,(1280,720))


# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # grab the current frame
    image = frame.array

    # pause
    time.sleep(0.1)

    # resize the frame, blur it, and convert to the HSV
    # color space
    # image = imutils.resize(image, width=1280)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find counters in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 0.1:
            # draw the circle and centroid on the frame
            # then update the list of tracked points
            cv2.circle(image, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)

            # update the points queue
            pts.appendleft(center)

        # loop over the set of tracked points
        for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)

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









