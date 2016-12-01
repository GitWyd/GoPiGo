from gopigo import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
CONE = [178.0, 198.0, 249.0]
US_PORT = 15
SPEED = 80
# constants to define threshold
HUE_TOLERANCE = 5;
SAT_MIN = 120;
VAL_MIN = 120;
SAT_MAX = 255;
VAL_MAX = 255;
KERNEL_SIZE = 5; # size of n x n kernel
list_of_clicks = [] # lists the clicks in the picture
image = [[]]
final_hsv = [[]]
final_hsv_flip = False
is_initialized = False
hue_color = 0 # color of pixel clicked on
initial_area = None # initial area measured
initial_distance = 20 # initial measured distance
def getxy_callback(event, x, y, flags, param):
    global list_of_clicks
    if event == cv2.EVENT_LBUTTONDOWN :
        list_of_clicks.append([x,y])
        print "Click point: ", (x,y)
        print "Image coords", image[y][x]
        global hue_color
        # average color with neighboring pixels
        # stores global hue-value
        hue_color = get_hue_color(y,x)
        global final_hsv_flip
        final_hsv_flip = True

def move_robot(area, center):
    set_speed(SPEED)
    tolerance = 5000
    px_tolerance = 40
    centroid_x = center[0]
#    centroid_y = center[1]
#    print "center[0]: " + str(centroid_x) + "\t center[1]: " + str(centroid_y)
#    centroid_dist = (initial_distance/initial_area)*area-initial_distance
#    angle_to_rotate_to = 90 - np.rad2deg(np.arctan(centroid_y/centroid_x))
    ang_diff = centroid_x-320
   # pulse_scalar = int(90*(initial_area/area))
   # pulses = abs(ang_diff)/pulse_scalar if abs(ang_diff)/pulse_scalar < 4 else 3
    pulses = 1
    if ang_diff > px_tolerance:
        print "turn right"
        enc_tgt(1,0,pulses)
        right_rot()
        time.sleep(1)
    elif ang_diff < -px_tolerance:
        print "turn right"
        enc_tgt(0,1,pulses)
        left_rot()
        time.sleep(1)
    print "initial area: " + str(initial_area) + "\t new area: " + str(area)
    diff = int(area/tolerance) - int(initial_area/tolerance)
    if diff > 0:
        print "move bwd() by "+ str(abs(diff)) 
        enc_tgt(1, 1, 2)
        bwd()
        time.sleep(0.5)
    elif diff < 0:
        print "move fwd() by "+ str(abs(diff))
        enc_tgt(1, 1, 2)
        fwd()
        time.sleep(0.5)
    return
def rotation(angle_to_rotate_to, diff):
    return
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
    # # call back getxy_callback() onClick
    # # cv2.setMouseCallback('frame', getxy_callback)
    # print "Please select the color by clicking on the screen..."
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        image = frame.array
        print image
        for pixel in image:
            print pixel
            color = np.uint8([[pixel[y][x]]])
            hsv_color = bgr_to_hsv(color)
            print "HSV for each pixel"

        # and occupied/unoccupied text
        # destroy original frame and only show 
        # binarized image of selected color
        new_im = show_selected_color(hue_color)
        cv2.imshow('target', new_im)
        cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
    cv2.destroyAllWindows()
