# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import RPi.GPIO as GPIO
import time

# use GPIO pin numbers
GPIO.setmode(GPIO.BCM)

#define pins

DirectionOneM1 = 23
DirectionTwoM1 = 24

DirectionOneM2 = 22
DirectionTwoM2 = 27

# set pins as output

GPIO.setup(DirectionOneM1, GPIO.OUT)
GPIO.setup(DirectionTwoM1, GPIO.OUT)

GPIO.setup(DirectionOneM2, GPIO.OUT)
GPIO.setup(DirectionTwoM2, GPIO.OUT)

GPIO.output(DirectionOneM1, GPIO.LOW)
GPIO.output(DirectionTwoM1, GPIO.LOW)

GPIO.output(DirectionOneM2, GPIO.LOW)
GPIO.output(DirectionTwoM2, GPIO.LOW)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
redUpper = (190, 255, 255)
redLower = (160,160,10)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    nfr = cv2.flip(frame, 0)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(nfr, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "red", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        myint = int(M["m10"] / M["m00"])

	print (myint)
#	mybool = (350 > myint and myint > 250) 
	#print (mybool)
#	if (not mybool):
	    
	if myint > 475:
            #print ('left')
            GPIO.output(DirectionOneM1, GPIO.LOW)
            GPIO.output(DirectionTwoM1, GPIO.LOW)

	    GPIO.output(DirectionOneM2, GPIO.HIGH)
            GPIO.output(DirectionTwoM2, GPIO.LOW)
	elif myint < 125:
            #print ('right')
            GPIO.output(DirectionOneM1, GPIO.HIGH)
            GPIO.output(DirectionTwoM1, GPIO.LOW)

            GPIO.output(DirectionOneM2, GPIO.LOW)
            GPIO.output(DirectionTwoM2, GPIO.LOW)
	else:
#            print ('stay (x-position)')
#            GPIO.output(DirectionOneM1, GPIO.LOW)
#            GPIO.output(DirectionTwoM1, GPIO.LOW)

#            GPIO.output(DirectionOneM2, GPIO.LOW)
#            GPIO.output(DirectionOneM2, GPIO.LOW)

            if (radius > 250):
	        #print ('too close (move backward)')
	        GPIO.output(DirectionOneM1, GPIO.LOW)
	        GPIO.output(DirectionTwoM1, GPIO.HIGH)	    

	        GPIO.output(DirectionOneM2, GPIO.LOW)
	        GPIO.output(DirectionTwoM2, GPIO.HIGH)
            elif (radius < 250) and (radius > 150):
	        #print ('stay (distance is okay)')
	        GPIO.output(DirectionOneM1, GPIO.LOW)
	        GPIO.output(DirectionTwoM1, GPIO.LOW)

	        GPIO.output(DirectionOneM2, GPIO.LOW)
	        GPIO.output(DirectionTwoM2, GPIO.LOW)
            elif (radius < 150):
	        #print ('too far (move forward)')
	        GPIO.output(DirectionOneM1, GPIO.HIGH)
	        GPIO.output(DirectionTwoM1, GPIO.LOW)
	    
	        GPIO.output(DirectionOneM2, GPIO.HIGH)
	        GPIO.output(DirectionTwoM2, GPIO.LOW)
        # only proceed if the radius meets a minimum size

#        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
#            cv2.circle(nfr, (int(x), int(y)), int(radius),(0, 255, 255), 2)
#            cv2.circle(frame, center, 5, (0, 0, 255), -1)
#        else:
#            GPIO.output(DirectionOneM1, GPIO.LOW)
#            GPIO.output(DirectionTwoM1, GPIO.LOW)

#            GPIO.output(DirectionOneM2, GPIO.LOW)
#            GPIO.output(DirectionTwoM2, GPIO.LOW)
    # show the frame to our screen
#    GPIO.output(DirectionOneM1, GPIO.LOW)
#    GPIO.output(DirectionTwoM1, GPIO.LOW)

#    GPIO.output(DirectionOneM2, GPIO.LOW)
#    GPIO.output(DirectionTwoM2, GPIO.LOW)
    cv2.imshow("Frame", nfr)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
GPIO.cleanup()
