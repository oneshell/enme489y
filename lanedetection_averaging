# ENME 489Y: Remote Sensing
# Week 4: Basic Lane Detection
# Code includes lane averaging & transparent lane overlays

# Import packages
import numpy as np
import argparse
import cv2
import imutils

print "All packages imported properly!"

# Identify filename of video
cap = cv2.VideoCapture('lanedetectiontestvideo.mp4')

# Initialize frame counter
counter = 0

# Initialize arrays for averaging across multiple frames
x_1 = []
x_2 = []
x_3 = []
x_4 = []
y_1 = []
y_2 = []
y_3 = []
y_4 = []

# Initialize averaging counters
z = 0
zz = 0

# Loop through until entire video file is played
while(cap.isOpened()):

    print counter
    counter = counter + 1

    # Read video frame & show on screen
    ret, frame = cap.read()
    final_output = frame.copy()

    # Snip region of video frame of interest & show on screen
    snip = frame[500:700,300:900]

    # Create polygon (trapezoid) mask to select region of interest
    mask = np.zeros((snip.shape[0], snip.shape[1]), dtype="uint8")
    pts = np.array([[25, 190], [275, 50], [380, 50], [575, 190]], dtype=np.int32)
    cv2.fillConvexPoly(mask, pts, 255)

    # Apply mask & show masked image on screen
    masked = cv2.bitwise_and(snip, snip, mask=mask)

    # convert to grayscale then black/white to binary image
    frame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    thresh = 200
    frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]

    # blur image to help with edge detection
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # identify edges & show on screen
    edged = cv2.Canny(blurred, 30, 150)

    # perform full Hough Transform to identify lane lines
    lines = cv2.HoughLines(edged, 1, np.pi / 180, 25)

    # initialize arrays for left and right lanes
    rho_left = []
    theta_left = []
    rho_right = []
    theta_right = []

    # ensure cv2.HoughLines found at least one line
    if lines is not None:

        # loop through all of the lines found by cv2.HoughLines
        for i in range(0, len(lines)):

            # evaluate each row of cv2.HoughLines output 'lines'
            for rho, theta in lines[i]:

                # collect left lanes
                if theta < np.pi/2 and theta > np.pi/4:
                    rho_left.append(rho)
                    theta_left.append(theta)

                    # # plot all lane lines for DEMO PURPOSES ONLY
                    a = np.cos(theta); b = np.sin(theta)
                    x0 = a * rho; y0 = b * rho
                    x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                    x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))

                # collect right lanes
                if theta > np.pi/2 and theta < 3*np.pi/4:
                    rho_right.append(rho)
                    theta_right.append(theta)

                    # # plot all lane lines for DEMO PURPOSES ONLY
                    a = np.cos(theta); b = np.sin(theta)
                    x0 = a * rho; y0 = b * rho
                    x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                    x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))

    # statistics to identify median lane dimensions
    left_rho = np.median(rho_left)
    left_theta = np.median(theta_left)
    right_rho = np.median(rho_right)
    right_theta = np.median(theta_right)

    # plot median lane on top of scene snip
    if left_theta > np.pi/4:
        a = np.cos(left_theta); b = np.sin(left_theta)
        x0 = a * left_rho + 300; y0 = b * left_rho + 500
        offset1 = 200; offset2 = 400
        x1 = int(x0 - offset1 * (-b)); y1 = int(y0 - offset1 * (a))
        x2 = int(x0 + offset2 * (-b)); y2 = int(y0 + offset2 * (a))

        x_1.append(x1)
        x_2.append(x2)
        y_1.append(y1)
        y_2.append(y2)

        if len(x_1) > 15:

            x1 = np.average(x_1[z:len(x_1)])
            x1 = int(x1)
            x2 = np.average(x_2[z:len(x_2)])
            x2 = int(x2)
            y1 = np.average(y_1[z:len(y_1)])
            y1 = int(y1)
            y2 = np.average(y_2[z:len(y_2)])
            y2 = int(y2)

            z = z + 1

            # (1) create a copy of the original:
            overlay = final_output.copy()
            # (2) draw shapes:
            cv2.line(final_output, (x1, y1), (x2, y2), (0, 0, 255), 16)
            # (3) blend with the original:
            opacity = 0.4
            cv2.addWeighted(overlay, opacity, final_output, 1 - opacity, 0, final_output)

    if right_theta > np.pi/4:
        a = np.cos(right_theta); b = np.sin(right_theta)
        x0 = a * right_rho + 300; y0 = b * right_rho + 500
        offset1 = 335; offset2 = 800
        x3 = int(x0 - offset1 * (-b)); y3 = int(y0 - offset1 * (a))
        x4 = int(x0 - offset2 * (-b)); y4 = int(y0 - offset2 * (a))

        x_3.append(x3)
        x_4.append(x4)
        y_3.append(y3)
        y_4.append(y4)

        if len(x_3) > 5:

            x3 = np.average(x_3[zz:len(x_3)])
            x3 = int(x3)
            x4 = np.average(x_4[zz:len(x_4)])
            x4 = int(x4)
            y3 = np.average(y_3[zz:len(y_3)])
            y3 = int(y3)
            y4 = np.average(y_4[zz:len(y_4)])
            y4 = int(y4)

            zz = zz + 1

        # (1) create a copy of the original:
        overlay = final_output.copy()
        # (2) draw shapes:
        cv2.line(final_output, (x3, y3), (x4, y4), (0, 0, 255), 16)
        # (3) blend with the original:
        opacity = 0.4
        cv2.addWeighted(overlay, opacity, final_output, 1 - opacity, 0, final_output)

    cv2.imshow("Original Video", final_output)

    # press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
cap.release()
cv2.destroyAllWindows()


