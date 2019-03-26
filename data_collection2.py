# ENME489Y: Remote Sensing

# import the necessary packages
import numpy as np
import time
import cv2
import imutils
import os

# allow the camera to setup
time.sleep(1)

# Enter the initial IMU angle from user
d = raw_input("Please enter IMU angle: ")
print "Confirming the IMU angle you entered is: "
print d

# The following line should be used if interestsed in
# the -ss ("shutter speed") command for long exposure
#command = 'raspistill -w 1280 -h 720 -ss 1000000 -o blank.jpg'
command = 'raspistill -w 1280 -h 720 -o blank.jpg'
os.system(command)

image = cv2.imread('blank.jpg')
image = cv2.flip(image,-1)

# plot crosshairs for alignment
cv2.line(image, (640,0), (640,720), (0,150,150), 1)
cv2.line(image, (600,360), (1280,360), (0,150,150), 1)

# display IMU angle, for reference
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
red = (0, 0, 255)
cv2.putText(image, d, (800, 200), font, 10, red, 10)

# write image to file
d = int(d)
filename = "%d.jpg" %d
cv2.imwrite(filename, image)

command = 'mv ' + filename + ' /home/pi/alignment_images/'
os.system(command)

print "All done!"



