Team PushKar
Path Planner Robot

This is a Lab 5 submission for Group 20

Team Members: Anshuman Singh(as4916), Philippe Martin Wyder(pmw2125), Varun Jagdish Shetty(vs2567)

The following submission is made up of the following files:

1. obstacle.py - Contains code for reflection algorithm and accessory functions

2. visibility_graph.py - Contains code for creating visibility graph, dijkstra and a_star_search algorithms

3. draw_world.py - Contains turtle python code to draw required world

4. follow_path.py - Contains required odometry and sensor check codes to move the robot on the course

5. point.py - contains our Point class to identify co-ordinates on the graph

6. robot.gif - our awesome robot plotted on the turtle world

7. obstacles.txt - map of the robotrace

The program can be run by running the command `python obstacle.py obstacles.txt` on the GoPiGo robot.

If run on the console just to see the simulation, we'd need to comment line number 2 in obstacle.py to not run the odometry code

The program works as under -

1) We are assuming a size of 24 X 24 cm robot and reflecting along the top left corner

2) When you run the progrram, you will see it outputting all the relevant information like

	a. convex hull co-ordinates

	b. The graph of the map created

	c. The shortest path calculated

	d. Cost of taking the chortest path in terms of distance

3) While running this, we can see the same being generated on the turtle display console where the following are displayed

	a. start and end points

	b. The expanded polygons based on reflection

	c. The obstacles

	d. All the edges between all components ie start --> hulls, hulls--> hulls , hulls --> end

	e. The robot traversing the shortest path

4) Once the final path is traversed on the display console, just click it to continue to run the actual odometry on the robot. Clicking on the turtle display console exits the screen and allows us to resume the program.

5) The odometry is achieved as thus-
	a. We pass the result of the Dijkstra shortest path to follow_path.py as a set of points on the graph to traverse in the real world system with the robot location ie start point and the robot facing straight ahead

	b. The program then creates a line from the start to the first point on the path and keeps iteratively doing it for each consecutive point from the last point travelled to.

	c. We calculate the l2 distance between the 2 points to traverse and break it down into steps to take for the robot and make it move in the steps till either the number of steps have been taken or we see an obstacle on the path based on the readings from the servo. We also calculate the slope of the line and rotate the robot to make the rotation before following the path

	d. Once a point is reached, we do (c) again for the next set of points and repeat till end point has been reached

	e. Odometry is an issue and our trim tests have taken care of most issues. We also have a velcro band attached to the wheel of the robot for better traction

6) We also have the code for identifying the orange cone which once the robot reaches the end point looks around for the orange and tries to match the hue color for it. Once it locates it, it will keep moving forward till the servo readings tell it to stop.


