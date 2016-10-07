'''
	Author: Philippe Wyder (PMW2125)
'''
import numpy as np
ROBOT = [0,0,0]  #robot vector  [x,y,theta]
SERVODISTANCE = 7 
SENSORARM = 3

# function transforms Pr from the robot Frame to Pw in the world frame
# assumes coordinate format [x,y,phi]
def robot2world(Pr, Or):
	wHr = getwHr(Or)
	Pw = np.array(wHr.dot(Pr)).tolist()
        print "robot2world():" + str(Pw[0]) 
        return Pw[0]
# transforms Pus in the ultrasonic sensors field of view to the world coordinate frame
def us2world(Or, dist, phi):
	wHr = getwHr(Or)
	rHus = getrHus(phi)
	wHus = np.dot(wHr,rHus)
	Pus = [dist,0,1]
	Pw = np.array(wHus.dot(Pus)).tolist()
        print "us2world():" + str(Pw[0]) 
        return Pw[0]
def getNewRobotLocation(dist, Or, theta):
        Pr = [dist,0,theta]
        dr = robot2world(Pr, Or)
        print "getNewRobotLocation() Pr - dr" + str(Pr) + "-" + str(dr)
        Or = [x + y for x,y in zip(Or,dr)]
        return Or
# returns transformation matrix wHr (world_H_robot)
def getwHr(robot):
	o1 = [robot[0],robot[1]]
	theta = robot[2]
	wHr = np.matrix([[np.cos(theta),-np.sin(theta),o1[0]],[np.sin(theta), np.cos(theta), o1[1]],[0,0,1]])
	return wHr
# takes the servo rotation orientation phi with respect to the robot, and returns
# returns transformation matrix rHus (robot_H_ultrasonic)
def getrHus(phi):
	servo = [SERVODISTANCE,0,phi]	
	o2 = [servo[0],servo[1]]
	rHs = np.matrix([[np.cos(phi),-np.sin(phi),o2[0]],[np.sin(phi), np.cos(phi), o2[1]],[0,0,1]])
	sHus = np.matrix([[1,0,SENSORARM],[0,1,0],[0,0,1]])
	rHus = np.dot(rHs,sHus)		
	return rHus

def main():
	# how to use robot2world(PointInRobotCoordinateFrame, Origin of Robot Coordinate Frame)
	Pr = [3,0,1]
	theta = np.pi
	Orobot = [3,3,theta]
        r2s = robot2world(Pr, Orobot)
	print(r2s)
        # how to use us2world(PointInUSCoordinateFrame, Origin of Robot Coordinate Frame)
	distUS = 10
	phi = 0
	print(us2world(Orobot, distUS, phi))

if __name__ == '__main__':
	main()

