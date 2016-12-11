import sys, random, math
from math import sqrt,cos,sin,atan2
from point import Point

#global variables
world_x = 600
world_y = 600
obstalces = []
start = ()
goal = ()
obstacles = []
obstacles_filename = 'obstacles.txt'
coordinates_filename = 'coordinates.txt'
max_nodes = 5000
max_retries = 500

class Line:
    def __init__(self, point_one, point_two):
        # coord_one and coord_two are two points
        # for the line of obstacles
        self.coord_one = point_one
        self.coord_two = point_two

    def find_intersection(self, line2):

        return self.coord_one.ccw(line2.coord_one,line2.coord_two)!=self.coord_two.ccw(line2.coord_one, line2.coord_two) \
               and self.coord_one.ccw(self.coord_two,line2.coord_one)!=self.coord_one.ccw(self.coord_two, line2.coord_two)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.coord_one) ^ hash(self.coord_two)

    def get_line(self):
        return (self.coord_one, self.coord_two)

    def __repr__(self):
        return '[Coord_one=%s \n\t Coord_two=%s]\n' % (str(self.coord_one), str(self.coord_two))

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

class Obstacle:
    def __init__(self):
	self.vertices = []
        self.boundaries = []
	
    def add_vertex(self, x, y):
	pt = Point(x, y)
	self.vertices.append(pt)	

    def make_boundaries(self):
        vertices = self.vertices
        for i in range(0,len(vertices) - 1):
            self.boundaries.append(Line(vertices[i],vertices[i+1]))
        self.boundaries.append(Line(vertices[-1],vertices[0]))

    def __repr__(self):
        parts = []
        for line in self.vertices:
            parts.append(line)
        return str(parts)

# Check for point visibilitys
def is_visible(start_vertex, end_vertex):
    temp_line_one = Line(Point(start_vertex[0], start_vertex[1]), Point(end_vertex[0], end_vertex[1]))
    temp_line_two = Line(Point(end_vertex[0], end_vertex[1]), Point(start_vertex[0], start_vertex[1]))

    for obstacle in obstacles:
        for edge in obstacle.boundaries:
               if temp_line_one.find_intersection(edge) or temp_line_two.find_intersection(edge):
                   return False
    return True

def initialize_world():
    #initializes the world based on the file provided
    global obstacles
    obstacle_txt = [obstacle.rstrip('\n') for obstacle in open(obstacles_filename)]
    coordinates = [coordinate.rstrip('\n') for coordinate in open(coordinates_filename)]
    global goal
    global start

    # initialize start position
    start_x = float(coordinates[0].split()[0])
    start_y = float(coordinates[0].split()[1])
    start = (start_x, start_y)
    # initialize goal position
    goal_x = float(coordinates[1].split()[0])
    goal_y = float(coordinates[1].split()[1])
    goal = (goal_x, goal_y)
    #  
    num_obstacles = int(obstacle_txt[0].split()[0])
    counter = 1 # index for list of points
    for i in range(0, num_obstacles, 1):
        num_vertices = int(obstacle_txt[counter].split()[0])
        obstacle = Obstacle()
        for j in range(1, num_vertices + 1, 1):
            obstacle_x = float(obstacle_txt[counter+j].split()[0])
            obstacle_y = float(obstacle_txt[counter+j].split()[1])
            obstacle.add_vertex(obstacle_x, obstacle_y)
        counter += num_vertices + 1
        obstacle.make_boundaries()
        obstacles.append(obstacle)

def dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 

def grow_from_towards(closest_node, random_pt, distance):
    if dist(closest_node, random_pt) < distance:
        return random_pt
    else:
        theta = atan2(random_pt[1] - closest_node[1], random_pt[0] - closest_node[0])
        return (closest_node[0] + distance * cos(theta), closest_node[1] + distance * sin(theta))

def find_closest_node(nodes, random_pt):
    closest_pt = nodes[0]
    for node in nodes:
        if dist(node, random_pt) < dist(closest_pt, random_pt):
            closest_pt = node
    return closest_pt

def rrt(distance, forward):
    nodes = []

    if forward:
        nodes.append((start[0], start[1]))
    else:
        nodes.append((goal[0], goal[1]))

    for i in range(max_nodes):
        random_pt = (random.random() * world_x, random.random() * world_y)
        closest_node = find_closest_node(nodes, random_pt)
        next_node = grow_from_towards(closest_node, random_pt, distance)
        if is_visible(closest_node, next_node):
            print 'adding this node now ' + str(next_node[0]) + str(next_node[1]) 
            nodes.append(next_node)
    return nodes

def merge_rrts(forward_nodes, reverse_nodes):
    for i in range(max_retries):
        random_pt = (random.random() * world_x, random.random() * world_y)
        closest_forward_node = find_closest_node(forward_nodes, random_pt)
        next_forward_node = grow_from_towards(closest_forward_node, random_pt, distance)
        closest_reverse_node = find_closest_node(reverse_nodes, next_forward_node)
        next_reverse_node = grow_from_towards(closest_reverse_node, next_forward_node, distance)
        if next_reverse_node == next_forward_node:
            forward_nodes.append(next_forward_node)
            return (forward_nodes, reverse_nodes)
        temp = forward_nodes
        forward_nodes = reverse_nodes
        reverse_nodes = temp

if __name__ == '__main__':
    distance = float(sys.argv[1])
    initialize_world()
    forward_nodes = rrt(distance, True)
    reverse_nodes = rrt(distance, False)   
    merge_rrts(forward_nodes, reverse_nodes)

