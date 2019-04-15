# ENME 489Y
# Facial Recognition
#
# Code derived from Adrian Rosebrock's work:
# https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/
#
# USAGE: type the following into Terminal window
# python detect_faces.py --image facialrecognition01.jpg --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
import numpy as np
import argparse
import cv2
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
image_original = cv2.imread(args["image"])
image_original = imutils.resize(image_original, width=800)
cv2.imshow("Original Image", image_original)

image = cv2.imread(args["image"])
image = imutils.resize(image, width=800)
cv2.imshow("Original Image", image)
#image = imutils.resize(image, width=800)
print(image.shape[0],image.shape[1])
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))

# pass the blob through the network and obtain the detections and
# predictions
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

# loop over the detections
for i in range(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections by ensuring the `confidence` is
	# greater than the minimum confidence
	if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for the
		# object
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
 
		# draw the bounding box of the face along with the associated
		# probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 255, 0), 2)
		cv2.putText(image, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

# show the output image
cv2.imshow("Output", image)

# Stack the original and processed images together
image = imutils.resize(image, width=600)
image_original = imutils.resize(image_original, width=600)
results = np.hstack([image_original, image])
cv2.imshow("Results", results)
cv2.imwrite("FacialRecognitionTest01.jpg", results)


cv2.waitKey(0)
