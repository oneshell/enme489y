# ENME 489Y: Remote Sensing
# Week 3: OpenCV Fundamentals

# Import packages
import numpy as np
import cv2
import imutils

print "All packages imported properly!"

# Displaying & resizing images
image = cv2.imread("testudo.jpg")

cv2.imshow("Old School Testudo Logo", image)
cv2.waitKey(0)

image = imutils.resize(image, width=400)

cv2.imshow("Old School Testudo Logo: Resized", image)
cv2.waitKey(0)

# Write image to disk (save image)
cv2.imwrite("testimage.jpg", image)

# Image shape (dimensions)
print image.shape
print "height: %d" % (image.shape[0])
print "width: %d" % (image.shape[1])
print "channels: %d" % (image.shape[2])

# Pixel operations & image slicing
(b, g, r) = image[0, 0]
print "Pixel at (0, 0) - Red: %d, Green: %d, Blue: %d" % (r, g, b)
#
image[0, 0] = (0, 0, 255)
(b, g, r) = image[0, 0]
print "Pixel at (0, 0) - Red: %d, Green: %d, Blue: %d" % (r, g, b)

corner = image[0:100, 0:100]
cv2.imshow("Corner", corner)

image[0:100, 0:100] = (0, 255, 0)

cv2.imshow("Updated", image)
cv2.waitKey(0)

# Image blurring
blurred = np.hstack([
    cv2.blur(image, (3,3), 0),
    cv2.blur(image, (5,5), 0),
    cv2.blur(image, (7,7), 0)])
cv2.imshow("Average Blurring", blurred)

cv2.waitKey(0)

blurred = np.hstack([
    cv2.GaussianBlur(image, (3,3), 0),
    cv2.GaussianBlur(image, (5,5), 0),
    cv2.GaussianBlur(image, (7,7), 0)])
cv2.imshow("Gaussian Blurring", blurred)

cv2.waitKey(0)

blurred = np.hstack([
    cv2.medianBlur(image, 3),
    cv2.medianBlur(image, 5),
    cv2.medianBlur(image, 7)])
cv2.imshow("Median Blurring", blurred)

cv2.waitKey(0)

blurred = np.hstack([
    cv2.bilateralFilter(image, 5, 21, 21),
    cv2.bilateralFilter(image, 7, 31, 31),
    cv2.bilateralFilter(image, 9, 41, 41)])
cv2.imshow("Bilater Filtering", blurred)

cv2.waitKey(0)

# Drawing lines & rectangles
canvas = np.zeros((500, 500, 3), dtype="uint8")

green = (0, 255, 0)
cv2.line(canvas, (0,0), (400, 500), green)

red = (0, 0, 255)
cv2.line(canvas, (500, 0), (0, 500), red, 3)

cv2.rectangle(canvas, (40, 50), (100, 100), green)
cv2.rectangle(canvas, (50, 400), (400, 225), red, 5)
cv2.rectangle(canvas, (350, 150), (400, 425), (255, 0, 0), -1)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

# Drawing circles
canvas = np.zeros((500, 500, 3), dtype="uint8")

(centerX, centerY) = (canvas.shape[1]/2, canvas.shape[0]/2)

white = (255, 255, 255)

for r in xrange(0, 275, 25):
    cv2.circle(canvas, (centerX, centerY), r, white)
    cv2.imshow("Concentric Circles", canvas)
    cv2.waitKey(0)

# Overlay text on top of an image
canvas = np.zeros((500, 500, 3), dtype="uint8")

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

red = (0, 0, 255)
cv2.putText(canvas, 'Hello World', (100, 200), font, 1, red, 1)

cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

# Transforming images / flipping
image = cv2.imread("testudo.jpg")
image = imutils.resize(image, width=400)

cv2.imshow("Original", image)

flipped = cv2.flip(image, 1)
cv2.imshow("Flipped Horizontally", flipped)

flipped = cv2.flip(image, 0)
cv2.imshow("Flipped Vertically", flipped)

flipped = cv2.flip(image, -1)
cv2.imshow("Flipped Horizontally & Vertically", flipped)

cv2.waitKey(0)

# Rectangular mask
image = cv2.imread("testudo.jpg")
image = imutils.resize(image, width=400)

cv2.imshow("Original", image)

mask = np.zeros(image.shape[:2], dtype = "uint8")
(cX, cY) = (image.shape[1]/2, image.shape[0]/2)
cv2.rectangle(mask, (cX - 75, cY - 75), (cX + 75, cY + 75), 255, -1)
cv2.imshow("Mask", mask)

masked = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Mask Applied to Image", masked)

cv2.waitKey(0)

# Circular mask
image = cv2.imread("testudo.jpg")
image = imutils.resize(image, width=400)

cv2.imshow("Original", image)

mask = np.zeros(image.shape[:2], dtype = "uint8")
(cX, cY) = (image.shape[1]/2, image.shape[0]/2)
cv2.circle(mask, (cX, cY), 100, 255, -1)
cv2.imshow("Mask", mask)

masked = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Mask Applied to Image", masked)

cv2.waitKey(0)


