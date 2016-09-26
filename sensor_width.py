from gopigo import *
import math
import time

US_SENSOR_PORT = 15
enable_servo()
servo(90)
time.sleep(5)
perpendicular_dist = us_dist(US_SENSOR_PORT)
angle = 0
for i in range(90,0, -2):
    servo(i)
    time.sleep(2)
    print "Perpendicular distance: " + str(perpendicular_dist)
    calculated_dist = us_dist(US_SENSOR_PORT)
    print "Calculated distance is: " + str(calculated_dist)
    if perpendicular_dist < calculated_dist and calculated_dist - perpendicular_dist > 0.01 * perpendicular_dist:
        print 'The angle is: ' + str(90 - i)
        angle = 2 * (90 - i)
        break

disable_servo()
print 'Total range is: ' + str(angle)
