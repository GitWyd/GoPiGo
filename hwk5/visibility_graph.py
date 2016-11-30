
class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
  
    def neighbors(self, id):
        return self.edges[id]

    # Method to make edges for the graph:
    # start_vertex to all obstacle hulls
    # end_vertex to all obstacle hulls
    # each vertex of every obstacel hull to other vertices of other obstacle hulls
    def make_edges(self, start, end, obstacles):
    	polygons = []
    	for obstacle in obstacles:
    		polygon = Hull_Polygon()
    		polygon.make_hull_polygon(obstacle.hull_vertices)
    		polygons.append(polygon)
		
		for i in range(0,obstacles):
			for vertex in obstacle[i].hull_vertices:
	    		if is_visible(start, vertex, polygons):
	    			edges[start] = edges.get(start).append(Line(end,vertex))
	    		if is_visible(end, vertex, polygons):
	    			edges[end] = edges.get(end).append(Line(end,vertex))

	    		obstacle_temp = obstacle[:i] + obstacle[i+1:]
	    		for other_obstacle in obstacle_temp:
	    			for other_vertex in other_obstacle:
	    				if is_visible(vertex, other_vertex, polygons):
	    					edges[vertex] = edges.get(vertex).append(Line(vertex, other_vertex)) 

    # Check for point visibility
    def is_visible(self, start_vertex, end_vertex, hull_polygons):
    	temp_line = Line(start_vertex, end_vertex)
    	for polygon in hull_polygons:
    		for edge in polygon:
    			if find_intersection(temp_line, edge):
    				return False
    			else:
    				return True


class Line:
    def __init__(self, point_one, point_two):
        # coord_one and coord_two are two points 
        # for the line of obstacles
        self.coord_one = point_one
        self.coord_two = point_two

    # need to change this for bounding intersections to points inside each edge

    def find_intersection(line1, line2):
        # Method to find intersection between two lines
        # line1 = (self.coord_one, self.coord_two)
        xdiff = (line1[0].x - line1[1].x, line2[0].x - line2[1].x)
        ydiff = (line1[0].y - line1[1].y, line2[0].y - line2[1].y)        
        div = det(xdiff, ydiff)
        if div == 0:
            print 'div 0'
            return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        # Checking if the intersection point is within the range. line2 is the line made by the robot sensor. 
        if (((x > line1[0][0] and x < line1[1][0]) or (x < line1[0][0] and x > line1[1][0])) \
            and ((y > line1[0][1] and y < line1[1][1]) or (y < line1[0][1] and y > line1[1][1]))):
            return True
        else:
            return False
    
    def get_line(self):
        return (self.coord_one, self.coord_two)
    
def det(a, b):
    return a[0] * b[1] - a[1] * b[0]
    

class Hull_Polygon:
	def __init__(self):
		self.polygon = []

	def make_hull_polygon(self,hull_vertices):
		for i in range(0,len(hull_vertices) - 1):
			self.polygon.append(Line(hull_vertices[i],hull_vertices[i+1]))
		self.polygon.append(Line(hull_vertices[-1],hull_vertices[0]))
