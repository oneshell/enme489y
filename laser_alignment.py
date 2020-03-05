# ENME 489Y: Remote Sensing
# Assignment 5: Alignment of field deployable lidar using line laser

# Import packages
import numpy as np
import argparse
import cv2
import imutils
import glob
import re
import time
import datetime
import matplotlib
import matplotlib.pyplot as plt

print("All packages imported properly!")

files = glob.glob('alignment_images/*.jpg')      # finds all the pathnames matching a specified pattern
print(files)

# define the lower and upper boundaries of the
# red line in the HSV color space
# Note: use colorpicker.py to create a new HSV mask
colorLower = (164, 114, 26)
colorUpper = (255, 255, 255)

# initialize plot arrays
x_plot = []
y_plot = []

for x in files:  # x is the filename
    print(x)

    distance = re.findall('\\d+', x)
    distance = map(int, distance)
    print(distance)

    image = cv2.imread(x)

    # blur the frame and convert to the HSV color space
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "red"
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    # cv2.imshow("Caption", mask)

    # Define image row of interest & color to plot line
    y = 360

    #  Convert image to grayscale and define matrix row of interest
    x = mask[y]

    # Initialize arrays for averaging
    spot = []

    # identify laser returns
    for i in range(0,len(x)):
        if x[i] > 200:
            print(i)
            spot.append(i)
    if len(spot) > 0:
        print spot
        spot = np.average(spot)
        spot = int(spot)
    else: 
        spot = 1
        
    #  Draw line of interest on original image & plot
    cv2.line(mask, (620, y), (1280, y), (255,255,255), 2)
    cv2.circle(mask, (spot, 360), 20, (255,255,255))

    # write (distance,x,y) coordinates of laser spot to file
    # for post-processing
    f = open('laserlog.txt', 'a')
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y/%m/%d %H:%M")
    outstring = str(distance).strip('[]') + " " + str(spot) + "\n"
    print(outstring)
    f.write(outstring)
    f.close()

    x_plot.append(spot)
    y_plot.append(distance)

# Define ro and rpc, specific to your lidar
# Radian offset, which compensates for alignment errors
ro = -0.0019

# Radians per pixel pitch, or Gain [rad / pixel]
rpc = 0.00008

# Define the full span of pixels from center
# Since our Python code sets the camera frame (x,y) coordinates
# as (1280, 640), the imaged laser spot is free to translate through
# (1280/2) = 640 pixels from the center of the image
pfc = np.arange(0,640,2)

# Separation distance between axes of laser pointer and webcam [cm]
# 12 inches = 0.3048 meters
H = 0.3048

# Determine the distance to the target, given calibrated system parameters
# and pfc array evaluated from data
D = np.empty((0))
for i in range(pfc.shape[0]):
    D = np.append(D, H/( np.tan(pfc[i]*rpc + ro) ))

D = np.flip(D,0)

# Convert H into inches and D into feet for analysis
H = 39.37*H
D = 3.28*D

# Graph row of interest values
plt.figure(1)
plt.plot(x_plot,y_plot,'ro')
plt.plot(pfc, D, 'b-', linewidth=3)
plt.title('Lidar Calibration Curve')
plt.xlabel('Pixel')
plt.ylabel('Distance to Target (Inches)')
plt.axis([0, 640, 0, 120])
plt.show()





