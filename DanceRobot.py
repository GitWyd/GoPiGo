from gopigo import * # has basic robot control fucntions
import sys #used for clsing the running program
from random import Random
def main():
   timer = Timer()
   random = Random()
   while(True):
        print "I'm looping"
        motorDanceMoves(random)
        sensorDanceMoves()
def motorDanceMoves(rnd):
        print "Start Motor Moves"
        lmot = rnd.randint(0, 1)
   	rmot = rnd.randint(0, 1)
   	steps = rnd.randint(0,9)
   	left_rot()
   	enc_tgt(lmot,rmot,steps)
   	time.sleep(1)
   	stop()
   	bwd()
        fwd()
   	lmot = rnd.randint(0, 1)
   	rmot = rnd.randint(0, 1)
   	steps = rnd.randint(0,9)
   	right_rot()
   	enc_tgt(lmot,rmot,steps)
   	time.sleep(1)
   	stop()
   	fwd()
        bwd()
        print "stop motor moves"
def sensorDanceMoves():
    print "start sensor moves"
    for i in range(0,30,90):
   	servo(i)
   	time.sleep(1)
    for i in range(0,30,90):
   	servo(90-i)
   	time.sleep(1)
    print "stop sensor moves"
class Timer:
  def __init__(self):
    self.start = time.time()

  def restart(self):
    self.start = time.time()

  def get_time_hhmmss(self):
    end = time.time()
    m, s = divmod(end - self.start, 60)
    h, m = divmod(m, 60)
    time_str = "%02d:%02d:%02d" % (h, m, s)
    return time_str

  def get_time_ss(self):
    return time.time()
if __name__ == '__main__':
    print "getting started"
    main()
    print "we're done"
    stop()
    sys.exit()


