
# A simple particle filter from Sebastian thrun's Mobile Robot MOOC
# Robot has x,y, theta location
# Sensing is distance of robot from 4 landmarks (with sensor noise)
# movement is arbitrary with sensor noise

import time
from turtle import *
import math
import numpy as np
import random
from draw_world import Maze
from GoPiGoModel import getNewRobotLocation
# from gopigo import *

# REAL ROBOT CONSTANTS
DIST_OBSTACLE = 15 
US_MAX_DIST = 300                           
US_PIN = 15                                       
ROTATE_SPEED = 50
SPEED = 100
TIME_INCREMENTS = 0.20
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 18 # Pulses Per Revolution          


# ENVIRONMENT / ROBOT CONSTANTS 
CONE = 5.7
NOISE_FWD = 0.05
NOISE_ROT = 0.025
NOISE_US  = 1.05
DIST_US = 7
R_TURN = 0.4
R_MOVE = 3.4

landmarks = []
obstacles = []
world_x = 0.0
world_y = 0.0
lines = []
def set_environment_boundaries(x,y):
    # Not sure about the first line
    # This is just a yukky looking function. Sorry about that. 
    global lines
    line1 = Line() 
    line2 = Line() 
    line3 = Line()
    line4 = Line() 
    line5 = Line()
    line1.set_equation(0, 0, x, 0) # x axis
    line2.set_equation(0, 0, 0, y) # y axis
    line3.set_equation(x, 0, x, y) # perpendicular to x, || to y
    line4.set_equation(0, y, x, y) # perpendicular to y, || to x
    line5.set_equation(0, 0, 1, 1)
    lines.append(line1)
    lines.append(line2)
    lines.append(line3)
    lines.append(line4)

    # intersection_point = line1.find_intersection_with_line(myrobot.get_angle_line())
    # if intersection_point:
    #     print 'found ' + str(intersection_point[0]) + ' ' + str(intersection_point[1])
    # else:
    #     print 'fucked up logic of intersection'

    # intersection_point = line2.find_intersection_with_line(myrobot.get_angle_line())
    # if intersection_point:
    #     print 'found ' + str(intersection_point[0]) + ' ' + str(intersection_point[1])
    # else:
    #     print 'fucked up logic of intersection'

    # intersection_point = line3.find_intersection_with_line(myrobot.get_angle_line())
    # if intersection_point:
    #     print 'found ' + str(intersection_point[0]) + ' ' + str(intersection_point[1])
    # else:
    #     print 'fucked up logic of intersection'

    # intersection_point = line4.find_intersection_with_line(myrobot.get_angle_line())
    # if intersection_point:
    #     print 'found ' + str(intersection_point[0]) + ' ' + str(intersection_point[1])
    # else:
    #     print 'fucked up logic of intersection'

def set_cone_boundaries(x, y):
    # setting the boundaries of the cone as lines
    global lines
    line1 = Line()
    line2 = Line()
    line3 = Line() 
    line4 = Line()
    line1.set_equation(x - CONE, y - CONE, x + CONE, y - CONE) # left bottom point to right bottom point
    line2.set_equation(x - CONE, y - CONE, x - CONE, y + CONE) # left bottom point to left top point
    line3.set_equation(x - CONE, y + CONE, x + CONE, y + CONE) # left top point to top right point
    line4.set_equation(x + CONE, y - CONE, x + CONE, y + CONE) # right bottom point to top right point
    lines.append(line1)
    lines.append(line2)
    lines.append(line3)
    lines.append(line4)

def initialize_world():
    global obstacles
    obstacles = [obstacle.rstrip('\n') for obstacle in open('obstacles.txt')] 
    global world_x
    global world_y
    world_x = float(obstacles[0].split()[0])
    world_y = float(obstacles[0].split()[1])
    print 'world x,y ', world_x, ' ', world_y
    # generate lines of env. borders 
    set_environment_boundaries(world_x, world_y) 
    # generate lines of obstacles / cones
    for obstacle in obstacles:
        x = float(obstacle.split()[0])
        y = float(obstacle.split()[1])
        print 'landmark x and y ', x, ' ', y
        set_cone_boundaries(x, y) # consider renaming
        global landmarks
        landmarks.append([x, y])
    print_lines_landmarks()

