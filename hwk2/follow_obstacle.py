from gopigo import *
import operator
import main as helper
US_SENSOR_PORT = 15
STEP_SIZE = 0.2
DIST_OBTACLE = 10
ROBOT_FIRST_MOVE = True
WHEEL_CIRCUMFERENCE = 20.4
ENCODER_PPR = 18 # Pulses Per Revolution
STEPS_TO_MOVE = 1

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

def intial_setup():
	enable_servo()
	time.sleep(2)	
	servo(90)
	follow_obstacle()
    	stop()

