'''
	Author: Philippe Wyder (PMW2125)
'''
import numpy as np
ROBOTORIGIN = [0,0,1] 
SERVODISTANCE = 7 
SENSORARM = 3

# function transforms Pr from the robot Frame to Pw in the world frame
# assumes coordinate format [x,y,phi]
def robot2world(Or, TrX, thetaRot):
	wHr = getwHr(Or)
        RzTheta = getTransformationMatrix(TrX, thetaRot)
        #print("robot2world() RzTheta ")
        #print(str(RzTheta))
        # wHr_new = [wHr][Rz,theta]
        wHr_new = np.dot(wHr,RzTheta) 
        #print("robot2world() wHr_new " + str(wHr_new))
        # Or_new = [wHr][Or]
	Or_newXY = np.array(wHr_new.dot(ROBOTORIGIN)).tolist()
        Or_new = [Or_newXY[0][0], Or_newXY[0][1], Or[2]+thetaRot]
        return Or_new
# transforms Pus in the ultrasonic sensors field of view to the world coordinate frame
def us2world(Or, dist, phi):
	wHr = getwHr(Or)
	rHus = getrHus(phi)
	wHus = np.dot(wHr,rHus)
	Pus = [dist,0,1]
	Pw = np.array(wHus.dot(Pus)).tolist()
        return Pw[0]
# function returns new robot location & orientation after a transformation and/or
# a rotation
def getNewRobotLocation(dist, Or, thetaRot):
        Tr = [dist,0,1]
        #print "getNewRobotLocation() Or " + str(Or) + "\tTr " + str(Tr)
        #print "getNewRobotLocation() thetaRot " + str(thetaRot)
        Or_new = robot2world(Or, Tr, thetaRot)
        #print "getNewRobotLocation() Or_new " + str(Or_new)
        return Or_new
# takes Or - Origin of the robot with respect to the world frame of the form [x,y,theta]
# returns transformation matrix wHr (world_H_robot)
def getwHr(Or):
        return  np.matrix([[np.cos(Or[2]),-np.sin(Or[2]),Or[0]],[np.sin(Or[2]), np.cos(Or[2]), Or[1]],[0,0,1]]) 
# takes the servo rotation orientation phi with respect to the robot, and returns
# returns transformation matrix rHus (robot_H_ultrasonic)
def getrHus(phi):
	servo = [SERVODISTANCE,0,phi]
	o2 = [servo[0],servo[1]]
	rHs = np.matrix([[np.cos(phi),-np.sin(phi),o2[0]],[np.sin(phi), np.cos(phi), o2[1]],[0,0,1]])
	sHus = np.matrix([[1,0,SENSORARM],[0,1,0],[0,0,1]])
	rHus = np.dot(rHs,sHus)
	return rHus
# returns a rotation matrix Rz,theta
def getTransformationMatrix(Tr, theta):
        return np.array([[np.cos(theta),-np.sin(theta),Tr[0]],[np.sin(theta),np.cos(theta),Tr[1]],[0,0,1]])

def main():
	# how to use robot2world(PointInRobotCoordinateFrame, Origin of Robot Coordinate Frame)
	theta = 0
	Or = [0,0,theta]
        #print("main: Old Robot Origin " + str(Or))
        Or1 = getNewRobotLocation(5,Or,0)
        Or2 = getNewRobotLocation(5,Or1,0)
        Or3 = getNewRobotLocation(5,Or2,0)
        #print("main: New Robot Origin " + str(Or_new))
        # how to use us2world(PointInUSCoordinateFrame, Origin of Robot Coordinate Frame)
	distUS = 10
	phi = 0
	#print(us2world(Or, distUS, phi))

if __name__ == '__main__':
	main()

