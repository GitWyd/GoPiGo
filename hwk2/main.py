from gopigo import *                              
import math                                       
import time                                       
import numpy as np
import follow_obstacle as follow_obstacle   
import GoPiGoModel as model
import plot_path

DIST_OBSTACLE = 10
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

TARGET_X = 300 
TARGET_Y = 0

SOURCE_X = 0
SOURCE_Y = 0

SLOPE_TO_TARGET = 0
INTERCEPT = 0
TARGET_FOUND = False

STEPS_TO_MOVE = 4.534
TARGET_ANGLE = 0
# tollerance for robot when finding target
TOLERANCE = 3
#1 Align the robot to the target
#2 Get distance to the target
#3 Move on m-line towards the target
#4 Check for obstacles
#4.1 if obstacles - follow obstacle till m-line
	# if m-line check if distance is less than previously calculated
	# else continue
#4.2 else 3
def align_robot_to_target():
    angle = angle_to_target()
    global TARGET_ANGLE
    TARGET_ANGLE = angle
    current_robot_world_location = model.getNewRobotLocation(0,follow_obstacle.get_robot_world_location(),np.deg2rad(angle))
    #current_robot_world_location[2] = np.deg2rad(angle)
    follow_obstacle.store_robot_world_location(current_robot_world_location)
    # Angle to target
    rotate_left(angle_to_target())
    DISTANCE_TO_TARGET = get_distance_to_target()

def angle_to_target(robot=None):
    if robot:
        slope = slope_to_target(robot)
        return math.degrees(math.atan(slope))
    return math.degrees(math.atan((TARGET_Y - SOURCE_Y)/(TARGET_X - SOURCE_X)))

def rotate_left(angle):
    pulse = int (angle/DPR)
    pulse /= 2
    if not pulse:
	return
    # update robot location
    new_robot_world_location = model.getNewRobotLocation(0,follow_obstacle.get_robot_world_location(),np.deg2rad(angle))
    #current_robot_world_location[2] += np.deg2rad(angle)
    follow_obstacle.store_robot_world_location(new_robot_world_location)
    enc_tgt(1,1, pulse)
    print "Rotate left angle and pulse :" + str(angle) + "  " + str(pulse)
    left_rot()
    time.sleep(1)

def rotate_right(angle):
    pulse = int (angle/DPR)
    pulse /= 2
    if not pulse:
	return
    # update robot location
    new_robot_world_location = model.getNewRobotLocation(0,follow_obstacle.get_robot_world_location(), np.deg2rad(angle*-1))
    follow_obstacle.store_robot_world_location(new_robot_world_location)
    enc_tgt(1,1, pulse)
    print "Rotate right angle and pulse :" + str(angle) + "  " + str(pulse)
    right_rot()
    time.sleep(1)

def get_distance_to_target():
    return math.pow((TARGET_Y - SOURCE_Y),2) + math.pow((TARGET_X - SOURCE_X),2)

def get_slope_to_target(robot = None):
    if robot:
        return abs((TARGET_Y - robot[1])/(TARGET_X - robot[0]))
    else:
        SLOPE_TO_TARGET = abs((TARGET_Y - SOURCE_Y)/(TARGET_X - SOURCE_X))
        return SLOPE_TO_TARGET

def get_intercept():
    INTERCEPT = TARGET_Y - SLOPE_TO_TARGET * TARGET_X
    return INTERCEPT

def follow_line():
    coords = follow_obstacle.get_robot_world_location()
    if tolerant_equal(coords, [TARGET_X,TARGET_Y]):
#    coords[0] == TARGET_X and coords[1] == TARGET_Y:
        global TARGET_FOUND
        TARGET_FOUND = True
        return
    elif follow_obstacle.distance_to_obstacle() <= DIST_OBSTACLE:
        stop()
        follow_obstacle.initial_setup()
        print "Follow obstacle over"
        time.sleep(1)
        servo(90)
        current_robot_location = follow_obstacle.get_robot_world_location()
        print "Location after finding line " + str(current_robot_location)
        new_angle = TARGET_ANGLE - np.rad2deg(current_robot_location[2])
        print "Target angle " + str(TARGET_ANGLE)
        print "New angle " + str(new_angle)
        if new_angle > 0:
            print "Rotate left " + str(abs(new_angle))
            rotate_left(abs(new_angle))
            time.sleep(1)
        else:
            print "Rotate right" + str(abs(new_angle))
            rotate_right(abs(new_angle))
            time.sleep(1)
    else:
        go_forward(STEPS_TO_MOVE)
        time.sleep(0.2)

def go_forward(distance):
    set_speed(SPEED)
    print "Distance is " + str(distance)
    pulse = cm2pulse(distance)
    print "Pulse is " + str(pulse)
    if pulse == 0:
        return
    enc_tgt(1,1,pulse)
    fwd()
    time.sleep(0.5)
    old_robot_location = follow_obstacle.get_robot_world_location() 
    new_robot_world_location = model.getNewRobotLocation(distance,old_robot_location,0)
    follow_obstacle.store_robot_world_location(new_robot_world_location)
    
def cm2pulse(distance):
    distToWheelRatio = float(distance / WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR)
    return encoder_counts
# takes two points a, and b in a vector format
# where the index 0 = x and index 1 = y value
def tolerant_equal(a, b):
    diff_x = abs(a[0]-b[0])
    diff_y = abs(a[1]-b[1])
    if (diff_x<TOLERANCE and diff_y<TOLERANCE):
        return True
    else:
        return False
if __name__=='__main__': 
    enable_servo()
    follow_obstacle.store_robot_world_location([SOURCE_X,SOURCE_Y,0])
    align_robot_to_target()
    servo(90)
    time.sleep(2)
    while not TARGET_FOUND:
        follow_line()
    stop()
    plot_path.plot_graph() 
    print "Reached Target!"