# prints lines and landmarks
def print_lines_landmarks():
    global lines
    global landmarks
    for line in lines:
        print 'line ', line.get_line()
    for landmark in landmarks:
        print 'landmark ', landmark

class robot:
    def __init__(self, isRobot = 0):
        self.isRobot = isRobot
        self.has_collided = False
        # random values are uniformly distributed
        self.x = random.random() * world_x
        self.y = random.random() * world_y
        self.orientation = random.random() * 2.0 * pi
        # define ultrasonic location
        self.usX = self.x + DIST_US * cos(self.orientation)
        self.usY = self.y + DIST_US * sin(self.orientation)
        self.usPhi = self.orientation - pi/2
        # define noise variables
        self.forward_noise = NOISE_FWD;
        self.turn_noise = NOISE_ROT;
        self.sense_noise = NOISE_US;
        # adding these to conform with the functions added.
        # coord_one and coord_two are two points on the imaginary
        # line made by the US sensor
        self.coord_one = [self.usX, self.usY]
        self.coord_two = [0.0, 0.0]
        self.angle_line = (self.coord_one,self.coord_two)

    def set_angle_line(self, angle):
        # print "Setting angle equation"
        # Finding out new point on line created by us sensor and the
        # beam it emits out. Formula is x = old_x + cos(theta).
        new_x = self.usX + DIST_US * cos(self.usPhi + angle)
        new_y = self.usY + DIST_US * sin(self.usPhi + angle)
        # print 'x and y' + str(self.x) + str(self.y)
        self.coord_two = [new_x, new_y]
        # print 'coord_two ' + str(self.coord_two)
        # print 'coord_one ' + str(self.coord_one)
        self.angle_line = (self.coord_one, self.coord_two)

    def get_angle_line(self):
        return (self.coord_one, self.coord_two)
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_x:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_y:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        self.usX = self.x + DIST_US * cos(self.orientation)
        self.usY = self.y + DIST_US * sin(self.orientation)
        self.usPhi = self.orientation - pi/2

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise = float(new_t_noise);
        self.sense_noise = float(new_s_noise);

    def virtual_scan(self):
        us_scan_readings = []
        # enable_servo() to be done here for actual robot

        # Iterating through the angles (at every 20 degrees)
        for i in range(0,180,20):
            # servo(i) for actual robot
            self.set_angle_line(np.deg2rad(i))
            min_dist = 200
            for j in range(len(lines)):
                # finding intersection points and only storing the least
                intersection_point = lines[j].find_intersection_with_line(self.get_angle_line())
                if intersection_point: 
                    dist = sqrt((self.usX - intersection_point[0]) ** 2 + (self.usY - intersection_point[1]) ** 2)
                    dist += random.gauss(0.0, self.sense_noise)
                    min_dist = min(min_dist, dist)
            us_scan_readings.append(min_dist)
        return us_scan_readings

    def move(self, turn, forward):
        x = self.x
        y = self.y
        orientation = self.orientation
        if turn:
            # turn, and add randomness to the turning command
            orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
            orientation %= 2 * pi

