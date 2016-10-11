from gopigo import *
import GoPiGoModel as model
import operator
import main as helper
import numpy as np

US_SENSOR_PORT = 15
STEP_SIZE = 0.2
DIST_OBSTACLE = 15 
ROBOT_FIRST_MOVE = True
ENCODER_PPR = 18 # Pulses Per Revolution
STEPS_TO_MOVE = 4.534 
SLOPE = helper.get_slope_to_target()
MLINE_COEFF = helper.get_intercept()
MLINE_CROSSER = False 

locationHistory = []
obstacleHistory = []
SERVO_ANGLE = 90
def get_robot_world_location():
	return locationHistory[-1]
# stores the location of the robot with respect
# to the world coordinate frame in the location history
def store_robot_world_location(newRobotLocation):
        print "Robot locaiton is " + str(newRobotLocation[0]) + " " + str(newRobotLocation[1]) +  " " +  str(np.rad2deg(newRobotLocation[2]))
	locationHistory.append(newRobotLocation)
# stores the location of an object measured by the location
# of the robot and the lection of an object with respect to it 
def store_obstacle_location(servoAngle):
	obstacleCoordinate = model.us2world(get_robot_world_location(), distance_to_obstacle(), servoAngle)
	obstacleHistory.append(obstacleCoordinate)

def get_location_history():
    return locationHistory

def get_obstacle_history():
    return obstacleHistory
    
def distance_to_obstacle():
	return us_dist(US_SENSOR_PORT)

def follow_obstacle():
        #if distance_to_obstacle() < DIST_OBSTACLE:
        #        return
        angle_to_rotate_to = rotate_clockwise()
        stop()
	helper.rotate_left(angle_to_rotate_to)
	time.sleep(3)
        servo(20)
        global SERVO_ANGLE
	SERVO_ANGLE = 0
        move_obstacle_periphery()

def move_obstacle_periphery():
	global ROBOT_FIRST_MOVE
        distance = distance_to_obstacle()
    	while True:
	    	helper.go_forward(STEPS_TO_MOVE)
	    	if is_point_on_mline() and not ROBOT_FIRST_MOVE:
		    	break	
                if is_point_in_history(get_robot_world_location()):
                        print "robot got lost in loop"
                        break
                if distance > DIST_OBSTACLE:
		    	tilt_closer_to_object()
	    	else: 
		    	tilt_away_from_object()
                
                distance = distance_to_obstacle()
		ROBOT_FIRST_MOVE = False

def rotate_clockwise():
# Rotate till the distance from the intial recorded is different
	obstacle_distance = distance_to_obstacle()
        i = 0
        global SERVO_ANGLE
	while obstacle_distance == distance_to_obstacle():
	    servo(90 + i)
            time.sleep(1)
	    SERVO_ANGLE = 90 + i
            i += 23
	return i

def angle_closest_to_sensor_multiple(angle):
        multiplier = int (angle / 22.5)
        new_angle = multiplier * angle
        remainder = angle % 22.5
        if remainder > 22.5/2:
            new_angle += 22.5
        return new_angle

def tilt_closer_to_object():
	while distance_to_obstacle() > DIST_OBSTACLE: 
                helper.rotate_right(22.5)
                time.sleep(1)
def tilt_away_from_object():
	while distance_to_obstacle() <  DIST_OBSTACLE: 
                helper.rotate_left(22.5)
                time.sleep(1)

def is_point_on_mline():
	robot_location = get_robot_world_location()
	robot_x = robot_location[0]
	robot_y = robot_location[1]
	wanted_y = SLOPE * robot_x + MLINE_COEFF
	if helper.tolerant_equal([0,wanted_y],[0,robot_y]):
		return True
	elif wanted_y >= robot_y and not MLINE_CROSSER:
		return True
	elif wanted_y < robot_y and MLINE_CROSSER:
		return True
	return False

def set_m_line():
	robot_location = get_robot_world_location()
	robot_x = robot_location[0]
        robot_y = robot_location[1]
	m_line_y  = robot_x * SLOPE + MLINE_COEFF
	if m_line_y >= robot_y:
		MLINE_CROSSER = False
        else:
                MLINE_CROSSER = True
# checks if coordinate a has been found in the coordinate history,
# considering the tolerance to account for real world deviations
def is_point_in_history(a):
    for point in locationHistory:
        if helper.tolerant_equal(a,point):
            return 1
    return 0
		
def initial_setup():
	enable_servo()
	servo(90)
        time.sleep(0.5)
        SERVO_ANGLE = 90
	set_m_line()
	store_obstacle_location(SERVO_ANGLE)
	follow_obstacle()
    	stop()
