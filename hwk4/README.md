Team PushKar
Color Tracking Robot

This is a Lab 4 submission for Group 20

Team Members: Anshuman Singh(as4916), Philippe Martin Wyder(pmw2125), Varun Jagdish Shetty(vs2567)

Virtual Implemenation:

This was an implementation of the Particle Filter logic for the localization problem. The implementation in the code here accounts for finding the robot location in a maze based on the maze boundaries and obstacles around it using its sensor reaadings. The code is made up of the following components-
 1. The Robot class which initializes the robot itself and all the particles with random x,y co-ordinates and orientation on the maze
 2. The Line class to help us implement the logic of finding the intersections of the particles/robot with the maze objects like obstacles and the maze walls
 3. The Maze class which is the turtle implementation of the drawing program to build out the world graphically
 
The code is implemented as follows- 
 1. The number of iterations are set to 80 and the number of particles to 3000 to get maximum variation in the particle localization and enough iterations to see a convergence
 2. We then create a myrobot instance to mimic our GoPiGo robot on the maze and 3000 particles spread out randomly on the maze. These are created with noise for forward movement, turns and sensor reading set to 0.05, 0.025, 1.1
 3. The robot is then moved ahead with a following conditions-
    a. If it sees an obstacle, it will turn
    b. else it moves ahead
 4. Once the robot is moved, we do a virtual scan for the robot to get the points near it with the noise for the sensor accounted for
 5. We then get the virtual scan for each particle and get a value from the Gaussian distribution for each virtual particle to account for its distance from the robot.
 6. We use the above values to create a weight list for each particle having a weight in it for its distance from the actual robot
 7. We then perform the importance sampling to use of the values with the higher weight into our next round of calculations. 
 8. We keep doing this for the total number of iterations and at the end of it have the value for the mean error of the clustered points around the actual robot
 
Observations-

The problem is largely governed by the intersection functions and the Gaussian + the importance sampling. We were observing very fast convergence and that to to a single point in 1 iteration which is why we changed the measurement_prob function to calculate the sum of probabilities for weights which were a bit higher than the other(there were some tending to 0 which were throwing off the entire readings and beta calculations). Post the calculation, we normalized the weight vector with the maximum weight value and gave that to the next step.

We had to tune the Sense Noise to handle the Gaussian values and get a better fit for the data. 



Real Robot Implementation:

The Real robot implementation is equivalent the above steps with code for the actual robot movement in the alternate file simple_particle_pka_REAL_ROBOT.py
