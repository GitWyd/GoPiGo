from Queue import *
from collections import defaultdict
from draw_world import *
from turtle import *

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
                        self.edges.get(self.start).append(Line(self.start,vertex)) 
                    else:
                        self.edges[self.start] = [Line(self.start,vertex)]
                if self.is_visible(self.end, vertex, polygons):
                    if self.edges.get(self.end):
                        print "Edges"
                        print self.edges.get(self.end)
                        print type(self.edges.get(self.end))
                        self.edges.get(self.end).append(Line(self.end,vertex))
                    else:
                        self.edges[self.end] = [Line(self.end,vertex)]
                obstacle_temp = self.obstacles[:i] + self.obstacles[i+1:]
                for other_obstacle in obstacle_temp:
                    for other_vertex in other_obstacle.hull_vertices:
                        if self.is_visible(vertex, other_vertex, polygons):
                            if self.edges.get(vertex):
                                self.edges.get(vertex).append(Line(vertex, other_vertex))
                            else:
                                self.edges[vertex] = [Line(vertex, other_vertex)]
        maze = Maze(240, 420, self.obstacles)
        maze.draw()
        maze.show_robot()
        exitonclick()

    # Check for point visibility
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

    def manhattan(coord1, coord2):
        return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)

    def l2(coord1, coord2):
        return sqrt( (coord1.x - coord2.x) ** 2 + (coord1.y - coord2.y) ** 2 )

    def dijkstra_search(graph, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.l2(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current
        
        return came_from, cost_so_far

    def a_star_search(graph, start, goal):
        frontier = Queue.PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.l2(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + l2(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        return came_from, cost_so_far

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
    


