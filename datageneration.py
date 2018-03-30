# ENME 489Y: Remote Sensing

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
from mpl_toolkits.mplot3d import Axes3D

print "All packages imported properly!"

# define the lower and upper boundaries of the
# red laser line in the HSV color space
# Note: may need to use colorpicker.py to create a new HSV mask
colorLower = (164, 114, 26)
colorUpper = (255, 255, 255)

# initialize plot arrays
x_plot = []
y_plot = []
a_plot = []
D_plot = []
IMU_plot = []
pcX = []
pcY = []
pcZ = []

# lidar parameters
# these should be copied/tuned based on your lidar setup
ro = -0.0019
rpc = 0.00008

# 12 inch separation distance, laser to camera, in meters
H = 0.3048

# Raspberry Pi camera field of view
# 12 inch ruler fills width of camera at 17 inch range
# ang = np.atan(6/17)
rpi = 0.339292614   # [rad]

ang = np.zeros((720), dtype=float)

for i in range(0, 720):
    ang[i] = 0.000942479485*(i-360)
# print ang

files = glob.glob('testdataraymond/*.jpg')      # finds all the pathnames matching a specified pattern
print files

# Write (angle,x,y) coordinates of laser spot to file
# for post-processing
f = open('testdataraymond/testresults.txt', 'a')
# now = datetime.datetime.now()
# timestamp = now.strftime("%Y/%m/%d %H:%M")

# uncomment to examine time required to process all data files
millis = int(round(time.time() * 1000))

for x in files:  # x is the filename
    print x

    # Pull pointing angle from each filename
    # Ensure all filenames have POSITIVE angle values (0-359 deg)
    angle = re.findall('\\d+', x)
    angle = map(int, angle)
    print angle

    # Read in image
    image = cv2.imread(x)

    # blackout the right side of the image, since this is all noise
    # but...leave the original .jpg file untouched
    image[0:720, 600:1280] = (0, 0, 0)

    # blur the frame and convert to the HSV color space
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Apply mask for the color "red"
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    for a in range(0,720,1):
        # Define image row of interest & color to plot line
        y = a
        # print y

        #  Convert image to grayscale and define matrix row of interest
        x = mask[y]

        # Initialize arrays for averaging
        spot = []

        # identify laser returns
        for i in range(0,len(x)):
            if x[i] > 200:
                spot.append(i)
                # Future work: include false detection filter?

        # Average all row pixels identified as the red laser line
        if len(spot) > 1:
            spot = np.average(spot)
            spot = int(spot)
        else:
            spot = int(0)

        if spot >= 1:

            # Ensure proper setup of pixels-from-center
            spot = 640 - spot

            # calculate range based on geometry
            D = 3.28084*H/np.tan(spot * rpc + ro)   # outputs range in feet

            IMU_plot.append(angle)
            a_plot.append(a)
            D_plot.append(D)
            x_plot.append(D*np.sin(ang[a]))
            pcX.append(D*np.sin(ang[a])*np.cos(np.deg2rad(angle)))
            pcY.append(D*np.cos(np.deg2rad(angle)))
            pcZ.append(D*np.sin(np.deg2rad(angle)))

            # Writes (x, y, z) coordinates of each 3D point to file
            outstring = str(D*np.sin(ang[a])*np.cos(np.deg2rad(angle))).strip("[]") + " " + str(D*np.cos(np.deg2rad(angle))).strip("[]") + " " + str(D*np.sin(np.deg2rad(angle))).strip("[]") + "\n"
            f.write(outstring)

        else:

            IMU_plot.append(angle)
            a_plot.append(a)
            D_plot.append(0)
            x_plot.append(0)
            pcX.append(int(0))
            pcY.append(int(0))
            pcZ.append(int(0))

            # Writes (x, y, z) coordinates of each 3D point to file
            outstring = str(0) + " " + str(0) + " " + str(0) + "\n"
            f.write(outstring)

# close the text file
f.close()

# uncomment to examine time required to process each frame
millis_1 = int(round(time.time() * 1000))
print " "
print "Time required to process all data:"
print millis_1 - millis

# Plot data in 3D point cloud scatter plot
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pcX, pcY, pcZ, s=1)
ax.view_init(elev=110, azim=110)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.xlim(-40, 40)
plt.ylim(20, 100)
plt.show()

print " "
print "finished...bye bye!"













