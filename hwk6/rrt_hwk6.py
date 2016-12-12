import sys, random, math
from math import sqrt,cos,sin,atan2
from point import Point
from draw_world import *
from turtle import *
#global variables
BIAS = 0
MATCH_TOLERANCE = 0.5
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
class Node:
    def __init__(self, pt, parent):
        self.pt = pt
        self.parent = parent
    def get_parent(self):
        return self.parent
    def set_parent(self, parent):
        self.parent = parent
    def dist(self, other):
        return self.pt.dist_to(other.pt)
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        #return self.pt.tolerant_equal(other.pt) 
    def tolerant_equal(self, other, threshold):
        return self.pt.tolerant_equal(other.pt, threshold)
    def __repr__(self):
        return str(self.pt)
    # return path
    def get_path(self,path):
        path.append(self)
        if (self.get_parent()):
            return self.get_parent().get_path(path)
        return path
    def whose_my_daddy(nodes):
        child = nodes[0]
        parent = Null
        for i in range(1,len(nodes)):
            parent = nodes[i]
            child.set_parent(parent)
            child = parent
        # set parent of last node to None
        child = None


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
# takes in two points
# Check for point visibilitys
def is_visible(start_vertex, end_vertex):
    start_vertex = start_vertex.to_tuple()
    end_vertex = end_vertex.to_tuple()
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
    # add the bounderies around world
    ## bottom border
    obstacle = Obstacle()
    obstacle.add_vertex(0,0)
    obstacle.add_vertex(world_x,0)
    obstacle.add_vertex(world_x,-1)
    obstacle.add_vertex(0,-1)
    obstacle.make_boundaries()
    obstacles.append(obstacle)
    ## top border
    obstacle = Obstacle()
    obstacle.add_vertex(0,world_y)
    obstacle.add_vertex(world_x,world_y)
    obstacle.add_vertex(world_x,world_y+1)
    obstacle.add_vertex(0,world_y+1)
    obstacle.make_boundaries()
    obstacles.append(obstacle)
    # right border
    obstacle = Obstacle()
    obstacle.add_vertex(world_x,world_y)
    obstacle.add_vertex(world_x+1,world_y)
    obstacle.add_vertex(world_x+1,0)
    obstacle.add_vertex(world_x,0)
    obstacle.make_boundaries()
    obstacles.append(obstacle)
    # left border
    obstacle = Obstacle()
    obstacle.add_vertex(0,world_y)
    obstacle.add_vertex(-1,world_y)
    obstacle.add_vertex(-1,0)
    obstacle.add_vertex(0,0)
    obstacle.make_boundaries()
    obstacles.append(obstacle)
# def dist(p1, p2):
#     return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 

# def det(a, b):
#     return a[0] * b[1] - a[1] * b[0]

# converts a path of nodes into points
def nodes_2_points(list):
    tmp = []
    for i in list:
        tmp.append(i.pt)
    return tmp
# takes two points as arguments and return the next Node to grow towards
def grow_from_towards(closest_node, rnd_node, distance):
    if closest_node.dist(rnd_node) < distance:
        return rnd_node
    else:
        theta = closest_node.pt.get_angle_to(rnd_node.pt)
        tmp_pt = closest_node.pt.get_pt_in_direction(theta, distance)
        return Node(tmp_pt, None)

# a list of nodes and a reference node as input arguments
# returns the closest Node to the reference Node from the list
def find_closest_node(nodes, rnd_node):
    closest_pt = nodes[0]
    for node in nodes:
        #if dist(node, random_pt) < dist(closest_pt, random_pt):
        if node.dist(rnd_node) < closest_pt.dist(rnd_node):
            closest_pt = node
    return closest_pt

def rrt(distance, forward, maze):
    nodes = []
    color = None
    if forward:
        nodes.append(Node(Point(start[0], start[1]),None))
        color = "green"
    else:
        nodes.append(Node(Point(goal[0], goal[1]),None))
        color = "red"

    for i in range(max_nodes):
        #random_pt = Point(random.random() * world_x, random.random() * world_y)
        #rnd_node = Node(random_pt, None)
        rnd_node = None

        # rnd_node with bias towards goal or start
        if forward:
            rnd_node = Node(Point().random(world_x, world_y, goal, BIAS), None)
        else:
            rnd_node = Node(Point().random(world_x, world_y, start, BIAS), None)
        closest_node = find_closest_node(nodes, rnd_node)
        next_node = grow_from_towards(closest_node, rnd_node, distance)

        #print 'adding this node now ' + str(next_node.pt)
        if is_visible(closest_node.pt, next_node.pt):
            #print(Point(random.random() * world_x, random.random() * world_y))
            #print 'adding this node now ' + str(next_node.pt.x) +','+ str(next_node.pt.y)
            maze.drawLine(closest_node.pt.to_tuple(), next_node.pt.to_tuple(), color)
            # set parent node for trace back
            next_node.set_parent(closest_node)
            nodes.append(next_node)
    return nodes

def merge_rrts(forward_nodes, reverse_nodes):
    for i in range(max_retries):
        #random_pt = Point(random.random() * world_x, random.random() * world_y)
        # find next forward Node
        rnd_node = Node(Point().random(world_x, world_y, goal, BIAS), None)
        #rnd_node = Node(random_pt, None)
        closest_forward_node = find_closest_node(forward_nodes, rnd_node) 
        next_forward_node = grow_from_towards(closest_forward_node, rnd_node, distance)
        if not is_visible(closest_forward_node.pt, next_forward_node.pt):
            continue # if the node is not visible try again
        # find next reverse Node
        closest_reverse_node = find_closest_node(reverse_nodes, next_forward_node)
        next_reverse_node = grow_from_towards(closest_reverse_node, next_forward_node, distance)
        if not is_visible(closest_reverse_node.pt, next_reverse_node.pt):
            continue # if the node is not visible try again

        if next_reverse_node.tolerant_equal(next_forward_node, MATCH_TOLERANCE):
            next_forward_node.set_parent(closest_forward_node)

            # get forward path start to connection node
            forward_nodes.append(next_forward_node)
            fwd_path = next_forward_node.get_path([])
            fwd_path.whose_my_daddy()
            fwd_path = fwd_path.reverse()
            # get reverse path closest_reverse_node to goal
            rev_path = closest_reverse_node.get_path([])
            # join paths
            fwd_path[-1].set_parent=rev_path[0]
            path = fwd_path + rev_path
            return nodes_2_points(path)
        temp = forward_nodes
        forward_nodes = reverse_nodes
        reverse_nodes = temp

if __name__ == '__main__':
    distance = float(sys.argv[1])
    initialize_world()

    maze = Maze(world_x, world_y, obstacles)
    maze.draw()
    maze.drawPoints(start, goal)
    time.sleep(0.5)

    forward_nodes = rrt(distance, True, maze)
    reverse_nodes = rrt(distance, False, maze)

    path = merge_rrts(forward_nodes, reverse_nodes)

    maze.drawResult(path[0], path)

    exitonclick()

