from gopigo import *
import GoPiGoModel as model
import operator
import main as helper

US_SENSOR_PORT = 15
STEP_SIZE = 0.2
DIST_OBTACLE = 10
ROBOT_FIRST_MOVE = True
WHEEL_CIRCUMFERENCE = 20.4
ENCODER_PPR = 18 # Pulses Per Revolution
STEPS_TO_MOVE = 1
SLOPE = helper.get_slope_to_target()
MLINE_COEFF = helper.get_intercept()
MLINE_CROSSER = False 

locationHistory = []
obstacleHistory = []
servoAngle = 90
def get_robot_world_location():
	return locationHistory-1
# stores the location of the robot with respect
# to the world coordinate frame in the location history
def store_robot_world_location(newRobotLocation):
	locationHistory.append(newRobotLocation)
# stores the location of an object measured by the location
# of the robot and the lection of an object with respect to it 
def store_obstacle_location():
	obstacleCoordinate = model.us2world(locationHistory-1, distance_to_obstacle(), servoAngle)	
	obstacleHistory.append(obstacleCoordinate)

def distance_to_obstacle():
	return us_dist(US_SENSOR_PORT)

def follow_obstacle():
	store_obstacle_location()
	if distance_to_obstacle() < DIST_OBSTACLE:
		break
	angle_to_rotate_to = rotate_clockwise()
	servo(0)
	SERVO_ANGLE = 0
	rotate_to_degrees(angle_to_rotate_to)
	move_obstacle_periphery()

def move_obstacle_periphery():
    	while True:
	    	go_forward(STEP_SIZE)
	    	if is_point_on_mline() and not ROBOT_FIRST_MOVE:
		    	break	
	    	if distance_to_obstacle() < DIST_OBSTACLE:
		    	tilt_closer_to_object()
	    	else: 
		    	tilt_away_from_object()	
		ROBOT_FIRST_MOVE = False;

def rotate_clockwise():
# Rotate till the distance from the intial recorded is different
	obstacle_distance = distance_to_obstacle() 
	while obstacle_distance == distance_to_obstacle():
		for i in range(10,90,10):
			servo(90 + i)
			SERVO_ANGLE = 90 + i
	return 90 + i

def go_forward(distance):
	set_speed(SPEED)
	pulse = cm2pulse(STEPS_TO_MOVE)
	enc_tgt(1,1,pulse)
	fwd()

def cm2pulse(distance):
	distToWheelRatio = float(abs(distance) / WHEEL_CIRCUMFERENCE)
	encoder_counts = int(distToWheelRatio*ENCODER_PPR)
	return encoder_counts

def tilt_closer_to_object(cms):
	helper.rotate_to_degrees(80);
	go_forward(cms if not None else STEP_SIZE);
    
def tilt_away_from_object(cms):
	helper.rotate_to_degrees(100);
	go_forward(cms if not None else STEP_SIZE);

def is_point_on_m_line():
	robot_location = get_robot_world_location()
	robot_x = robot_location[0]
	robot_y = robot_location[1]
	wanted_y = SLOPE * robot_x + MLINE_COEFF
	if wanted_y - robot_y == 0:
		return True
	else if wanted_y > robot_y and MLINE_CROSSER:
		return True
	else if wanted_y < robot_y and not MLINE_CROSSER:
		return True
	return False

def set_m_line():
	robot_location = get_robot_world_location()
	robot_x = robot_location[0]
	m_line_y  = (robot_x - MLINE_COEFF)/SLOPE
	if m_line_y > robot_y:
		MLINE_CROSSER = False
	else MLINE_CROSSER = True
		
def intial_setup():
	enable_servo()
	time.sleep(2)	
	servo(90)
	SERVO_ANGLE = 90
	set_m_line()
	follow_obstacle()
    	stop()

