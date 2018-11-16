# ENME 489Y: Remote Sensing

# import the necessary packages
import time
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt

##### PULL OUT THE TOP CAMERA IMAGERY #####

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('home/pi/cam12topview.avi',fourcc,10,(1280, 720))

# define video capture
# original script playes stoplight.mp4
# feel free to change 'stoplight.mp4' to filename of your choosing
cap = cv2.VideoCapture('home/pi/cam12.avi')

# initial frame counter to track pertinent frames
frame = 0
print "Frame number: "

# loop through until entire video file is played
while(cap.isOpened()):
    frame = frame + 1
    print frame

    ret, image = cap.read()
    if ret ==  False:       # break out of loop if no frame is found
        break

    # Black out the top left corner
    video = image[0:image.shape[0]/2,0:image.shape[1]]
    cv2.imshow("Top Camera", video)
    print video.shape[1]
    print video.shape[0]

    time.sleep(0.01)

    # write the frame to video file
    # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    out.write(video)

	# press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
print "----- All done! -----"
cap.release()
cv2.destroyAllWindows()


##### PULL OUT THE BOTTOM CAMERA IMAGERY #####

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('home/pi/cam12bottomview.avi',fourcc,10,(1280, 720))

# define video capture
# original script playes stoplight.mp4
# feel free to change 'stoplight.mp4' to filename of your choosing
cap = cv2.VideoCapture('home/pi/cam12.avi')

# initial frame counter to track pertinent frames
frame = 0
print "Frame number: "

# loop through until entire video file is played
while(cap.isOpened()):
    frame = frame + 1
    print frame

    ret, image = cap.read()
    if ret ==  False:       # break out of loop if no frame is found
        break

    # Black out the top left corner
    video = image[image.shape[0]/2:image.shape[0],0:image.shape[1]]
    cv2.imshow("Bottom Camera", video)
    print video.shape[1]
    print video.shape[0]

    time.sleep(0.01)

    # write the frame to video file
    # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    out.write(video)

	# press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
print "----- All done! -----"
cap.release()
cv2.destroyAllWindows()












##### PULL OUT THE TOP CAMERA IMAGERY #####

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('home/pi/cam34topview.avi',fourcc,10,(1280, 720))

# define video capture
# original script playes stoplight.mp4
# feel free to change 'stoplight.mp4' to filename of your choosing
cap = cv2.VideoCapture('home/pi/cam34.avi')

# initial frame counter to track pertinent frames
frame = 0
print "Frame number: "

# loop through until entire video file is played
while(cap.isOpened()):
    frame = frame + 1
    print frame

    ret, image = cap.read()
    if ret ==  False:       # break out of loop if no frame is found
        break

    # Black out the top left corner
    video = image[0:image.shape[0]/2,0:image.shape[1]]
    cv2.imshow("Top Camera", video)
    print video.shape[1]
    print video.shape[0]

    time.sleep(0.01)

    # write the frame to video file
    # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    out.write(video)

	# press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
print "----- All done! -----"
cap.release()
cv2.destroyAllWindows()


##### PULL OUT THE BOTTOM CAMERA IMAGERY #####

# define the codec and create VideoWriter object
# UNCOMMENT THE FOLLOWING TWO (2) LINES TO SAVE .avi VIDEO FILE
# TRY BOTH XVID THEN MJPG, IN THE EVENT THE .avi FILE IS NOT SAVING PROPERLY
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('home/pi/cam34bottomview.avi',fourcc,10,(1280, 720))

# define video capture
# original script playes stoplight.mp4
# feel free to change 'stoplight.mp4' to filename of your choosing
cap = cv2.VideoCapture('home/pi/cam34.avi')

# initial frame counter to track pertinent frames
frame = 0
print "Frame number: "

# loop through until entire video file is played
while(cap.isOpened()):
    frame = frame + 1
    print frame

    ret, image = cap.read()
    if ret ==  False:       # break out of loop if no frame is found
        break

    # Black out the top left corner
    video = image[image.shape[0]/2:image.shape[0],0:image.shape[1]]
    cv2.imshow("Bottom Camera", video)
    print video.shape[1]
    print video.shape[0]

    time.sleep(0.01)

    # write the frame to video file
    # UNCOMMENT THE FOLLOWING ONE (1) LINE TO SAVE .avi VIDEO FILE
    out.write(video)

	# press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# clear everything once finished
print "----- All done! -----"
cap.release()
cv2.destroyAllWindows()
