import Queue
from collections import defaultdict
from draw_world import *
from turtle import *
import sys
import time

class Hull_Polygon:
    def __init__(self):
        self.polygon = []

    def make_hull_polygon(self, hull_vertices):
        
        for i in range(0,len(hull_vertices) - 1):
            self.polygon.append(Line(hull_vertices[i],hull_vertices[i+1]))
        self.polygon.append(Line(hull_vertices[-1],hull_vertices[0]))

    def __repr__(self):  
        parts = []     
        for line in self.polygon:
            parts.append(line)
        return str(parts)

class Graph:
    def __init__(self, obstacles, start, end, robot):
        self.edges = defaultdict(list)
        self.obstacles = obstacles
        self.start = start
        self.end = end
        self.robot = robot

    def neighbors(self, id):
        return self.edges[id]

    # Method to make edges for the graph:
    # start_vertex to all obstacle hulls
    # end_vertex to all obstacle hulls
    # each vertex of every obstacel hull to other vertices of other obstacle hulls
    def make_edges(self):
        polygons = []
        for obstacle in self.obstacles:
            polygon = Hull_Polygon()
            polygon.make_hull_polygon(obstacle.hull_vertices)
            polygons.append(polygon)

        for i in range(0,len(self.obstacles)):
            for vertex in self.obstacles[i].hull_vertices:
                if self.is_visible(self.start, vertex, polygons):
                    if self.edges.get(self.start):
                        self.edges.get(self.start).append(vertex) 
                    else:
                        self.edges[self.start] = [vertex]
                if self.is_visible(vertex, self.end, polygons):
                    if self.edges.get(vertex):
                        self.edges.get(vertex).append(self.end)
                    else:
                        self.edges[vertex] = [self.end]
                obstacle_temp = self.obstacles[:i] + self.obstacles[i+1:]
                for other_obstacle in obstacle_temp:
                    for other_vertex in other_obstacle.hull_vertices:
                        if self.is_visible(vertex, other_vertex, polygons):
                            if self.edges.get(vertex):
                                self.edges.get(vertex).append(other_vertex)
                            else:
                                self.edges[vertex] = [other_vertex]

            hull_vertices_temp = self.obstacles[i].hull_vertices
            for i in range(0,len(hull_vertices_temp) - 1):
                if self.edges.get(hull_vertices_temp[i]):
                    self.edges.get(hull_vertices_temp[i]).append(hull_vertices_temp[i+1])
                else:
                    self.edges[hull_vertices_temp[i]] = [hull_vertices_temp[i+1]]
                if self.edges.get(hull_vertices_temp[i+1]):
                    self.edges.get(hull_vertices_temp[i+1]).append(hull_vertices_temp[i])
                else:
                    self.edges[hull_vertices_temp[i+1]] = [hull_vertices_temp[i]]
            self.edges[hull_vertices_temp[0]] = [hull_vertices_temp[-1]]

        maze = Maze(240, 420, self.obstacles)
        maze.draw()
        maze.show_robot(self.robot)
        time.sleep(0.5)
        for key, value in self.edges.iteritems():
            if value:
                maze.drawLines(key, value)
                time.sleep(0.5)

        for key,value in self.edges.iteritems():
            print str(key)+':\n'+str(value)
        result, cost_so_far = self.dijkstra_search()
        print "Result path and cost"
        print result
        print cost_so_far
        for key, value in self.edges.iteritems():
            if value:
                maze.drawLines(key, value, "white")
        maze.draw()
        maze.show_robot(self.robot)
        self.robot.robot_x = self.end.x
        self.robot.robot_y = self.end.y
        maze.drawResult(result[0], result, "green")
        maze.show_robot(self.robot)
        exitonclick()

    # Check for point visibilitys
    def is_visible(self, start_vertex, end_vertex, hull_polygons):
        temp_line_one = Line(start_vertex, end_vertex)
        temp_line_two = Line(end_vertex, start_vertex)

        for p in hull_polygons:
            if temp_line_one in p.polygon or temp_line_two in p.polygon:
                continue
            else:
                for edge in p.polygon:
                    if (temp_line_one.coord_two == edge.coord_one or \
                        temp_line_one.coord_two == edge.coord_two):
                        continue
                    if temp_line_one.find_intersection(edge):
                        return False
        
        return True

    def manhattan(self, coord1, coord2):
        return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)

    def l2(self, coord1, coord2):
        return sqrt( (coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2 )

    def dijkstra_search(self):
        closed_set = set()
        frontier = Queue.PriorityQueue()
        frontier.put((self.l2(self.start,self.end),self.start))
        came_from = {}
        cost_so_far = {}
        for obstacle in self.obstacles:
            for vertex in obstacle.hull_vertices:
                cost_so_far[vertex] = sys.maxsize
        cost_so_far[self.end] = sys.maxsize
        cost_so_far[self.start] = 0
        
        while not frontier.empty():
            min_f, current = frontier.get()
            
            if current == self.end:
                return (self.reconstructed_path(came_from, current), cost_so_far[current])

            if current in closed_set:
                continue
            closed_set.add(current)

            for next in self.neighbors(current):
                if next not in closed_set:

                    new_cost = cost_so_far[current] + self.l2(current, next)

                    if new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost
                        frontier.put((priority, next))
                        came_from[next] = current
        
        # return came_from, cost_so_far

    def reconstructed_path(self,came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return [p for p in reversed(path)]  

    def a_star_search(self):
        closed_set = set()
        frontier = Queue.PriorityQueue()
        frontier.put((self.l2(self.start,self.end),self.start))
        came_from = {}
        cost_so_far = {}
        for obstacle in self.obstacles:
            for vertex in obstacle.hull_vertices:
                cost_so_far[vertex] = sys.maxsize
        cost_so_far[self.end] = sys.maxsize
        cost_so_far[self.start] = 0
        
        while not frontier.empty():
            min_f, current = frontier.get()
            
            if current == self.end:
                return (self.reconstructed_path(came_from, current), cost_so_far[current])

            if current in closed_set:
                continue
            closed_set.add(current)
            print "Current"
            print current
            print "Neighbours"
            print self.neighbors(current)
            for next in self.neighbors(current):
                if next not in closed_set:

                    new_cost = cost_so_far[current] + self.l2(current, next)

                    if new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + self.l2(self.end, next)
                        frontier.put((priority, next))
                        came_from[next] = current

class Line:
    def __init__(self, point_one, point_two):
        # coord_one and coord_two are two points 
        # for the line of obstacles
        self.coord_one = point_one
        self.coord_two = point_two

    # need to change this for bounding intersections to points inside each edge

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
    


