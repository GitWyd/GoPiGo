##
# Obstacle classa
# pmw2125
##

class Obstacle:
        def __init__(self, vertices = None):
                self.vertices = []
                # add vetcies from list of tuples
                if vertices:
                        for pt in vertices:
                                self.vertices.apend(Point(pt[0],pt[1]))
                self.center = None
                self.convex_hull = None
        def add_vertex(self, x, y):
                pt = Point(x,y)
                self.vertices.append(pt)
                self._find_centroid()
        def _find_centroid():
                tot = sum(self.vertices)
                n = len(self.vertices)
                return Point(tot.x/n, tot.y/n)
        def _order_vertices_CW(self):
        # bubble sort algorithm ()
                list = self.vertices 
                for passnr in range(len(list)-1,0,-1):
                        for i in range(passnr):
                                if list[i].is_left_CW(list[i+1]):
                                        temp = list[i]
                                        list[i] = list[i+1]
                                        list[i+1] = temp
        def convex_hull(self):
                self.convex_hull = hull
class Point:
        def __init__(self, x=None, y=None):
                self.x = x
                self.y = y
        # returns true if a point A is left of point B
        # in Clockwise ordering around the cetner
        def is_left_CW(self, pt, center=self.center):
                a = self
                b = pt
                c = center
                if (a.x - c.x < 0 and b.x - c.x >= 0):
                        return false
                if (a.x - c.x >= 0 and b.x - c.x < 0):
                        return true
                if (a.x - c.x == 0 and b.x - c.x == 0):
                        if (a.y - c.y >=0 or b.y - c.y >=0):
                                return a.y > b.y
                        return b.y > a.y
                det = (a.x-c.x) * (b.y-c.y) - (b.x-c.x) * (a.y-c.y)
                if det < 0:
                        return True
                if det > 0:
                        return False
                # for points that lie on same line, tiebrake by choosing the one closer to the center
                dist1 = (a.x-c.x)**2 + (a.y-c.y)**2
                dist2 = (b.x-c.x)**2 + (b.y-c.y)**2
                return dist1 > dist2
        def __radd__(self, other):
                return Point(self.x+other.x,self.y+other.y)
        def set_x(self, x):
                self.x = x
        def set_y(self, y):
                self.y = y 
