# ENME 489Y: Remote Sensing
# Basic Lane Detection

import numpy as np
import cv2
import imutils

# Identify filename of video
cap = cv2.VideoCapture('lanedetectiontestvideo.mp4')

# Initialize frame counter
counter = 0

# Loop through until entire video file is played
while(cap.isOpened()):

    counter = counter + 1
    print counter

    # Read video frame & show on screen
    ret, frame = cap.read()
    cv2.imshow("Original Video", frame)

    # Snip region of video frame of interest & show on screen
    snip = frame[500:700,300:900]
    cv2.imshow("Region of Interest",snip)

    # Create polygon (trapezoid) mask to select region of interest
    mask = np.zeros((snip.shape[0], snip.shape[1]), dtype="uint8")
    pts = np.array([[25, 190], [275, 50], [380, 50], [575, 190]], dtype=np.int32)
    cv2.fillConvexPoly(mask, pts, 255)
    cv2.imshow("Mask", mask)

    # Apply mask & show masked image on screen
    masked = cv2.bitwise_and(snip, snip, mask=mask)
    cv2.imshow("Region of Interest", masked)

    # Convert to grayscale
    frame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale", frame)

    # Black/white to binary image
    thresh = 200
    frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Black/White", frame)

    # Blur image to aid edge detection
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    cv2.imshow("Blurred", blurred)

    # Identify edges & show on screen
    edged = cv2.Canny(blurred, 30, 150)
    cv2.imshow("Edged", edged)

    # Perform Hough Transform to identify lane lines
    lines = cv2.HoughLines(edged, 1, np.pi / 180, 25)

    # Define empty arrays for left and right lanes
    rho_left = []
    theta_left = []
    rho_right = []
    theta_right = []

    # Ensure cv2.HoughLines identified at least one line
    if lines is not None:

        # Loop through all of the lines found by cv2.HoughLines
        for i in range(0, len(lines)):

            # Evaluate each row of cv2.HoughLines output 'lines'
            for rho, theta in lines[i]:

                # Show all lines -----DEMO PURPOSES ONLY-----
                # rho_left.append(rho)
                # theta_left.append(theta)
                #
                # a = np.cos(theta); b = np.sin(theta)
                # x0 = a * rho; y0 = b * rho
                # x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                # x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
                #
                # cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 1)


                # Collect left lanes
                if theta < np.pi/2 and theta > np.pi/4:
                    rho_left.append(rho)
                    theta_left.append(theta)

                    # Plot all lane lines for -----DEMO PURPOSES ONLY-----
                    # a = np.cos(theta); b = np.sin(theta)
                    # x0 = a * rho; y0 = b * rho
                    # x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                    # x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
                    #
                    # cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 1)

                # Collect right lanes
                if theta > np.pi/2 and theta < 3*np.pi/4:
                    rho_right.append(rho)
                    theta_right.append(theta)

                    # Plot all lane lines for -----DEMO PURPOSES ONLY-----
                    # a = np.cos(theta); b = np.sin(theta)
                    # x0 = a * rho; y0 = b * rho
                    # x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
                    # x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
                    #
                    # cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 1)

    # Statistics to identify median lane dimensions
    left_rho = np.median(rho_left)
    left_theta = np.median(theta_left)
    right_rho = np.median(rho_right)
    right_theta = np.median(theta_right)

    # Plot median lane on top of scene snip
    if left_theta > np.pi/4:
        a = np.cos(left_theta); b = np.sin(left_theta)
        x0 = a * left_rho; y0 = b * left_rho
        offset1 = 250; offset2 = 800
        x1 = int(x0 - offset1 * (-b)); y1 = int(y0 - offset1 * (a))
        x2 = int(x0 + offset2 * (-b)); y2 = int(y0 + offset2 * (a))

        cv2.line(snip, (x1, y1), (x2, y2), (0, 255, 0), 6)

    if right_theta > np.pi/4:
        a = np.cos(right_theta); b = np.sin(right_theta)
        x0 = a * right_rho; y0 = b * right_rho
        offset1 = 290; offset2 = 800
        x3 = int(x0 - offset1 * (-b)); y3 = int(y0 - offset1 * (a))
        x4 = int(x0 - offset2 * (-b)); y4 = int(y0 - offset2 * (a))

        cv2.line(snip, (x3, y3), (x4, y4), (255, 0, 0), 6)

    # Overlay semi-transparent lane outline on original
    if left_theta > np.pi/4 and right_theta > np.pi/4:
        pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.int32)

        # (1) create a copy of the original:
        overlay = snip.copy()
        # (2) draw shapes:
        cv2.fillConvexPoly(overlay, pts, (0, 255, 0))
        # (3) blend with the original:
        opacity = 0.4
        cv2.addWeighted(overlay, opacity, snip, 1 - opacity, 0, snip)

    cv2.imshow("Lined", snip)

    # perform probablistic Hough Transform to identify lane lines
    # lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 20, 2, 1)
    # for x in range(0, len(lines)):
    #     for x1, y1, x2, y2 in lines[x]:
    #         cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
cap.release()
cv2.destroyAllWindows()




