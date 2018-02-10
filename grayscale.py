# ENME 489Y: Remote Sensing
# Grayscale algorithm & comparison with OpenCV

# Import packages
import numpy as np
import cv2
import imutils

print "All packages imported properly!"

# Load & show original image
image = cv2.imread("testudo.jpg")
true = image.copy()

cv2.imshow("Original Image", image)

print "height: %d" % (image.shape[0])
print "width: %d" % (image.shape[1])

x_lim = image.shape[0]
y_lim = image.shape[1]

for x in range (0,x_lim - 1):
    for y in range (0,y_lim - 1):
        (b, g, r) = image[x, y]
        # image[x, y] = (0.33 * b + 0.33 * g + 0.33 * r)
        image[x, y] = (0.11 * b + 0.59 * g + 0.3 * r)

cv2.imshow("Grayscale Image: Algorithm", image)

# Grayscale image using cv2.COLOR_BGR2GRAY
image = cv2.cvtColor(true, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale: OpenCV", image)

cv2.waitKey(0)
