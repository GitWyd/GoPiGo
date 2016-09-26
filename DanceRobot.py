'''
COMS W4733 - PMW2125/UNI Anshuman/UNI Varun
'''

from gopigo import * # has basic robot control fucntions
import sys #used for clsing the running program
from random import Random
import time

DANCE_DURATION = 20

def main(duration):
   #timer = Timer()
   start_time = time.time()
   random = Random()

   while(duration > time.time()-start_time):
        print time.time()-start_time
        print "I'm looping"
        motorDanceMoves(random)
        sensorDanceMoves()
def motorDanceMoves(rnd):
        max_move = 10
        print "Start Motor Moves"
        lmot = rnd.randint(0, 1)
   	rmot = rnd.randint(0, 1)
   	steps = rnd.randint(0,max_move)
   	enc_tgt(lmot,rmot,steps)
        #backward step
   	bwd()
   	time.sleep(0.5)
   	stop()
        left_rot()
        time.sleep(.2)
        stop()
   	right_rot()
        time.sleep(.2)
   	stop()
        #forward step
        fwd()
   	time.sleep(0.5)
   	stop()
   	right_rot()
        time.sleep(.2)
   	stop()
        left_rot()
        time.sleep(.2)
        stop()
   #	lmot = rnd.randint(0, 1)
   #	rmot = rnd.randint(0, 1)
   #	steps = rnd.randint(0,max_move)
   #	right_rot()
   #	enc_tgt(lmot,rmot,steps)
   #	time.sleep(1)
   #	stop()
   #	fwd()
   #     bwd()
        print "stop motor moves"
def sensorDanceMoves():
    print "start sensor moves"
    for i in range(0,180,30):
   	servo(i)
   	time.sleep(0.1)
   	servo(180-i)
   	time.sleep(0.1)
    print "stop sensor moves"
#class Timer:
#  def __init__(self):
#    self.start = time.time()
#
#  def restart(self):
#    self.start = time.time()
#
#  def get_time_hhmmss(self):
#    end = time.time()
#    m, s = divmod(end - self.start, 60)
#    h, m = divmod(m, 60)
#    time_str = "%02d:%02d:%02d" % (h, m, s)
#    return time_str
#
#  def get_time_ss(self):
#    return time.time()
if __name__ == '__main__':
    print "getting started"
    main(DANCE_DURATION)
    print "we're done"
    stop()
    sys.exit()


