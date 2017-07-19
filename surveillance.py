import argparse
import imutils
import cv2
import RPi.GPIO as GPIO
import time

# use GPIO numbering system

GPIO.setmode(GPIO.BCM)

# initialize/declare pin number variables
DirectionOneM1 = 23
DirectionTwoM1 = 24

DirectionOneM2 = 22
DirectionTwoM2 = 27

GPIO.setup(DirectionOneM1, GPIO.OUT)
GPIO.setup(DirectionTwoM1, GPIO.OUT)

GPIO.setup(DirectionOneM2, GPIO.OUT)
GPIO.setup(DirectionTwoM2, GPIO.OUT)

# set all pins to LOW(off)

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

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

while True:
    #grab the current frame
    (grabbed, frame) = camera.read()

    #if did not grab a frame - video is over
    if args.get("video") and not grabbed:
	break

    #resize fram and flip it
    frame = imutils.resize(frame, width=600)
    frame = cv2.flip(frame, 0)

    #show frame to screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
	break
    elif key == ord("w"):
	GPIO.output(DirectionOneM1, GPIO.HIGH)
	GPIO.output(DirectionTwoM1, GPIO.LOW)
	GPIO.output(DirectionOneM2, GPIO.HIGH)
	GPIO.output(DirectionTwoM2, GPIO.LOW)
    elif key == ord("s"):
        GPIO.output(DirectionOneM1, GPIO.LOW)
        GPIO.output(DirectionTwoM1, GPIO.HIGH)
        GPIO.output(DirectionOneM2, GPIO.LOW)
        GPIO.output(DirectionTwoM2, GPIO.HIGH)
    elif key == ord("a"):
        GPIO.output(DirectionOneM1, GPIO.LOW)
        GPIO.output(DirectionTwoM1, GPIO.LOW)
        GPIO.output(DirectionOneM2, GPIO.HIGH)
        GPIO.output(DirectionTwoM2, GPIO.LOW)
    elif key == ord("d"):
        GPIO.output(DirectionOneM1, GPIO.HIGH)
        GPIO.output(DirectionTwoM1, GPIO.LOW)
        GPIO.output(DirectionOneM2, GPIO.LOW)
        GPIO.output(DirectionTwoM2, GPIO.LOW)
    elif key == ord("e"):
        GPIO.output(DirectionOneM1, GPIO.LOW)
        GPIO.output(DirectionTwoM1, GPIO.LOW)
        GPIO.output(DirectionOneM2, GPIO.LOW)
        GPIO.output(DirectionTwoM2, GPIO.LOW)

camera.release()
cv2.destroyAllWindows()
GPIO.cleanup()	
