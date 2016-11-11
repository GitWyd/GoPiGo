import math
import turtle
import random
from turtle import *
import numpy as np

OBSTACLE_LINE_COLOR = "red"
OBSTACLE_FILL_COLOR = "red"
ORIGIN = (0,0)


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
        turtle.goto(x,y)

        # Use this to draw things on the screen
        turtle.pendown()
        turtle.begin_fill()
        print "Points"
        print points
        for points in points:
            dx, dy = points
            turtle.goto(dx, dy)
            print "Point gone to"
            print turtle.position()
        turtle.goto(x, y)  # connect them to start to form a closed shape
        
        # Set this back when drawing done
        turtle.penup()
        turtle.end_fill()
        turtle.update()

    def draw(self):
    	turtle.tracer(80000, delay=0) 
        turtle.register_shape("dot", ((-1,-1), (-1,1), (1,1), (1,-1)))
        turtle.register_shape("particle", ((-3, -2), (0, 3), (3, -2), (0, 0)))
        turtle.speed(0)
        
        self.drawShapes(self.origin, self.boundaries)
        for obstacle in self.obstacles:
            self.drawShapes(obstacle[0], obstacle, OBSTACLE_LINE_COLOR, OBSTACLE_FILL_COLOR)
        turtle.home()
        turtle.update()

    def show_mean(self, mean_x, mean_y, is_evaluated):
        if is_evaluated:
            turtle.color("green")
        else:
            turtle.color("gray")
        turtle.setposition(mean_x, mean_y)
        turtle.shape("circle")
        turtle.stamp()

    def show_particles(self, particles, is_evaluated):
        turtle.clearstamps()
        turtle.color("blue")
        turtle.shape("particle")
        sum_x = 0
        sum_y = 0
        mean_x = 0 
        mean_y = 0
        count = 0
        for particle in particles:
        	sum_x += particle.x
        	sum_y += particle.y
        for i in range(0,len(particles), 10):
            turtle.setposition(particles[i].x, particles[i].y)
            turtle.setheading(np.rad2deg(particles[i].orientation)) # Need to confirm angle adjustment based on values in the main file
            # turtle.color(self.weight_to_color(particle.weight)) # need to check this with the original file
            turtle.stamp()

        mean_x = sum_x/float(len(particles))
        mean_y = sum_y/float(len(particles))

        self.show_mean(mean_x, mean_y, is_evaluated)
        turtle.update()

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition(robot.x, robot.y)
        turtle.setheading(np.rad2deg(robot.orientation))
        turtle.stamp()
        turtle.update()

