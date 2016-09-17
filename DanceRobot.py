def danceMoves( time ):
   timer = Timer()
   random = Random()
   while(timer.get_time_ss<20):
   	motorDanceMoves()

   stop()
   return [expression]
def motorDanceMoves():
	lmot = rndMotor.randint(0, 1)
   	rmot = rndMotor.randint(0, 1)
   	steps = rndSteps.randint(0,18)
   	left_rot()
   	enc_tgt(lmot,rmot,steps)
   	time.sleep(90)
   	stop()
   	bwd()
   	lmot = rndMotor.randint(0, 1)
   	rmot = rndMotor.randint(0, 1)
   	steps = rndSteps.randint(0,18)
   	right_rot()
   	enc_tgt(lmot,rmot,steps)
   	time.sleep(90)
   	stop()
   	fwd()
def sensorDanceMoves():
   for i in range(180):
   	servo(i)
   	time.sleep(10)
   for i in range(180):
   	servo(180-i)
   	time.sleep(10)
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