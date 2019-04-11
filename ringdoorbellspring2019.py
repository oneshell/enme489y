# ENME489Y Spring 2019
# Code implements Ring Doorbell functionality on the Raspberry Pi

# Import necessary packages
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email 
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import numpy as np
from datetime import datetime
import time
import os
import cv2
import imutils

# Mask image such that the algorithm is triggered only by someone at the front door
def mask_image(img):
	mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")
	pts = np.array([[240, 475], [240, 420], [310, 420], [375, 410], [525, 350], [550, 100], [635,100], [635, 475]], dtype=np.int32)
	cv2.fillConvexPoly(mask, pts, 255)
	pts = np.array([[1, 395], [1, 315], [110, 305],[110, 365]], dtype=np.int32)
	cv2.fillConvexPoly(mask, pts, 255)
	masked = cv2.bitwise_and(img, img, mask=mask)
	gray = imutils.resize(masked, width=200)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21,21), 0)
	return gray

# take a 1st image to begin the comparison
command = 'raspistill -w 640 -h 480 -vf -hf -o ' +  'test1' + '.jpg'
os.system(command)

# Data on 1st image
test1 = cv2.imread("test1.jpg")
gray1 = mask_image(test1)

print "Sum of gray1: "
abs1 = np.uint64(0)
abs1 = np.uint64(np.sum(gray1))
print abs1

print "Captured 1st image & performed analytics...moving on to video loop"

# keep looping
counter = -1
while True:

	counter = counter + 1
	print counter
	time.sleep(0.01)

	# Take a 2nd image and see if someone is there
	command = 'raspistill -w 640 -h 480 -vf -hf -o ' +  'test2' + '.jpg'
	os.system(command)

	# Data on 2nd image
	test2 = cv2.imread("test2.jpg")
	gray2 = mask_image(test2)

	print "Sum of gray2: "
	abs2 = np.uint64(0)
	abs2 = np.uint64(np.sum(gray2))
	print abs2

	# Compare the two images
	pixel_thres = 50

	detector_total = np.uint64(0)
	detector = np.zeros((gray2.shape[0], gray2.shape[1], 3), dtype="uint8")

	for i in range(0,gray2.shape[0]):
		for j in range(0, gray2.shape[1]):
			if int(gray1[i,j])-int(gray2[i,j]) > pixel_thres or int(gray2[i,j])-int(gray1[i,j]) > pixel_thres and int(gray1[i,j]) > 0:
				detector[i,j] = 255

	if abs1 >= abs2:
		print " "
		print "Absolute difference of gray1 - gray2: "
		abs_diff = np.uint64(0)
		abs_diff = np.uint64(abs1 - abs2)
		print abs_diff
		print " "
	if abs1 < abs2:
		print " "
		print "Absolute difference of gray1 - gray2: "
		abs_diff = np.uint64(0)
		abs_diff = np.uint64(abs2 - abs1)
		print abs_diff
		print " "

	detector_total = np.uint64(np.sum(detector))
	print "detector_total = "
	print detector_total
	print " "

	# write the values of detector_total to file for post-processing
	f = open('ringlog.txt','a')
	now = datetime.now()
	timestamp = now.strftime("%Y/%m/%d %H:%M")
	outstring = str(timestamp)+" "+ str(detector_total)+"\n"
	f.write(outstring)
	f.close()

	if counter > 0 and detector_total > 30000:
		# logic: a 50 greyscale change over n-pixels is 50*n = ?...here 
		print "Ring has detected someone/something at the door!"

		# Define current time for email purposes
		f_time = datetime.now().strftime('%a %d %b @ %H:%M')
		image_time = datetime.now().strftime('%H%M')

		# define unique name for each new video file
		timestr = time.strftime("ringcameraview-%Y%m%d-%H%M%S")

		# Wrap this around the video recording to email time/length of video
		t_start = time.time()

		command1 = 'raspivid -t 30000 -w 640 -h 480 -fps 30 -vf -hf -o ' + timestr + '.h264'
		os.system(command1)

		t_stop = time.time()
		t_video = t_stop - t_start

		time.sleep(0.1)
		print "Finished recording .h264...now converting to .mp4"
		command2 = 'MP4Box -add ' + timestr + '.h264 ' + timestr + '.mp4'
		os.system(command2)

		print "Finished recording...now uploading..."
		time.sleep(0.1)

		fullDirectory = '/home/pi/' + timestr + '.mp4'
		command = '/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ' + fullDirectory + ' /Apps/GPIO'
		os.system(command)
		time.sleep(0.1)

		# Now send email to the user to confirm video has been recorded

		# Gmail login information
		smtpUser = 'YOUREMAILHERE@gmail.com'
		smtpPass = 'YOURPASSWORDHERE'

		# To/from information
		toAdd = 'DESTINATIONEMAILHERE@gmail.com'
		fromAdd = smtpUser
		subject = 'Ring recording from: ' + f_time 
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = fromAdd
		msg['To'] = toAdd
		msg.preamble = "Photo @ " + f_time

		# Email text
		body = email.mime.Text.MIMEText("Ring Video:  " + f_time + ", video length: " + str(t_video))
		msg.attach(body)

		# Attach both images to email
		fp = open('test1.jpg', 'rb')
		img = MIMEImage(fp.read())
		fp.close()
		msg.attach(img)
		fp = open('test2.jpg', 'rb')
		img = MIMEImage(fp.read())
		fp.close()
		msg.attach(img)

		# Send email
		s = smtplib.SMTP('smtp.gmail.com',587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(smtpUser, smtpPass)
		s.sendmail(fromAdd, toAdd, msg.as_string())
		s.quit()

		print "Email delivered " + f_time

		# Reset the time-out/shutdown counter to 0
		counter = 0

		# take a 1st image to begin the comparison
		command = 'raspistill -w 640 -h 480 -vf -hf -o ' +  'test1' + '.jpg'
		os.system(command)

		# Data on 1st image
		test1 = cv2.imread("test1.jpg")
		gray1 = mask_image(test1)

		print "Sum of gray1: "
		abs1 = np.uint64(0)
		abs1 = np.uint64(np.sum(gray1))
		print abs1

		print "Captured 1st image & performed analytics...moving on to video loop"

	# If not detection, then go ahead and recreate the 1st image
	else:
		print "Nothing detected...yet!"

		command = 'raspistill -w 640 -h 480 -vf -hf -o ' +  'test1' + '.jpg'
		os.system(command)

		# Data on 1st image
		test1 = cv2.imread("test1.jpg")
		gray1 = mask_image(test1)

		print "Sum of gray1: "
		abs1 = np.uint64(0)
		abs1 = np.uint64(np.sum(gray1))
		print abs1

		print "Captured 1st image & performed analytics...moving on to video loop"