#        if self.isRobot:
        if forward:
            # move, and add randomness to the motion command
            dist = float(forward) + random.gauss(0.0, self.forward_noise)
            x = self.x + (cos(orientation) * dist)
            y = self.y + (sin(orientation) * dist)
            x %= world_x
            y %= world_y
        # set particle & return new particle with new location
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def is_path_clear(self):
        obstacle_bool = False
        bounds_bool = False
        readings = self.virtual_scan()
        dist = readings[4]
        # print(str(dist))
        if dist <= ( R_MOVE + self.forward_noise*3 ):
            obstacle_bool = False
        else:
            obstacle_bool = True
        if self.isRobot:
            dist = float(R_MOVE) + 3 * self.forward_noise
            x = self.x + (cos(self.orientation) * dist)
            y = self.y + (sin(self.orientation) * dist)
            if x < 0 or x >= world_x:
                     return False
            if y < 0 or y >= world_y:
                    return False
        return obstacle_bool

    def is_robot_path_clear(self):
        servo(90)
        return R_MOVE < us_dist(15)

    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        if self.has_collided:
            return 0.0
        prtcl_measurements = self.virtual_scan() 
        # calculates how likely a measurement should be
        prob = 1.0;
        for i in range(len(measurement)):
            dist = prtcl_measurements[i]
            p = self.Gaussian(measurement[i], self.sense_noise, dist) 
            if (dist - measurement[i] <= 15):
                prob += p
            else:
                prob += self.Gaussian(1, self.sense_noise, 50) 
            # if (dist-measurement[i]<=19):
            #     prob *= p
            # else:
            #     prob *= self.Gaussian(0, self.sense_noise, 25) 



            #     prob *= 0.0000000000000001 
            #print 'dist ' + str(dist) + '\t meas[i]' + str(measurement[i]) + '\t prob' + str(prob)
        #     if probability:
        #        prob += math.log(probability, 2)
        #print 'prob ' + str(prob)
        # prob = np.log(2, prob)
        return prob
    def robot_measurements(self):
        enable_servo()
        measurements = []
        for i in range(0,180,20):
            dist = 200
            servo(i)
            if (dist > us_dist(15)):
                dist = us_dist(15)
            measurements.append(dist)
        return measurements    
    def move_robot(self, turn, forward):
        x = self.x
        y = self.y
        orientation = self.orientation
        if turn:
            # turn, and add randomness to the turning command
            self.rotate_left(turn)

#        if self.isRobot:
        if forward:
            # move, and add randomness to the motion command
            dist = float(forward) + random.gauss(0.0, self.forward_noise)
            self.go_forward(dist)

    def go_forward(self, distance):
        set_speed(SPEED)
        pulse = self.cm2pulse(distance)
        if pulse == 0:
            return
            enc_tgt(1,1,pulse)
            fwd()
            time.sleep(1)
        # new_robot_world_location = model.getNewRobotLocation(distance,old_robot_location,0)
        dist = float(distance) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        self.set(x, y, self.orientation)

    def cm2pulse(self, distance):
        distToWheelRatio = float(distance / WHEEL_CIRCUMFERENCE)
        encoder_counts = int(distToWheelRatio*ENCODER_PPR)
        return encoder_counts

    def rotate_left(self, angle):
        pulse = int (angle/DPR)
        pulse /= 2
        if not pulse:
            return
        # update robot location
        orientation = self.orientation + float(angle) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        self.set(self.x, self.y, orientation)
        enc_tgt(1,1, pulse)
        left_rot()
        time.sleep(1)

    def rotate_right(self, angle):
        pulse = int (angle/DPR)
        pulse /= 2
        if not pulse:
            return
        # update robot location
        orientation = self.orientation + float(angle) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        self.set(self.x, self.y, orientation)
        enc_tgt(1,1, pulse)
        right_rot()
        time.sleep(1)
    def __repr__(self):
        return '\n\t[x=%.6s y=%.6s orient=%.6s] \n\t[usX=%.6s usY=%.6s usPhi=%.6s]' % (str(self.x), str(self.y), str(self.orientation), str(self.usX), str(self.usY), str(self.usPhi))

class Line:
    def __init__(self):
        # coord_one and coord_two are two points 
        # for the line of obstacles
        self.coord_one = [0.0, 0.0]
        self.coord_two = [0.0, 0.0]
    
    def find_intersection_with_line(self, line2):
        # Method to find intersection between two lines
        line1 = (self.coord_one, self.coord_two)
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])        
        div = det(xdiff, ydiff)
        if div == 0:
            print 'div 0'
            return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        # Checking if the intersection point is within the range. line2 is the line made by the robot sensor. 
        if (((x >= line1[0][0] and x <= line1[1][0]) or (x <= line1[0][0] and x >= line1[1][0])) \
            and ((y >= line1[0][1] and y <= line1[1][1]) or (y <= line1[0][1] and y >= line1[1][1]))):
            return x, y
        else:
            return None

    def set_equation(self, x1, y1, x2, y2):
        self.coord_one = [x1, y1]
        self.coord_two = [x2, y2]
    
    def get_line(self):
        return (self.coord_one, self.coord_two)
    
