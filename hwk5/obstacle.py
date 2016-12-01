from visibility_graph import *
from follow_path import *
from point import Point
import math
import sys

ROBOT_SIZE = 23
ROBOT_START_ORIENTATION = 90
obstacle_list = []
world_x = 0.0
world_y = 0.0
goal_x = 0.0
goal_y = 0.0
robot = None

class Obstacle:
        def __init__(self, vertices = None):
                self.vertices = []
                self.hull_vertices = []
                # add vetcies from list of tuples
                if vertices:
                        for pt in vertices:
                                self.vertices.append(Point(pt[0],pt[1]))
                self.center = None
                self.convex_hull = None

        def add_vertex(self, x, y):
                pt = Point(x,y)
                self.vertices.append(pt)
                self.center = self._find_centroid()

        def _find_centroid(self):
                tot_x = sum(pt.x for pt in self.vertices)
                tot_y = sum(pt.y for pt in self.vertices)
                n = len(self.vertices)
                return Point(tot_x/n, tot_y/n)

        def _order_vertices_CW(self, P0):
        # bubble sort algorithm ()
                vertices_list = self.hull_vertices 
                for passnr in range(len(vertices_list)-1,0,-1):
                        for i in range(passnr):
                                if vertices_list[i].is_left_CW(vertices_list[i+1], P0):
                                        self._swap_elements(vertices_list, i, i+1)
                self.hull_vertices = vertices_list         

        # returns the list index of the point with the lowest y coordinate 
        def _get_lowest_y_coordinate(self):
                lowest_y_idx = 0
                vertices_list = self.hull_vertices
                for i in range(len(vertices_list)):
                        if vertices_list[i].y < vertices_list[lowest_y_idx].y:
                                lowest_y_idx = i
                        elif vertices_list[i].y == vertices_list[lowest_y_idx].y:
                                if vertices_list[i].x > vertices_list[lowest_y_idx].x:
                                        lowest_y_idx = i
                coord = vertices_list[lowest_y_idx]
                self.hull_vertices = vertices_list
                return coord 

        # swaps two elements in a list, and assumes 
        def _swap_elements(self, vertices_list, i, j):
                if not vertices_list:
                        vertices_list = self.hull_vertices
                temp = vertices_list[i]
                vertices_list[i] = vertices_list[j]
                vertices_list[j] = temp

        def grow_obstacles(self):
                global robot
                self.hull_vertices.extend(self.vertices)
                for vertex in self.vertices:
                        hull_vertices = robot.translate_to_vertex(vertex)
                        self.hull_vertices.extend(hull_vertices)
                self.hull_vertices = list(set(self.hull_vertices))

        def compute_convex_hull(self):
                P0 = self._get_lowest_y_coordinate()
                self._order_vertices_CW(P0)
                N = len(self.hull_vertices)
                Pn1 = self.hull_vertices[N - 1]
                vertices_list = self.hull_vertices
                stack = [Pn1, P0]
                i = 1 
                while i < N:
                        top = stack[len(stack) - 1]
                        second = stack[len(stack) - 2]
                        if vertices_list[i].is_strictly_left(top, second):
                            stack.append(vertices_list[i])
                            i+=1
                        else:
                            stack.pop()
                
                stack.pop()
                print 'convex hull vertices'
                self.hull_vertices = stack
                print self.hull_vertices
                
        def __eq__(self, other): 
                return self.vertices == other.vertices

        def __hash__(self):
                return hash(id(self))
                
class Robot:
    def __init__(self, x, y):
        self.robot_x = x
        self.robot_y = y
        # translate reference point
        # 
        self.reference_x = x 
        self.reference_y = y
        self.length = 23
        self.width = 23
        self.theta = 90
        # corner points of robot
        self.a = Point(self.reference_x - 12, self.reference_y + 12)
        self.b = Point(self.reference_x + 12, self.reference_y + 12)
        self.c = Point(self.reference_x - 12 , self.reference_y - 12)
        self.d = Point(self.reference_x + 12, self.reference_y - 12)
    # pick up robot and bring it to the origiin
    def translate_to_origin(self):
        origin_x = self.a.x
        origin_y = self.a.y
        # set robot upper left corner to [0,0]
        self.a.set_x_y(self.a.x - origin_x, self.a.y - origin_y)  
        self.b.set_x_y(self.b.x - origin_x, self.b.y - origin_y)  
        self.c.set_x_y(self.c.x - origin_x, self.c.y - origin_y)  
        self.d.set_x_y(self.d.x - origin_x, self.d.y - origin_y)  
        
    def reflect_along_x(self):
        self.a = self.a.reflect_x()
        self.b = self.b.reflect_x()
        self.c = self.c.reflect_x()
        self.d = self.d.reflect_x()
    
    def reflect_along_y(self):
        self.a = self.a.reflect_y()
        self.b = self.b.reflect_y()
        self.c = self.c.reflect_y()
        self.d = self.d.reflect_y()
        
    def get_corners(self):
        return [self.a, self.b, self.c, self.d]

    def translate_to_vertex(self, vertex):
        vertex_x = vertex.x
        vertex_y = vertex.y
        a = Point(self.a.x + vertex_x, self.a.y + vertex_y)
        b = Point(self.b.x + vertex_x, self.b.y + vertex_y)
        c = Point(self.c.x + vertex_x, self.c.y + vertex_y)
        d = Point(self.d.x + vertex_x, self.d.y + vertex_y)
        return [a, b, c, d] 

def initialize_world():
    global obstacles
    filename = str(sys.argv[1])
    obstacles = [obstacle.rstrip('\n') for obstacle in open(filename)]
    global world_x
    global world_y
    global goal_x
    global goal_y
    global start_x
    global start_y
    global obstacle_list
    global robot
    
    # initialize start position
    start_x = float(obstacles[0].split()[0])
    start_y = float(obstacles[0].split()[1])
    # initialize robot at start position
    robot = Robot(start_x, start_y)
    # initialize goal position
    goal_x = float(obstacles[1].split()[0])
    goal_y = float(obstacles[1].split()[1])
    # world dimensions
    world_x = float(obstacles[2].split()[0])
    world_y = float(obstacles[2].split()[1])
    num_obstacles = int(obstacles[3].split()[0])
    counter = 4 # index for list of points
    for i in range(0, num_obstacles, 1):
        num_vertices = int(obstacles[counter].split()[0])
        obstacle = Obstacle()
        for j in range(1, num_vertices + 1, 1):
            obstacle_x = float(obstacles[counter+j].split()[0])
            obstacle_y = float(obstacles[counter+j].split()[1])
            obstacle.add_vertex(obstacle_x, obstacle_y)
        counter += num_vertices + 1
        obstacle_list.append(obstacle)

def grow_obstacles():
    counter = 1
    robot.translate_to_origin()
    print 'robot origin'
    print str(robot.get_corners())
    robot.reflect_along_x()
    robot.reflect_along_y()
    for obstacle in obstacle_list:
        print 'obstacle ' + str(counter)
        obstacle.grow_obstacles()
        obstacle.compute_convex_hull()
        counter += 1

if __name__ == '__main__':
    initialize_world()
    grow_obstacles()
    g = Graph(obstacle_list, Point(robot.robot_x, robot.robot_y), Point(goal_x, goal_y), robot)
    g.make_edges()
    follow_path(g.path, Point(robot.robot_x, robot.robot_y), ROBOT_START_ORIENTATION)

