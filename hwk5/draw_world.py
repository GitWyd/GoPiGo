import math
import turtle
import random
from turtle import *
import numpy as np
from obstacle import Point

OBSTACLE_LINE_COLOR = "red"
OBSTACLE_FILL_COLOR = "red"
ORIGIN = Point(0,0)
scale=3
offsetx= -scale/2*100
offsety= -scale/2*100

class Maze(object):
    def __init__(self, world_x, world_y, obstacles):
        self.world_x = world_x
        self.world_y = world_y
        self.obstacles = obstacles
        self.origin = ORIGIN

        self.boundaries = [self.origin,Point(self.world_x,0),Point(self.world_x, self.world_y),Point(0, self.world_y)]

    def drawShapes(self, start, points, lineColour="blue", fillColour="white"):
        turtle.penup()
        turtle.pencolor(lineColour)
        turtle.fillcolor(fillColour)
        print start
        x = start.x
        y = start.y
        turtle.goto(x, y)

        # Use this to draw things on the screen
        turtle.pendown()
        turtle.begin_fill()
        print "Points"
        print points
        for point in points:
            dx = point.x
            dy = point.y
            turtle.goto( dx,  dy)
            print "Point gone to"
            print turtle.position()
        turtle.goto( x,  y)  # connect them to start to form a closed shape
        
        # Set this back when drawing done
        turtle.penup()
        turtle.end_fill()
        turtle.update()

    def draw(self):
    	turtle.tracer(50000, delay=0) 
        turtle.register_shape("dot", ((-1,-1), (-1,1), (1,1), (1,-1)))
        turtle.register_shape("particle", ((-3, -2), (0, 3), (3, -2), (0, 0)))
        turtle.speed(0)
        
        self.drawShapes(self.origin, self.boundaries)
        for obstacle in self.obstacles:
            self.drawShapes(obstacle.hull_vertices[0], obstacle.hull_vertices, OBSTACLE_LINE_COLOR, OBSTACLE_FILL_COLOR)
        turtle.home()
        turtle.update()

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition( robot.x,  robot.y)
        turtle.setheading(np.rad2deg(robot.orientation))
        turtle.stamp()
        turtle.update()