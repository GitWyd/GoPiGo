from gopigo import *
import math
import time

US_SENSOR_PORT = 15
enable_servo()
servo(90)
perpendicular_dist = us_dist(US_SENSOR_PORT)
angle = 0
for i in range(90,0, -1):
    servo(i)
    time.sleep(1)
    expected_dist = perpendicular_dist / math.cos(math.radians(i))
    calculated_dist = us_dist(US_SENSOR_PORT)
    if not (math.abs(expected_dist - calculated_dist) < (0.20 * perpendicular_dist)):
        print 'The angle is: ' + 90 - i
        angle = 2 * 90 - i

print 'Total range is: ' + angle
