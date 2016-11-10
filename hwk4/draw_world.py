import math
import turtle
import random
from turtle import *

OBSTACLE_LINE_COLOR = "red"
OBSTACLE_FILL_COLOR = "red"
ORIGIN = (0,0)
turtle.tracer(50000, delay=0)
turtle.register_shape("dot", ((-3,-3), (-3,3), (3,3), (3,-3)))
turtle.register_shape("particle", ((-3, -2), (0, 3), (3, -2), (0, 0)))
turtle.speed(0)

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

        x, y = start
        turtle.goto(x,y)

        # Use this to draw things on the screen
        turtle.pendown()
        turtle.begin_fill()

        for point in points:
            dx, dy = point
            turtle.goto(dx, dy)
            print "Point gone to"
            print turtle.position()
        turtle.goto(x, y)  # connect them to start to form a closed shape
        
        # Set this back when drawing done
        turtle.penup()
        turtle.end_fill()

    def draw(self):
        self.drawShapes(self.origin, self.boundaries)
        for obstacle in self.obstacles:
            self.drawShapes(self.obstacles[0], obstacle, OBSTACLE_LINE_COLOR, OBSTACLE_FILL_COLOR)
        turtle.update()
        exitonclick()

    def show_mean(self, mean_x, mean_y, is_evaluated):
        if is_evaluated:
            turtle.color("gray")
        else:
            turtle.color("green")
        turtle.setposition(mean_x, mean_y)
        turtle.shape("circle")
        turtle.stamp()

    def showParticles(self, particles, is_evaluated):
        turtle.clearstamps()
        turtle.color("blue")
        turtle.shape("particle")

        for particle in particle:
            turtle.setposition(particle.x, particle.y)
            turtle.setheading(90 - particle.orientation) # Need to confirm angle adjustment based on values in the main file
            # turtle.color(self.weight_to_color(particle.weight)) # need to check this with the original file
            turtle.stamp()
            sum_x += particle.x
            sum_y += particle.y

        mean_x = sum_x/float(len(particle))
        mean_y = sum_y/float(len(particle))

        self.show_mean(mean_x, mean_y, is_evaluated)

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition(robot.x, robot.y)
        turtle.setheading(90 - robot.orientation)
        turtle.stamp()
        turtle.update()

