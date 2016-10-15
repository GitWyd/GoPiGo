from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
list_of_clicks = []
def getxy_callback(event, x, y, flags, param):
    global list_of_clicks
    if event == cv2.EVENT_LBUTTONDOWN :
        list_of_clicks.append([x,y])
        print "click point is...", (x,y)

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # warmup time for camera
    time.sleep(0.1)
    #define click event

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', getxy_callback)
    print "Please select the color by clicking on the screen..."
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        #show the image
        cv2.imshow('frame', image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

    #obtain the matrix of the selected points
    print "The clicked points..."
    print list_of_clicks

