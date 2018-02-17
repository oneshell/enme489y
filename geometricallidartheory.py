# ENME 489Y: Remote Sensing
# Triangulation lidar code

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Refer to Todd Danko's site for details, including physical layout
# https://sites.google.com/site/todddanko/home/webcam_laser_ranger

# Define ro and rpc, which can be tweaked down the road
# Radian offset, which compensates for alignment errors
ro = -0.01

# Radians per pixel pitch, or Gain [rad / pixel]
rpc = 0.001

# Define the full span of pixels from center
# Since our Python code sets the camera frame (x,y) coordinates
# as (1280, 640), the imaged laser spot is free to translate through
# (1280/2) = 640 pixels from the center of the image
pfc = np.arange(0,640,2)
pfc = np.flip(pfc,0)

# Separation distance between axes of laser pointer and webcam [cm]
# 12 inches = 0.3048 meters
H = 0.3048

# Determine the distance to the target, given calibrated system parameters
# and pfc array evaluated from data
D = np.empty((0))
for i in range(pfc.shape[0]):
    D = np.append(D, H/( np.tan(pfc[i]*rpc + ro) ))

# Convert H into inches and D into feet for analysis
H = 39.37*H
D = 3.28*D

# Plot distance to target as function of pfc value
plt.figure(1)
plt.plot(pfc, D, 'b-', linewidth=3)
plt.title('Range to Target for Separation Distance H = 12 inches')
plt.xlabel('Pixels from Center [pfc]')
plt.ylabel('Distance to target [ft]')
plt.axis([0, 650, 0, 10])
plt.grid()
plt.show()

