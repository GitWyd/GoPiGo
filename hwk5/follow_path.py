from gopigo import *
import numpy as np
from point import Point
#Constants
DPR = 360.0/64 # Degrees Per Revoluation
WHEEL_CIRCUMFERENCE = 21.7
ENCODER_PPR = 18 # Pulses Per Revolution          
DPP = WHEEL_CIRCUMFERENCE/ENCODER_PPR
SPEED = 140 # speed for GoForward
TURN_SPEED = 60 # speed for rotating
MIN_DIST_TOP_OBSTACLE = 5.5 # distance to be kept from obstacles
US_SENSOR_PORT  = 15
STEP_SCALAR = 3
# global variables
orient_robot = None
loc_robot = None
loc_target = None

def turn_to_target():
	global loc_target
	global loc_robot
	tgt_x, tgt_y = (loc_target.x, loc_target.y)
	src_x, src_y = (loc_robot.x, loc_robot.y)
	theta =  math.degrees(math.atan((tgt_y - src_y)/(tgt_x - src_x)))
	orientation = orient_robot
	if theta > orientation:
		turn_angle = theta-orientation
                print('rotate left by: ' + str(turn_angle))
		rotate_left(turn_angle)
	if theta < orientation:
		turn_angle = orientation-theta
                print('rotate right by: ' + str(turn_angle))
		rotate_right(turn_angle)

def dist_to_obstacle():
	dist = []
	for i in range(3):
		dist.append(us_dist(US_SENSOR_PORT))
	dist = sum(dist)/len(dist)
	# compensate for measurment error based on HWK1
	if dist>=30:
		dist-=8
	if dist>=60:
		dist-=8
	return dist

def cm2pulse(distance):
    distToWheelRatio = float(distance / WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR)
    return encoder_counts

# move robot in a straight line
def move_forward(dist):
    set_speed(SPEED)
    global loc_robot
    global orient_robot
    pulse = cm2pulse(dist)
    if pulse == 0:
        return
    enc_tgt(1,1,pulse)
    fwd()
    time.sleep(0.3*pulse)
    x = loc_robot.x + dist*math.cos(np.deg2rad(orient_robot))
    y = loc_robot.x + dist*math.sin(np.deg2rad(orient_robot))
    loc_robot = Point(x,y)

def go_to_target():
	dist = loc_robot.dist_to(loc_target)
	steps = int(dist/STEP_SCALAR)
        stepsize = float(dist/steps)
        print('go straight for: ' + str(dist))
        while (dist_to_obstacle()>MIN_DIST_TOP_OBSTACLE) and steps>0:
		move_forward(stepsize)
                print('Steps to go: ' +str(steps) +'robot location: ' + str(loc_robot) + '\t orientation: ' + str(orient_robot))
		steps -= 1


# turns left by theta degrees and updates the robots orientation
def rotate_left(theta):
    set_speed(TURN_SPEED)
    pulse = int (theta/DPR)
    pulse /= 2
    if not pulse:
		return
    # update robot location
    global orient_robot
    orient_robot += theta 
    enc_tgt(1,1, pulse)
    left_rot()
    time.sleep(1)

# turns right by theta degrees and updates the robots orientation
def rotate_right(theta):
    pulse = int (theta/DPR)
    pulse /= 2
    if not pulse:
		return
    # update robot location
    global orient_robot
    orient_robot -= theta 
    enc_tgt(1,1, pulse)
    right_rot()
    time.sleep(1)

def follow_path(path, robot_location, robot_orientation):
    enable_servo()
    # initialize robot
    global loc_robot
    global orient_robot
    global loc_target
    loc_robot = robot_location
    orient_robot = robot_orientation
    print('robot location: ' + str(loc_robot) + '\t orientation: ' + str(orient_robot))
    for pt in path[1:]:
                print "Next Point to go to: " + str(pt)
		loc_target = pt
		turn_to_target()
		go_to_target()
                print('robot location: ' + str(loc_robot) + '\t orientation: ' + str(orient_robot))
                time.sleep(1)
