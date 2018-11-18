import numpy as np
import imutils
import cv2
import time

# allow the camera to warmup
time.sleep(0.1)

# initialize the webcam
camera1 = cv2.VideoCapture(1)
camera2 = cv2.VideoCapture(2)

# Set the camera resolution to 1280 x 720
camera1.set(3, 1280)
camera1.set(4, 720)
camera2.set(3, 1280)
camera2.set(4, 720)

# keep looping
while True:

    # grab the current frame
    ret1, image1 = camera1.read()
    ret2, image2 = camera2.read()

    # resize the images
    image1 = imutils.resize(image1, width = 300)
    image2 = imutils.resize(image2, width = 300)

    # package and show the images to the screen
    package = np.hstack([image1, image2])
    cv2.imshow("Camera Views", package)

    key = cv2.waitKey(1) & 0xFF

	# press the 'q' key to stop the video stream
    if key == ord("q"):
        break
