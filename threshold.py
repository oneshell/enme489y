# ENME 489Y: Remote Sensing
# Threshold algorithm & comparison with OpenCV

# Import packages
import numpy as np
import cv2
import imutils

print "All packages imported properly!"

# Load & show original image
image = cv2.imread("testudo.jpg")
cv2.imshow("Original Image", image)

# Grayscale image using cv2.COLOR_BGR2GRAY
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image", image)

true = image.copy()

# Define threshold, in the range 0-255
thresh = 150

for x in range (0,image.shape[0]-1):
    for y in range (0,image.shape[1]-1):
        if image[x, y] > thresh:
            image[x, y] = 255
        else:
            image[x, y] = 0

cv2.imshow("Thresholded Image: Algorithm", image)

# Threshold image using cv2.THRESH_BINARY
frame = cv2.threshold(true, thresh, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("Thresholded Image: OpenCV", frame)

cv2.waitKey(0)
