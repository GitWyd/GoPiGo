from gopigo import *                              
import math                                       
import time                                       
                                                  
US_MAX_DIST = 300                           
US_PIN = 15                                       
ROTATE_SPEED = 50
DRIVE_SPEED = 80
TIME_INCREMENTS = 0.20
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 18 # Pulses Per Revolution          

DISTANCE_TO_TARGET = 300
DIRECTION = True #True = Left, False = right      
APPROACHING_DIST = 22   
DPR = 360.0/64

TARGET_X = 4
TARGET_Y = 5

SOURCE_X = 0
SOURCE_Y = 0

STEPS_TO_MOVE = 1
#1 Align the robot to the target
#2 Get distance to the target
#3 Move on m-line towards the target
#4 Check for obstacles
#4.1 if obstacles - follow obstacle till m-line
	# if m-line check if distance is less than previously calculated
	# else continue
#4.2 else 3
def align_robot_to_target(source_x, source_y, target_x, target_y):
	# Angle to target
	angle = angle_to_target(source_x, source_y, target_x, target_y)
	rotate_to_degrees(DIRECTION, angle_to_target)
	DISTANCE_TO_TARGET = get_distance_to_target(source_x, source_y, target_x, target_y)

def angle_to_target():
	return math.degrees(math.atan((target_y - source_y)/(target_x - source_x)))

def rotate_to_degrees(angle):
	if angle <= 90:
		pulse = int(90 - angle/DPR)
		enc_tgt(1,1,pulse)
		right_rot()
	else:
		pulse = int((angle - 90)/DPR)
		enc_tgt(1, 1, pulse)
		left_rot()

def get_distance_to_target(source_x, source_y, target_x, target_y):
	return math.abs((target_y - source_y)/(target_x - source_x))
	
def follow_line():
	
    while(TARGET_NOT_FOUND):
	    if isObstacle():
	    	follow_obstacle()
	    else:
	    	go_forward(STEPS_TO_MOVE)

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
    align_robot_to_target(SOURCE_X, SOURCE_Y, TARGET_X, TARGET_Y)
    follow_line()
    stop()