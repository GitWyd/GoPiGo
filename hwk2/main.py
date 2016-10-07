from gopigo import *                              
import math                                       
import time                                       
import numpy as np
import follow_obstacle as follow_obstacle   
import GoPiGoModel as model

DIST_OBTACLE = 10
US_MAX_DIST = 300                           
US_PIN = 15                                       
ROTATE_SPEED = 50
SPEED = 100
TIME_INCREMENTS = 0.20
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 18 # Pulses Per Revolution          

DISTANCE_TO_TARGET = 0
DIRECTION = True #True = Left, False = right      
APPROACHING_DIST = 22   
DPR = 360.0/64 # Degrees Per Revoluation

TARGET_X = 130
TARGET_Y = 0

SOURCE_X = 0
SOURCE_Y = 0

SLOPE_TO_TARGET = 0
INTERCEPT = 0
TARGET_FOUND = False

STEPS_TO_MOVE = 10
#1 Align the robot to the target
#2 Get distance to the target
#3 Move on m-line towards the target
#4 Check for obstacles
#4.1 if obstacles - follow obstacle till m-line
	# if m-line check if distance is less than previously calculated
	# else continue
#4.2 else 3
def align_robot_to_target():
    current_robot_world_location = model.getNewRobotLocation(0,follow_obstacle.get_robot_world_location(),np.deg2rad(angle_to_target()))
    follow_obstacle.store_robot_world_location(current_robot_world_location)
    # Angle to target
    rotate_left(angle_to_target())
    DISTANCE_TO_TARGET = get_distance_to_target()

def angle_to_target():
    return math.degrees(math.atan((TARGET_Y - SOURCE_Y)/(TARGET_X - SOURCE_X)))

def rotate_left(angle):
    pulse = int (angle/DPR)
    if not pulse:
	return
    # update robot location
    current_robot_world_location = model.getNewRobotLocation(0,follow_obstacle.get_robot_world_location(),np.deg2rad(angle))
    follow_obstacle.store_robot_world_location(current_robot_world_location)
    enc_tgt(0,1, pulse)
    left_rot()
    time.sleep(1) 

def rotate_right(angle):
    pulse = int (angle/DPR)
    if not pulse:
	return
    # update robot location
    current_robot_world_location = model.getNewRobotLocation(0,follow_obstacle.get_robot_world_location(),np.deg2rad(360-angle))
    follow_obstacle.store_robot_world_location(current_robot_world_location)
    enc_tgt(1,0, pulse)
    right_rot()
    time.sleep(1) 

def get_distance_to_target():
    return math.pow((TARGET_Y - SOURCE_Y),2) + math.pow((TARGET_X - SOURCE_X),2)

def get_slope_to_target():
    SLOPE_TO_TARGET = abs((TARGET_Y - SOURCE_Y)/(TARGET_X - SOURCE_X))
    return SLOPE_TO_TARGET

def get_intercept():
    INTERCEPT = TARGET_Y - SLOPE_TO_TARGET * TARGET_X
    return INTERCEPT

def follow_line():
    coords = follow_obstacle.get_robot_world_location()
    if coords[0] == TARGET_X and coords[1] == TARGET_Y:
        TARGET_FOUND = True
    elif follow_obstacle.distance_to_obstacle() <= DIST_OBTACLE:
        stop()
        follow_obstacle.initial_setup()
    else:
        go_forward(STEPS_TO_MOVE)
        time.sleep(0.2)

def go_forward(distance):
    set_speed(SPEED)
    pulse = cm2pulse(STEPS_TO_MOVE)
    enc_tgt(1,1,pulse)
    fwd()
    time.sleep(2)
    current_robot_world_location = model.getNewRobotLocation(distance,follow_obstacle.get_robot_world_location(),0)
    follow_obstacle.store_robot_world_location(current_robot_world_location)
    
   
def cm2pulse(distance):
    distToWheelRatio = float(abs(distance) / WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR)
    return encoder_counts

if __name__=='__main__': 
    enable_servo()
    follow_obstacle.store_robot_world_location([SOURCE_X,SOURCE_Y,0])
    align_robot_to_target()
    servo(90)
    time.sleep(2)
    while not TARGET_FOUND:
        follow_line()
