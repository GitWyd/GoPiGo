import math
import turtle
import random
from turtle import *
import numpy as np
from point import *
import time

OBSTACLE_LINE_COLOR = "blue"
OBSTACLE_FILL_COLOR = "white"
HULL_LINE_COLOR = "black"
ORIGIN = Point(0,0)
scale=3
offset= -scale/2*150
offsety= -scale/2*100

class Maze(object):
    def __init__(self, world_x, world_y, obstacles):
        self.world_x = world_x
        self.world_y = world_y
        self.obstacles = obstacles
        self.origin = ORIGIN

        self.boundaries = [self.origin,Point(self.world_x,0),Point(self.world_x, self.world_y),Point(0, self.world_y)]

    def drawLine(self, start, end, lineColour="green"):
        turtle.shape('classic')
        turtle.penup()
        turtle.pencolor(lineColour)

        x = start[0]
        y = start[1]
        turtle.goto(offset + x, offset + y)

        # Use this to draw things on the screen
        turtle.pendown()
        dx = end[0]
        dy = end[1]
        turtle.goto(offset + dx, offset + dy)

        turtle.penup()
        turtle.update()

    def drawShapes(self, start, points, lineColour="blue", fillColour="white"):
        turtle.penup()
        turtle.pencolor(lineColour)
        
        x = start.x
        y = start.y
        turtle.goto(offset + x, offset + y)

        # Use this to draw things on the screen
        turtle.pendown()
        for point in points:
            dx = point.x
            dy = point.y
            turtle.goto(offset + dx, offset + dy)
        turtle.goto(offset + x, offset + y)  # connect them to start to form a closed shape
        
        # Set this back when drawing done
        turtle.penup()
        turtle.update()

    def drawResult(self, start, points, lineColour="blue"):
        turtle.penup()
        turtle.pencolor(lineColour)
        
        x = start.x
        y = start.y
        turtle.goto(offset + x, offset + y)

        # Use this to draw things on the screen
        turtle.pendown()
        for point in points:
            dx = point.x
            dy = point.y
            turtle.goto(offset + dx, offset + dy)
        
        # Set this back when drawing done
        turtle.penup()
        turtle.update()

    def draw(self):
        turtle.tracer(50000, delay=0) 
        turtle.register_shape("dot", ((-1,-1), (-1,1), (1,1), (1,-1)))
        turtle.register_shape("particle", ((-3, -2), (0, 3), (3, -2), (0, 0)))
        turtle.speed(0)
        
        self.drawShapes(self.origin, self.boundaries)
           
        for obstacle in self.obstacles:
            self.drawShapes(obstacle.vertices[0], obstacle.vertices, OBSTACLE_LINE_COLOR, OBSTACLE_FILL_COLOR)
            time.sleep(0.5)         

        turtle.home()
        turtle.update()

    # def show_robot(self, robot):
    #     turtle.shape('robot.gif')
    #     turtle.setposition( offset + robot.robot_x, offset + robot.robot_y)
    #     turtle.setheading(90)
    #     turtle.stamp()
    #     turtle.update()

    def drawPoints(self, start, end):
        turtle.shape('triangle')
        turtle.setposition( offset + start[0], offset + start[1])
        turtle.setheading(90)
        turtle.stamp()
        turtle.setposition( offset + end[0], offset + end[1])
        turtle.setheading(-90)
        turtle.stamp()
        turtle.update()
        time.sleep(2)