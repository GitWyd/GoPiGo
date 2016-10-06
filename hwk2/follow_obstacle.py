from gopigo import *

US_SENSOR_PORT = 15
STEP_SIZE = 0.2
DIST_OBTACLE = 10
ROBOT_FIRST_MOVE = True
WHEEL_CIRCUMFERENCE = 20.4
ENCODER_PPR = 18 # Pulses Per Revolution
STEPS_TO_MOVE = 1
GOAL = [5,3,1]
SLOPE = 1
MLINE_COEFF = 4
MLINE_CROSSER = False 

def get_robot_world_location():
	// Retrieve something stored here

def store_robot_world_location():
	// Store something here

def distance_to_obstacle():
	return us_dist(US_SENSOR_PORT)

def follow_obstacle():
	store_obstacle_location()
	if distance_to_obstacle() < DIST_OBSTACLE:
		break
	angle_to_rotate_to = rotate_clockwise()
	servo(0)
	rotate_to_degree(angle_to_rotate_to)
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

def rotate_to_degrees(angle):
	if angle <= 90:
		pulse = int(90 - angle/DPR)
		enc_tgt(1,1,pulse)
		right_rot()
	else:										               pulse = int((angle - 90)/DPR)
		enc_tgt(1, 1, pulse) 
		left_rot()

def rotate_clockwise():
/* Rotate till the distance from the intial recorded is different*/
	obstacle_distance = distance_to_obstacle() 
	while eq obstacle_ditance distance_to_obstacle():
		for i in range(10,90,10)
		servo(90 + i)
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
	rotate_right(80);
	move_forward(cms if not None else STEP_SIZE);
    
def tilt_away_from_object(cms):
	rotate_left(100);
	move_forward(cms if not None else STEP_SIZE);

def is_point_on_m_line(robot_location):
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
	robot_location = get_robot_location()
	robot_x = robot_location[0]
	m_line_y  = (robot_x - MLINE_COEFF)/SLOPE
	if m_line_y > robot_y:
		MLINE_CROSSER = False
	else MLINE_CROSSER = True
		

def intial_setup():
	enable_servo()
	time.sleep(2)	
	servo(90)
	follow_obstacle()
	set_m_line()
    	stop()

