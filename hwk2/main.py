from gopigo import *                              
import math                                       
import time                                       
import follow_obstacle as follow_obstacle   
import GoPiGoModel as Model

DIST_OBTACLE = 10
US_MAX_DIST = 300                           
US_PIN = 15                                       
ROTATE_SPEED = 50
DRIVE_SPEED = 100
TIME_INCREMENTS = 0.20
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 18 # Pulses Per Revolution          

DISTANCE_TO_TARGET = 0
DIRECTION = True #True = Left, False = right      
APPROACHING_DIST = 22   
DPR = 360.0/64 # Degrees Per Revoluation

TARGET_X = 4
TARGET_Y = 5

SOURCE_X = 0
SOURCE_Y = 0
SLOPE_TO_TARGET = 0
INTERCEPT = 0
TARGET_FOUND = False

STEPS_TO_MOVE = 1
#1 Align the robot to the target
#2 Get distance to the target
#3 Move on m-line towards the target
#4 Check for obstacles
#4.1 if obstacles - follow obstacle till m-line
	# if m-line check if distance is less than previously calculated
	# else continue
#4.2 else 3
def align_robot_to_target():
	# Angle to target
	rotate_to_degrees(angle_to_target())
	DISTANCE_TO_TARGET = get_distance_to_target()

def angle_to_target():
	return math.degrees(math.atan((TARGET_Y - SOURCE_Y)/(TARGET_X - SOURCE_X)))

def rotate_to_degrees(angle):
	pulse = int(math.abs(90 - angle)/DPR)
	enc_tgt(1,1,pulse)
	if angle <= 90:
		right_rot()
	else:
		left_rot()

def get_distance_to_target():
	return math.pow((TARGET_Y - SOURCE_Y),2) + math.pow((TARGET_X - SOURCE_X),2)

def get_slope_to_target():
	SLOPE_TO_TARGET = math.abs((TARGET_Y - SOURCE_Y)/(TARGET_X - SOURCE_X))
	return SLOPE_TO_TARGET

def get_intercept():
	INTERCEPT = TARGET_Y - SLOPE_TO_TARGET * TARGET_X
	return INTERCEPT

def follow_line():
	print "Getting world location"
    coords = follow_obstacle.get_robot_worl_location
    print "Co-ordinates" + str(coords)
	if(coords[0] == TARGET_X and coords[1] == TARGET_Y):
		print "Did we really do this. We actuallly found the target"
		TARGET_FOUND = True
		break
    elif follow_obstacle.distance_to_obstacle() <= DIST_OBTACLE: :
    	print "Calling anshuman's code for obstacle follow"
    	stop()
		follow_obstacle.initial_setup()
    else:
    	print "Moving forward reaaaalllllly slowly"
    	go_forward(STEPS_TO_MOVE)
    	time.sleep(0.2)

def go_forward(distance):
	set_speed(SPEED)
	pulse = cm2pulse(STEPS_TO_MOVE)
    enc_tgt(1,1,pulse)
    fwd()

def cm2pulse(distance):
	distToWheelRatio = float(abs(distance) / WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR) 
    return encoder_counts

if __name__=='__main__': 
    enable_servo()
    align_robot_to_target()

    print "Found target alignment. Lets go"
    while not TARGET_FOUND:
    	print "Target still not found"
    	follow_line()
