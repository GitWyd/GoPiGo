from gopigo import *
from obstacle import Point
Constants
DPR = 360.0/64 # Degrees Per Revoluation
WHEEL_CIRCUMFERENCE = 20.4
ENCODER_PPR = 18 # Pulses Per Revolution          
DPP = WHEEL_CIRCUMFERENCE/ENCODER_PPR
SPEED = 120 # speed for GoForward
TURN_SPEED = 60 # speed for rotating
MIN_DIST_TOP_OBSTACLE = 5.5 # distance to be kept from obstacles
# global variables
orient_robot = None
loc_robot = None
loc_target = None

def turn_to_target():
	global loc_target
	global loc_robot
	tgt_x, tgt_y = (loc_target.x, loc_target.y)
	src_x, src_y = (loc_robot.x, loc_robot.y)
	theta =  math.degrees(math.atan((tgt_Y - src_y)/(tgt_x - src_x)))
	orientation = np.rad2deg(orient_robot)
	if theta > orientation:
		turn_angle = theta-orientation
		rotate_left(turn_angle)
	if theta < orientation:
		turn_angle = orientation-theta
		rotate_right(turn_angle)
def go_to_target():
	dist = loc_robot.dist_to(loc_target)
	steps = dist/DPP
	while (dist_to_obstacle()>MIN_DIST_TOP_OBSTACLE) and steps
		move_forward(dist/steps)
		steps -= 1
def distance_to_obstacle():
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
# move robot in a straight line
def move_fotward(dist):
    set_speed(SPEED)
    pulse = cm2pulse(dist)
    if pulse == 0:
        return
    enc_tgt(1,1,pulse)
    fwd()
    time.sleep(0.5*pulse)
    x = loc_robot.x + dist*cos(np.deg2rad(orientation))
    y = loc_robot.x + dist*sin(np.deg2rad(orientation))
    loc_robot = Point(x,y)
def cm2pulse(distance):
    distToWheelRatio = float(distance / WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR)
    return encoder_counts
# turns left by theta degrees and updates the robots orientation
def rotate_left(theta):
	set_speed(TURN_SPEED)
	pulse = int (angle/DPR)
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
	pulse = int (angle/DPR)
    pulse /= 2
    if not pulse:
		return
    # update robot location
    global orient_robot
    orient_robot -= theta 
    enc_tgt(1,1, pulse)
    left_rot()
    time.sleep(1)

def follow_path(path, robot_location, robot_orientation):
    enable_servo()
    # initialize robot
    loc_robot = robot_location
    orient_robot = robot_orientation

    for pt in path:
		loc_target = pt
		turn_to_target()
		go_to_target()
