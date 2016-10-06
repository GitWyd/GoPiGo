from gopigo import *

US_SENSOR_PORT = 15
STEP_SIZE = 0.2
DIST_OBTACLE = 10
ROBOT_FIRST_MOVE = True

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
	rotate_clockwise()
	servo(0)
	move_obstacle_periphery()

def move_obstacle_periphery():
    	while True:
	    	move_forward(STEP_SIZE)
	    	if is_point_on_mline() and not ROBOT_FIRST_MOVE:
		    	break	
	    	if distance_to_obstacle() < DIST_OBSTACLE:
		    	move_closer_to_object()
	    	else: 
		    	move_away_from_object()	
		ROBOT_FIRST_MOVE = False;
		

def rotate_clockwise():
/*Rotate till the distance from the intial recorded is different*/

def rotate_counter_clockwise():
/* Rotate till the distance from the intial recorded is different*/

def rotate_left(degrees):
/* Rotate counter clockwise by the specified amount of degrees*/

def rotate_right(degrees):
/* Rotate clockwise by the specified amount of degrees */

def move_forward(cms):

def move_backward(cms):

def move_closer_to_object(cms):
	rotate_right(90);
	move_forward(cms if not None else STEP_SIZE);
    
def move_away_from_object(cms):
	rotate_left(90);
	move_forward(cms if not None else STEP_SIZE);

if __name__=='__main__': 
    	enable_servo()
	time.sleep(2)	
	servo(90)
    	stop()

