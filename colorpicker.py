# ENME 489Y: Remote Sensing

# Color picker code
# This file takes an RGB image input and dynamically creates
# a HSV color mask

# HOW TO USE: enter the following into the RPi command window
#
# python colorpicker.py -f HSV -i name_of_image_file.jpg
#
# where name_of_image_file.jpg is the name of the file
# for which you want to create a HSV mask


import cv2
import argparse
import imutils
from operator import xor



def callback(value):
	pass

def setup_trackbars(range_filter):
	cv2.namedWindow("Trackbars", 0)

	for i in ["MIN", "MAX"]:
		v = 0 if i == "MIN" else 255

		for j in range_filter:
			cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)

def get_arguments():
	ap = argparse.ArgumentParser()
	ap.add_argument('-f', '--filter', required=True,
		help='Range filter. RGB or HSV')
	ap.add_argument('-i', '--image', required=False,
		help='Path to the image')
	ap.add_argument('-w', '--webcam', required=False,
		help='Use webcam', action='store_true')
	ap.add_argument('-p', '--preview', required=False,
		help='Show a preview of the image after applying the mask',
		action='store_true')
	args = vars(ap.parse_args())

	if not xor(bool(args['image']), bool(args['webcam'])):
		ap.error("Please specify only one image source")

	if not args['filter'].upper() in ['RGB', 'HSV']:
		ap.error("Please speciy a correct filter.")

	return args


def get_trackbar_values(range_filter):
	values = []

	for i in ["MIN", "MAX"]:
		for j in range_filter:
			v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
			values.append(v)

	return values



def main():
	args = get_arguments()

	range_filter = args['filter'].upper()


	if args['image']:
		# ensure the name of your image file is
		# provided in the line below
		image = cv2.imread('laser_spot.jpg',1)
		# resize image to fit the screen
		# feel free to modify the value of "width" as desired
		image = imutils.resize(image, width=600)

		if range_filter == 'RGB':
			frame_to_thresh = image.copy()
		else:
			frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	else:
		camera = cv2.VideoCapture(0)

	setup_trackbars(range_filter)

	while True:
		if args['webcam']:
			ret, image = camera.read()
				
			if not ret:
				break

			if range_filter == 'RGB':
				frame_to_thresh = image.copy()
			else:
				frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		v1_min, v2_min, v3_min, v1_max,v2_max, v3_max = get_trackbar_values(range_filter)
	
		thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

		if args['preview']:
			preview = cv2.bitwise_and(image, image, mask=thresh)
			cv2.imshow("Preview", preview)
		else:
			cv2.imshow("Original", image)
			cv2.imshow("Thresh", thresh)

		if cv2.waitKey(1) & 0xFF is ord('q'):
			break


if __name__ == '__main__':
	main()
