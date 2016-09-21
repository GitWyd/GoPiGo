from gopigo import *                              
import math                                       
import time                                       
                                                  
US_US_MAX_DIST = 200                              
US_PIN = 15                                       
DIRECTION = True #True = Left, False = right      
SPEED = 100                                       
TIME_INCREMENTS = 1                               
WHEEL_CIRCUMFERENCE = 20.4                        
ENCODER_PPR = 64 # Pulses Per Revolution          
                                                  
APPROACHING_DIST = 20                             
                                                  
def findOBject(direction):                        
    turnToObjectDirection(direction)              
    approachObject(APPROACHING_DIST)              
def approachObject(minDist, stepSize):            
    while(us_dist(US_PIN)-minDist>0):             
        if (isObject()):                          
            stepSize = int(us_dist(US_PIN)/2)     
            goForward(stepSize)                   
            time.sleep(0.2)                       
        else:                                     
            direction = getObjDirection()         
            turnToObjectDirection(direction)      
                                                  
def getObjDirection():                            
    for (i in range(20,20,160)):                  
        if(isObject()):                           
            if (i>90):                            
                return True                       
            else:                                 
                return False                      
                                                  
def turnToObjectDirection(direction):             
    while(not isObject):                          
        turn(direction,TIME_INCREMENTS,SPEED)     
    objectSize = 1                                
    while(isObject):                              
        objectSize += 1                           
        turn(direction,TIME_INCREMENTS,SPEED)     
    turn(not direction,objectSize/2*TIME_INCREMENTS,SPEED)                                          
                                                  
def isObject():                                   
    if (us_dist(US_PIN) < US_MAX_DIST):           
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
    distToWheelRation = float(distance/WHEEL_CIRCUMFERENCE)                                         
    encoder_counts = int(distToWheelRatio*ENCODER_PPR)                                              
    enc_tgt(encoder_counts)                       
    fwd()                                         
if __name__==__main__:                            
    findObject()                     
