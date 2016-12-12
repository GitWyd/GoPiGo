import random
from math import sqrt, atan2, cos, sin

class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    # returns True if a is strictly left of b
    # returns false otherwise
    def is_strictly_left(self, b, c):
        a = self
        det = (a.x-c.x) * (b.y-c.y) - (b.x-c.x) * (a.y-c.y)
        return det<0
    def ccw(self,b,c):
        a = self
        return (c.y-a.y)*(b.x-a.x) > (b.y-a.y) * (c.x-a.x)        
    # returns true if a point A is left of point B
    # in Clockwise ordering around the center
    def is_left_CW(self, pt, center):
        a = self
        b = pt
        c = center
        # if det=0, then points are on the same line
        # if det>0, then a is right of b
        # if det<0, then a is left of b
        det = (a.x-c.x) * (b.y-c.y) - (b.x-c.x) * (a.y-c.y)
        if det < 0:
            return True
        if det > 0:
            return False
        # for points that lie on same line, tiebrake by choosing the one closer to the center
        dist1 = a.dist_to(c) #(a.x-c.x)**2 + (a.y-c.y)**2
        dist2 = b.dist_to(c) #(b.x-c.x)**2 + (b.y-c.y)**2
 #       if (a.x == b.x):
 #          return dist1 > dist2
 #       elif (a.y == b.y):
 #           return dist1 < dist2
        return dist1 > dist2
    def random(self, x_scalar, y_scalar, bias, bias_p):
        rnd_x = random.random() 
        rnd_y = random.random() 
        x_value = (1-bias_p)*(rnd_x * x_scalar) + bias_p*(rnd_x * bias[0])
        y_value = (1-bias_p)*(rnd_y * y_scalar) + bias_p*(rnd_y * bias[1])
        self = Point(x_value, y_value)
        return self 
    def __radd__(self, other):
        return Point(self.x+other.x,self.y+other.y)
    def __eq__(self, other): 
        return self.x == other.x and self.y == self.y
    def __hash__(self):
        return hash(id(self))
    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y  
    def set_x_y(self, x, y):
        self.x = x 
        self.y = y
        return self
    def reflect_x(self):
        self.set_y(self.y * -1)
        return self
    def reflect_y(self):
        self.set_x(self.x * -1)
        return self
    def get_angle_to(self, other):
        return atan2(self.y - other.y, self.x - other.x)
    # get point distance away from self in direction theta
    def get_pt_in_direction(self, theta, distance):
        return Point(self.x + distance * cos(theta), self.y + distance * sin(theta))
    def to_tuple(self):
        return (self.x,self.y)
    def dist_to(self,other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    # def __eq__(self, other):
    #     return self.__dict__ == other.__dict__
    def tolerant_equal(self, other, threshold):
        return True if self.dist_to(other)<threshold else False
        #value = b if a > 10 else c
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):        
        return '\n\t[x=%.6s y=%.6s]' % (str(self.x), str(self.y))
