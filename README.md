This is a Lab 1 submission for Group 20

Team Members: Anshuman Singh(as4916), Philippe Martin Wyder(pmw2125), Varun Jagdish Shetty(vs2567)

Question 1: Done

Question 2: Done. The robot leans to the right and trim had to be applied. We spoke to the TA and it seems to be an issue with the wheel in most robots

Question 3: Done

Question 4: Done. 
The sensor accuracy is 
Sr No | Distance Set | Observed Distance
   1		5					5
   2	   30				   38
   3	   60                  76
The observed error was in the general range of 26.7% which is useful for calculations in the next problem

Question 5 - Done. 
We based the calculation of this on the concept the professor discussed in class about the distance value returned by the sensor. Given that the distance is provided by the closest object in the beam's cone provides the response, out idea was to keep rotating the servo till the same distance isn't returned by the sensor. This was achieved by setting the servo initially at 90 and finding the distance d from the wall. Once this is recorded we keep rotating the servo till it stops returning the value d. We also accounted for the error reported in the problem above and tested for various distances from the wall. The average angle observed was 30 with values ranging from 28-34 for smaller to larger distances from the wall respectively(accounted for distance errors).

Question 6 - Done
