import math
import turtle
import random
from turtle import *
import numpy as np

OBSTACLE_LINE_COLOR = "red"
OBSTACLE_FILL_COLOR = "red"
ORIGIN = (0,0)
scale=3
offsetx= -scale/2*100
offsety= -scale/2*100

class Maze(object):
    def __init__(self, world_x, world_y, obstacles):
        self.world_x = world_x
        self.world_y = world_y
        self.obstacles = obstacles
        self.origin = ORIGIN

        self.boundaries = [self.origin,(self.world_x,0),(self.world_x, self.world_y),(0, self.world_y)]

    def drawShapes(self, start, points, lineColour="blue", fillColour="white"):
        turtle.penup()
        turtle.pencolor(lineColour)
        turtle.fillcolor(fillColour)
        print start
        x, y = start
        turtle.goto(offsetx + scale * x,offsety + scale * y)

        # Use this to draw things on the screen
        turtle.pendown()
        turtle.begin_fill()
        print "Points"
        print points
        for points in points:
            dx, dy = points
            turtle.goto(offsetx + scale * dx, offsety + scale * dy)
            print "Point gone to"
            print turtle.position()
        turtle.goto(offsetx + scale * x, offsety + scale * y)  # connect them to start to form a closed shape
        
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
            self.drawShapes(obstacle[0], obstacle, OBSTACLE_LINE_COLOR, OBSTACLE_FILL_COLOR)
        turtle.home()
        turtle.update()

    def show_mean(self, mean_x, mean_y, mean_orient, is_evaluated):
        if is_evaluated:
            turtle.color("green")
        else:
            turtle.color("gray")
        turtle.setposition(offsetx + scale * mean_x, offsety + scale * mean_y)
        turtle.setheading(np.rad2deg(mean_orient)) 
        turtle.shape("turtle")
        turtle.stamp()

    def weight_to_color(self, weight):
        return "#%02x00%02x" % (int(weight * 255) , int((1 - weight) * 255))

    def show_particles(self, particles, weights, is_evaluated):
        turtle.clearstamps()
        turtle.color("blue")
        turtle.shape("particle")
        sum_wx = 0
        sum_wy = 0
        mean_x = 0 
        mean_y = 0
        sum_w_orient = 0
        count = 0
        sumw = sum(weights)
        # for particle in particles: 
        #     sum_x += particle.x
        #     sum_y += particle.y
        #     sum_orient += particle.orientation

        for i in range(0,len(particles), 10):
            turtle.setposition(offsetx + scale * particles[i].x, offsety + scale * particles[i].y)
            turtle.setheading(np.rad2deg(particles[i].orientation)) 
            turtle.color(self.weight_to_color(weights[i])) 
            turtle.stamp()
        if not sumw:
            for i in range(len(weights)):
            	weights[i] = 1/float(len(weights))
        sumw = sum(weights)
        for i in range(0,len(particles), 10): 
        	sum_wx += particles[i].x * weights[i]
        	sum_wy += particles[i].y * weights[i]
        	sum_w_orient += particles[i].orientation * weights[i]

        mean_x = sum_wx/sumw
        mean_y = sum_wy/sumw
        mean_orient = sum_w_orient/sumw

        self.show_mean(mean_x, mean_y, mean_orient, is_evaluated)
        turtle.update()

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition(offsetx + scale * robot.x, offsety + scale * robot.y)
        turtle.setheading(np.rad2deg(robot.orientation))
        turtle.stamp()
        turtle.update()

