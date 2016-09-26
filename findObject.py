from gopigo import *                              
import math                                       
import time                                       
                                                  
US_MAX_DIST = 160                           
US_PIN = 15                                       
SPEED = 150
TIME_INCREMENTS = 0.2
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 64 # Pulses Per Revolution          

DIRECTION = True #True = Left, False = right      
APPROACHING_DIST = 20                             
                                                  
def findObject(direction):                        
    turnToObjectDirection(direction)              
    approachObject(APPROACHING_DIST)
def approachObject(minDist):            
    while(us_dist(US_PIN)-minDist>0):             
        if (isObject()):
            print 'I am approaching by steps:'
            stepSize = int((us_dist(US_PIN)-minDist)/2)
            print stepSize
            goForward(stepSize/2)
            if (us_dist(US_PIN)-minDist < 0):
                stop()
                return
            time.sleep(1)                       
        else:
            print 'lost target - recalibrate'
            direction = getObjDirection()
            if (direction == 99):
                turnToObjectDirection(DIRECTION) 
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
        print 'object not found'
        turn(direction,TIME_INCREMENTS,SPEED)
    print 'object found'
    objectSize = 1                                
    while(isObject()):                              
        objectSize += 1                           
        print 'measuring object width'
        turn(direction,TIME_INCREMENTS,SPEED)     
    turn(not direction,objectSize/2*TIME_INCREMENTS,SPEED)                                          
def isObject():
    time.sleep(1)
    dist = us_dist(US_PIN)
    print dist
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
    distToWheelRatio = float(distance/WHEEL_CIRCUMFERENCE)
    encoder_counts = int(distToWheelRatio*ENCODER_PPR) 
    enc_tgt(1,1,encoder_counts)                       
    fwd()                                         
if __name__=='__main__': 
    enable_servo()
    findObject(DIRECTION)
