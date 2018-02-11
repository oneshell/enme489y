# ENME 489Y: Remote Sensing

# Python script plays the video file stoplight.mp4

# import the necessary packages
import time
import cv2

# define video capture
# original script playes stoplight.mp4
# feel free to change 'stoplight.mp4' to filename of your choosing
cap = cv2.VideoCapture('stoplight.mp4')

# loop through until entire video file is played
while(cap.isOpened()):
	ret, frame = cap.read()

	# show frame to the screen
	cv2.imshow('frame',frame)

	# press the q key to break out of video
	if cv2.waitKey(25) & 0xFF == ord('q'):
		break

# clear everything once finished
cap.release()
cv2.destroyAllWindows()

