# ENME 489Y: Remote Sensing

# Color picker code
# This file takes an RGB image input and dynamically creates
# a HSV color mask

# HOW TO USE: enter the following into the RPi command window
#
# source ~/.profile
# workon cv
# python colorpicker.py -f HSV -i name_of_image_file.jpg
#
# where name_of_image_file.jpg is the name of the file
# for which you want to create a HSV mask


import cv2
import imutils
from operator import xor

print "All packages installed properly!"


def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)

def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values


def main():
    range_filter = 'hsv'

    image = cv2.imread("20190219.jpg")
    image = imutils.resize(image, width=600)

    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    setup_trackbars(range_filter)

    while True:
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        cv2.imshow("Original", image)
        cv2.imshow("Thresh", thresh)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()
