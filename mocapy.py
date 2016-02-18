# import the necessary packages
from __future__ import print_function
import cv2
import time
import datetime
import imutils
 
camera = cv2.VideoCapture(0)
time.sleep(1)

minarea = 200

(grabbed, frame) = camera.read()
frame = imutils.resize(frame, width=500)
gray0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray0 = cv2.GaussianBlur(gray0, (21, 21), 0)
time.sleep(0.5)
(grabbed, frame) = camera.read()
frame = imutils.resize(frame, width=500)
gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
time.sleep(0.5)
firstFrame = frame

while True:
    grabbed = False
    while not grabbed:
        (grabbed, frame) = camera.read()
    timestamp = datetime.datetime.now()

    text = "Ruhe"
 
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
    
    # if the first frame is None, initialize it
    # if firstFrame is None:
    	# firstFrame = gray
    	# continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta1 = cv2.absdiff(gray0, gray1)
    frameDelta2 = cv2.absdiff(gray1, gray2)
    frameDelta = cv2.absdiff(frameDelta1, frameDelta2)
    thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]
    
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    # 	cv2.CHAIN_APPROX_SIMPLE)
    
    # loop over the contours
    for c in cnts:
    	# if the contour is too small, ignore it
    	if cv2.contourArea(c) < minarea:
    		continue
    
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
    	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    	text = "Bewegung"
    # draw the text and timestamp on the frame
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
    # show the frame and record if the user presses a key
    if cv2.countNonZero(thresh) > minarea:
        cv2.imwrite(datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg',frame)
    cv2.imshow("Security Feed", frame)


    gray0 = gray1
    gray1 = gray2
    time.sleep(1.0)


    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
 
    # cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
