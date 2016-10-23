from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time

list_of_clicks = [] # lists the clicks in the picture
FIRST_TIME_CALC_XY = False
image = [[]]
final_hsv = [[]]
final_hsv_flip = False
hue_color = 0 # color of pixel clicked on

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
   # angle_to_rotate_to = 90 - tani(int(center[1]/center[0]))
   # diff = 0
   # if area > initial_area
   #     diff = area - initial_area
   #     enc_tgt(1, 1, diff)
   #     bwd()
   # else if area < initial_area
   #     diff = initial_area - area
   #     enc_tgt(1, 1, diff)
   #     fwd()

def bgr_to_hsv(color):
    hsv_pixel = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    return hsv_pixel

# find color overage over neighboring pixels
def get_hue_color(x, y): 
    pixels = []
    # xy
    pixels.append(image[x][y])
    # xy_upper        
    pixels.append(image[x+1][y])
    # xy_lower        
    pixels.append(image[x-1][y])
    # xy_upper        
    pixels.append(image[x-1][y+1])
    #
    pixels.append(image[x][y-1])
    # xy_upper        
    pixels.append(image[x+1][y+1])
    #
    pixels.append(image[x][y+1])
    # xy_upper        
    pixels.append(image[x+1][y-1])
    pixels.append(image[x-1][y-1])
    hsv_color = []
    for pixel in pixels:
        color = np.uint8([[pixel]])
        hsv_color.append(bgr_to_hsv(color))
    
    #new_color = np.uint8([[image[x][y]]])
    #hsv_mask = bgr_to_hsv(new_color)

    # hsv color value of color we want to match
    hsv_mask = np.mean(np.array(hsv_color), axis=0)
    # get hue_value from mask
    hue_color = hsv_mask[0][0][0]
    return hue_color
    
def show_selected_color(hue_color):
     # convert image to hsv
     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
     # define range of colors
     # HUE_TOLERANCE, SAT_THRESHOLD, VAL_THRESHOLD
     lower_hue = np.array([hue_color - 5,120,120])
     upper_hue = np.array([hue_color + 5,255,255])
     # blacks all pixels outside of the defined bounds
     mask = cv2.inRange(hsv_image, lower_hue, upper_hue)
      
     #res = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
     #gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
     
     # threhold gives boundaries to the object & marks all the pixels with the HUE Color & sets them white
     ret, thresh = cv2.threshold(mask, hue_color, 255, cv2.THRESH_BINARY)
     
     # mask that we run through image to erode the image
     # KERNEL_SIZE
     kernel = np.ones((5,5),np.uint8) * 255 # 255 - value for white
     erosion = cv2.erode(thresh, kernel, iterations = 1)
     # compensate for erosion by dialating with the same kernel
     dilation = cv2.dilate(erosion, kernel, iterations = 1)
     
     #_, contours, hierarchy = cv2.findContours(thresh, 1, 2)

     #cnt = contours[0]
     #print "Contours"
     #print cnt
     #M = cv2.moments(cnt)
     #print "Moments"
     #print M
     #Centroid calculations
     #cx = int(M['m10']/M['m00'])
     #cy = int(M['m01']/M['m00'])
     
     #print "Centroid"
     #print cx,cy
     #print image[y][x]

     # takes dialated image copy & computes moments (contour, perimeter, shapes, etc.)
     # cnts stores contours
     cnts = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
     center = None

     if len(cnts) > 0:
         print "Inside len cnts"
         # maximum value of cnts given the key contourArea
         c = max(cnts, key=cv2.contourArea)
         # enclosing circle value extracted
         ((x,y), radius) = cv2.minEnclosingCircle(c)
         M = cv2.moments(c)
         # centroid calculation
         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
         #print "Area is ", M["m00"]
         #print "Center and Radius", center," ", radius 
         cv2.circle(dilation, (int(x), int(y)), int(radius), (0, 255, 255), 2)
         cv2.circle(dilation, center, 5, (0, 0, 255), -1)
     # ToDo: area needs to be defined
     # checkout contourArea and connectedComponents (1 is the object, 1 whole frame)
     # we need to make a centroid a global variable and find the angle
     # set initial distance with ultrasonic sensor
     move_robot(area, center)
     global final_hsv
     global final_hsv_flip
     final_hsv = dilation
     final_hsv_flip = True
     return final_hsv

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # warmup time for camera
    time.sleep(0.1)
    #define click event
    cv2.namedWindow('frame')
    # call back getxy_callback() onClick
    cv2.setMouseCallback('frame', getxy_callback)
    print "Please select the color by clicking on the screen..."
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        image = frame.array
        # and occupied/unoccupied text
        # destroy original frame and only show 
        # binarized image of selected color
        if final_hsv_flip:
            cv2.destroyWindow('frame')
            new_im = show_selected_color(hue_color)
            cv2.imshow('target', new_im)
        else:
            cv2.imshow('frame', image)
        cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
    cv2.destroyAllWindows()
