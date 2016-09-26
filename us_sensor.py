from gopigo import *
import sys

enable_servo()
servo(90)
print 'Enter one of the following distances(cms):'
print 5
print 30
print 60
while True:
    print 'Press X to exit'

    option = raw_input('Enter your choice: ')
    print option
    if option == 'X' or option == 'x':
        sys.exit()
    else:
        print 'Comparing input  ' + option  + ' cms with sensor returned distance ' + str(us_dist(15)) + ' cms'



