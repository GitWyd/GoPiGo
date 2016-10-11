This is a Lab 1 submission for Group 20

Team Members: Anshuman Singh(as4916), Philippe Martin Wyder(pmw2125), Varun Jagdish Shetty(vs2567)

The video is shared at-

https://youtu.be/qu1PkV9L0Zc

This was an implementation of the Bug2 algorithm covered in class. Our target was set at 300 meters away from the robot and we were using global variables to track the object co-ordinates. The code basically does these steps-
1) Align to the target co-ordinates
2) Move along the m-line till it sees an obstacle
3) Moves around the object using a perimeter following function
4) While moving around the object keeps track of the m-line by translating each move forward function from the robot co-ordinates to worl co-ordinate system. 
5) If it meets the m-line, it re-aligns and heads down the m-line again till next obstacle or target.
6) If it encounters a co-ordinate already encountered, it realises that it is in a trap and breaks out.

Our robot was able to perform all the above steps satisfactorily. 

We did not do the extra credit part