def det(a, b):
    return a[0] * b[1] - a[1] * b[0]
    

def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].usX - r.usX + (world_x/2.0)) % world_x - (world_x/2.0)
        dy = (p[i].usY - r.usY + (world_y/2.0)) % world_y - (world_y/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def initialize():
    print 'in initialize'

# --------
N = 3000 # number of particles
T = 80  # number of iterations

initialize_world()
isEvaluated = False

obstacle_bounds = []
for landmark in landmarks[1:]:
    x = landmark[0]
    y = landmark[1]
    top_right = [x + CONE,y + CONE]
    top_left = [x - CONE, y + CONE]
    bottom_right = [x + CONE, y - CONE]
    bottom_left = [x - CONE, y - CONE]

    obstacle_bounds.append([top_right,top_left,bottom_left,bottom_right])

graph_world = Maze(world_x, world_y, obstacle_bounds)
graph_world.draw()
p = [] # list of particlesw
for i in range(N):
    r = robot()
    r.set_noise(NOISE_FWD, NOISE_ROT, NOISE_US) # provided noise.
    p.append(r)

myrobot = robot()
myrobot.isRobot = True
myrobot.set_noise(NOISE_FWD, NOISE_ROT, NOISE_US)

print 'Mean error at start', eval(myrobot, p)
# show particle's initial locations
#print p

w = []
for i in range(N):
    w.append(0)
graph_world.show_particles(p, w, isEvaluated)
graph_world.show_robot(myrobot)


for t in range(T):
#    print p
    # if there is an obstacle then turn
    # otherwise move forward
    clearPath = myrobot.is_path_clear()
    if clearPath:
        myrobot= myrobot.move(0, R_MOVE)
    else:
        myrobot = myrobot.move(R_TURN, 0)
    Z = myrobot.virtual_scan()
    
    # move all robots by the same as the actual robot 
    p_temp = []
    for i in range(N):
        if clearPath:
            if  not p[i].is_path_clear():
                p[i].has_collided = True
            p_temp.append(p[i].move(0, R_MOVE))
        else:
            p_temp.append(p[i].move(R_TURN, 0))

    p = p_temp
    
    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(Z))
    p3 = []

# this is importance sampling code
    index = int(random.random() * N)
    beta = 0.0 # what is beta
    mw = max(w)
    sum_w = sum(weight for weight in w)

    for i in range(len(w)):
        w[i] = w[i]/mw
    # print 'mw ' + str(mw)
    mw = max(w)
    for i in range(N):

        beta += random.random() * 3 * mw
        # print 'w ' + str(w[1:3])
        # print 'mw ' + str(mw)
        # print 'beta ' + str(beta)
        while beta > w[index]:
            # print "Beta and Index " + str(beta)+ " " + str(index)
            beta -= w[index]
            index = (index + 1) % N
        #print 'robot current location: ' + str(myrobot.x) +" " +str(myrobot.y)
        #print 'particle added: ' + str(p[index])
        # print 'particle ' + str(p[index])
        p3.append(p[index])
    p = p3

    if t%2 == 0:
        graph_world.show_particles(p, w, isEvaluated)
        graph_world.show_robot(myrobot)
        time.sleep(2)   
    
    print 'Mean error',eval(myrobot, p)
    # if eval(myrobot, p) < 6.0:
    #     for i in range(N/100):        
    #         print 'Final particle #', i*100, p[i*100]
    #     print ' '
    #     print 'Actual Robot Location', myrobot
    #     exitonclick()
    clearstamps()

graph_world.show_particles(p, w, True)
graph_world.show_robot(myrobot)
    
print ' '
if eval(myrobot, p) >= 0.0:
    for i in range(N/100):        
        print 'Final particle #', i*100, p[i*100]
    print ' '
    print 'Actual Robot Location', myrobot
    #print p
    exitonclick()
