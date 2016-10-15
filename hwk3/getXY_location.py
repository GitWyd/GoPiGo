from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
list_of_clicks = []
hsv_color = []
FIRST_TIME_CALC_XY = False

def getxy_callback(event, x, y, flags, param):
    global list_of_clicks
    if event == cv2.EVENT_LBUTTONDOWN :
        list_of_clicks.append([x,y])
        print "Click point is...", (x,y)

def bgr_to_hsv(color):
    hsv_pixel = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    return hsv_pixel

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # warmup time for camera
    time.sleep(0.1)
    #define click event

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', getxy_callback)
    print "Please select the color by clicking on the screen..."
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        #show the image
        cv2.imshow('frame', image)
        cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        # Calculation for color of clicked point
        if not FIRST_TIME_CALC_XY and list_of_clicks:           
            clicked_color_xy = list_of_clicks[0]
            print "IMAGE PIXEL XY CO-ORDS-"
            print image[clicked_color_xy[0]][clicked_color_xy[1]]
            pixels = []
            # xy
            pixels.append(image[clicked_color_xy[0]][clicked_color_xy[1]])
            # xy_upper        
            pixels.append(image[clicked_color_xy[0] + 1][clicked_color_xy[1]])
            # xy_lower        
            pixels.append(image[clicked_color_xy[0] - 1][clicked_color_xy[1]])
            # xy_upper_left   
            pixels.append(image[clicked_color_xy[0] + 1][clicked_color_xy[1] - 1])
            # xy_upper_right  
            pixels.append(image[clicked_color_xy[0] + 1][clicked_color_xy[1] + 1])
            # xy_lower_left   
            pixels.append(image[clicked_color_xy[0] - 1][clicked_color_xy[1] - 1])
            # xy_lower_right
            pixels.append(image[clicked_color_xy[0] - 1][clicked_color_xy[1] + 1])
            # xy_right        
            pixels.append(image[clicked_color_xy[0]][clicked_color_xy[1] + 1])
            # xy_left
            pixels.append(image[clicked_color_xy[0]][clicked_color_xy[1] - 1])
            global hsv_color
            for pixel in pixels:
                color = np.uint8([[pixel]])
                
                hsv_color.append(bgr_to_hsv(color))
            print "HSV TRANSFORMATION"
            print hsv_color
            FIRST_TIME_CALC_XY = True
