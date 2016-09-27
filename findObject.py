from gopigo import *                              
import math                                       
import time                                       
                                                  
US_MAX_DIST = 140                           
US_PIN = 15                                       
ROTATE_SPEED = 50
DRIVE_SPEED = 140
TIME_INCREMENTS = 0.20
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 18 # Pulses Per Revolution          

DIRECTION = True #True = Left, False = right      
APPROACHING_DIST = 22                             
                                                  
#def findObject(direction):                        
#    turnToObjectDirection(direction)              
#    approachObject(APPROACHING_DIST)
def approachObject(minDist):            
    #while(us_dist(US_PIN)-minDist>0):             
    while(True):
        if (isObject()):
            print 'I am approaching by steps:'
            stepSize = int((us_dist(US_PIN)-minDist)/2)
            print 'step Size:' + str(stepSize)
            print 'us_dist before goFwd()' + str(us_dist(US_PIN))
            goForward(stepSize)
            print 'us_dist after goFwd()' + str(us_dist(US_PIN))
            if (us_dist(US_PIN)-minDist < 0):
                stop()
                return
            time.sleep(.2)                       
        else:
            print 'lost target - recalibrate'
            direction = getObjDirection()
            if (direction == 99):
                turnToObjectDirection(DIRECTION) 
            else:
                turnToObjectDirection(direction)      
                                                  
def getObjDirection():                            
    for i in range(20, 160,20 ):
        servo(i)
        if(isObject()):                           
            if (i>90):                            
                servo(90) 
                return 1                       
            else:                                 
                servo(90) 
                return 0
    servo(90) 
    return 99
                                                  
def turnToObjectDirection(direction):             
    servo(90)
    while(not isObject()):
        print 'TurnToOBject(): object not found'
        turn(direction,TIME_INCREMENTS,ROTATE_SPEED)
    print 'TurnToObject(): object found'
    objectSize = 1                                
    while(isObject()):                              
        objectSize += 1                           
        print 'measuring object width'
        turn(direction,TIME_INCREMENTS,ROTATE_SPEED)     
    print 'object size:' + str(objectSize)
    turn(not direction,objectSize/2*TIME_INCREMENTS,ROTATE_SPEED)                                          
def isObject():
    time.sleep(.5)
    dist = us_dist(US_PIN)
    if (dist < US_MAX_DIST and dist > 5):           
        return 1                                  
    return 0                                      
def turn(direction, seconds, speed):              
    set_speed(speed)                              
    if (direction):                               
        left_rot()                                
    else:                                         
        right_rot()                               
    time.sleep(seconds)                           
    stop()                                        
def goForward(distance):
    set_speed(DRIVE_SPEED)
    distToWheelRatio = float(abs(distance)/WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR) 
    enc_tgt(1,1,encoder_counts) 
    if (distance >= 0):
        fwd() 
    else:
        bwd()
if __name__=='__main__': 
    enable_servo()
    approachObject(APPROACHING_DIST)
    stop()
