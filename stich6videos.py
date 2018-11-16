# ENME 489Y: Remote Sensing

# import the necessary packages
import time
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('home/pi/stitch6videos1.avi',fourcc,10,(3840, 1440))

# define video capture
# original script playes stoplight.mp4
# feel free to change 'stoplight.mp4' to filename of your choosing
cap = cv2.VideoCapture('home/pi/cam12topview.avi')
cap2 = cv2.VideoCapture('home/pi/cam12bottomview.avi')
cap3 = cv2.VideoCapture('home/pi/cam34topview.avi')
cap4 = cv2.VideoCapture('home/pi/cam34bottomview.avi')

# initial frame counter to track pertinent frames
frame = 0
print "Frame number: "

# loop through until entire video file is played
while(cap.isOpened()):
    frame = frame + 1
    print frame

    ret, image = cap.read()
    ret2, image2 = cap2.read()
    ret3, image3 = cap3.read()
    ret4, image4 = cap4.read()

    if ret ==  False:       # break out of loop if no frame is found
        break

    # create a blank image for the combined package, same dimensions as the plotfig
    canvas = np.zeros((image.shape[0],image.shape[1],3), dtype="uint8")
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    green = (0, 0, 255)
    cv2.putText(canvas, 'Camera View TBD', (200, 300), font, 4, green, 4)

    # horizontally stack things
    package1 = np.hstack([canvas,image,canvas])
    package2 = np.hstack([image3, image2, image4])

    # vertically stack things
    finalpackage = np.vstack([package1,package2])

    # print out the final shape of the package
    print finalpackage.shape

    time.sleep(0.01)

    # write the frame to video file
    # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    out.write(finalpackage)

    time.sleep(0.01)


	# press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
print "----- All done! -----"
cap.release()
cv2.destroyAllWindows()
