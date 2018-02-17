# ENME489Y: Remote Sensing

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280,720)
rawCapture = PiRGBArray(camera, size=(1280,720))

# allow the camera to setup
time.sleep(0.1)

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# plot crosshairs for alignment
cv2.line(image, (640,0), (640,720), (0,0,150), 1)
cv2.line(image, (0,360), (1280,360), (0,0,150), 1)

# plot additional lines to define bounds of laser region
#cv2.line(image, (0,380), (1280,380), (0,0,150), 1)
#cv2.line(image, (0,340), (1280,340), (0,0,150), 1)


# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)

# save image to file
cv2.imwrite('laser_spot.jpg', image)





