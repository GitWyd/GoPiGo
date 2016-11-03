
# A simple particle filter from Sebastian thrun's Mobile Robot MOOC
# Robot has x,y, theta location
# Sensing is distance of robot from 4 landmarks (with sensor noise)
# movement is arbitrary with sensor noise


from math import *
import random

landmarks = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
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
    line1.set_equation(0, 0, x, 0) # x axis
    line2.set_equation(0, 0, 0, y) # y axis
    line3.set_equation(x, 0, x, y) # perpendicular to x, || to y
    line4.set_equation(0, y, x, y) # perpendicular to y, || to x
    lines.append(line1)
    lines.append(line2)
    lines.append(line3)
    lines.append(line4)

def set_cone_boundaries(x, y):
    # setting the boundaries of the cone as lines
    global lines
    line1 = Line()
    line2 = Line()
    line3 = Line() 
    line4 = Line()
    line1.set_equation(x - 5.7, y - 5.7, x + 5.7, y - 5.7) # left bottom point to right bottom point
    line2.set_equation(x - 5.7, y - 5.7, x - 5.7, y + 5.7) # left bottom point to left top point
    line3.set_equation(x - 5.7, y + 5.7, x + 5.7, y + 5.7) # left top point to top right point
    line4.set_equation(x + 5.7, y - 5.7, x + 5.7, y + 5.7) # right bottom point to top right point
    lines.append(line1)
    lines.append(line2)
    lines.append(line3)
    lines.append(line4)

def initialize_world():
    obstacles = [obstacle.rstrip('\n') for obstacle in open('obstacles.txt')] 
    global world_x
    global world_y
    world_x = float(obstacles[0].split()[0])
    world_y = float(obstacles[0].split()[1])
    print 'world x,y ', world_x, ' ', world_y 
    set_environment_boundaries(world_x, world_y)
    for obstacle in obstacles:
        x = float(obstacle.split()[0])
	y = float(obstacle.split()[1])
	print 'landmark x and y ', x, ' ', y
	set_cone_boundaries(x, y)
        global landmarks
        landmarks.append([x,y])
    for line in lines:
	print 'line ', line.get_line()
    for landmark in landmarks:
	print 'landmark ', landmark

class robot:
    def __init__(self, isRobot = 0):
        self.isRobot = isRobot
        self.x = random.random() * world_x
        self.y = random.random() * world_y
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise = 0.0;
        self.sense_noise = 0.0;
	# adding these to conform with the functions added.
	# coord_one and coord_two are two points on the imaginary
	# line made by the US sensor
	self.coord_one = [self.x, self.y]
	self.coord_two = [0.0, 0.0]
	self.angle_line = (self.coord_one,self.coord_two)

    def set_angle_line(angle):
	print "Setting angle equation"
	orientation_to_world_angle = self.orientation - pi / 2
	us_angle = orientation_to_world_angle + angle
	# Finding out new point on line created by us sensor and the
	# beam it emits out. Formula is x = old_x + cos(theta).
	new_x = self.x + 2 * cos(us_angle)
	new_y = self.y + 2 * sin(us_angle)
	self.coord_two = [new_x, new_y]
	self.angle_line = (self.coord_one, self.coord_two)
	
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

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise = float(new_t_noise);
        self.sense_noise = float(new_s_noise);

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
		dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            	dist += random.gauss(0.0, self.sense_noise)
            	Z.append(dist)
        return Z
         
    def virtual_scan():
	us_scan_readings = []
	# enable_servo() to be done here for actual robot
	# Iterating through the angles
	for i in range(0,180,20):
	    # servo(i) for actual robot
	    min_dist = float("inf")
	    for j in range(len(lines)):
		# finding intersection points and only storing the least
		intersection_point = lines[j].find_intersection_with_line(self.angle_line)
		if intersection_point:    
		    dist = sqrt((self.x - intersection_point[0]) ** 2 + (self.y - intersection_point[1]) ** 2) 
		    min_dist = min(min_dist, dist)
	    us_scan_readings.append(min_dist)
	return us_scan_readings

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_x # cyclic truncate
        y %= world_y
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
            
    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        prob = 1.0;
                
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
 
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

class Line:

    def __init__(self):
	# coord_one and coord_two are two points 
	# for the line of obstacles
	self.coord_one = [0.0, 0.0]
	self.coord_two = [0.0, 0.0]
    
    def find_intersection_with_line(line2):
	# Method to find intersection between two lines
	line1 = (self.coord_one, self.coord_two)
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])        
	div = det(xdiff, ydiff)
	if div == 0:
            raise Exception('lines do not intersect')
    	d = (det(*line1), det(*line2))
    	x = det(d, xdiff) / div
    	y = det(d, ydiff) / div

	# Checking if the intersection point is within the range. line2 is the line made by the robot sensor. 
	if x >= line2[0][0] and x <= line2[1][0] and y >= line2[0][1] and y <= line21[1][1]:
	    return x, y
    	else:
	    return None

    def set_equation(self, x1, y1, x2, y2):
	self.coord_one = [x1, y1]
	self.coord_two = [x2, y2]
	
    def det(self, a, b):
	return a[0] * b[1] - a[1] * b[0]
    
    def get_line(self):
	return (self.coord_one, self.coord_two)

def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_x/2.0)) % world_x - (world_x/2.0)
        dy = (p[i].y - r.y + (world_y/2.0)) % world_y - (world_y/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def initialize():
    print 'in initialize'
# --------

N = 1000
T = 50
myrobot = robot()
initialize_world()


p = []
for i in range(N):
    r = robot()
    r.set_noise(0.05, 0.05, 5.0) # provided noise.
    p.append(r)
    
print 'Mean error at start', eval(myrobot, p)
# show particle's initial locations
print p    

for t in range(T):
#    print p
    myrobot= myrobot.move(0.1, 5.0)
    Z = myrobot.sense()
    
    p2 = []

    for i in range(N):
        p2.append(p[i].move(0.1, 5.0))
    p = p2
    
    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(Z))
    p3 = []

# this is importance sampling code

    index = int(random.random() * N)
    beta = 0.0
    mw = max(w)
    for i in range(N):
        beta += random.random() * 2.0 * mw
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1) % N
        p3.append(p[index])
    p = p3
    
    print 'Mean error',eval(myrobot, p)
    
print ' '
if eval(myrobot, p) > 0.0:
    for i in range(N/100):        
        print 'Final particle #', i*100, p[i*100]
    print ' '
    print 'Actual Robot Location', myrobot
