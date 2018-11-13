import numpy as np
import imutils
import cv2
import time

# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('galaxy/2Nov2018/trackball7.avi',fourcc,10,(1280, 1440))

# initialize the webcam
camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(3)

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

    image1 = imutils.resize(image1, height = 200)
    image2 = imutils.resize(image2, height = 200)

    # write the frame to video file
	  # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    # out.write(image1)

    # show the frames to the screen
    cv2.line(image1, (image1.shape[1]/2, 0), (image1.shape[1]/2, image1.shape[0]), (0, 255, 0))
    cv2.imshow("Camera 1", image1)
    cv2.imshow("Camera 2", image2)

    # package = np.vstack([image1, image2])
    # cv2.imshow("Packaged Camera Views", package)
    # print package.shape[1]
    # print package.shape[0]

    # write the frame to video file
    # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    #out.write(package)

    key = cv2.waitKey(1) & 0xFF

  	# press the 'q' key to stop the video stream
    if key == ord("q"):
        break
