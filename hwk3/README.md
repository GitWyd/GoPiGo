Team PushKar
Color Tracking Robot

This is a Lab 2 submission for Group 20

Team Members: Anshuman Singh(as4916), Philippe Martin Wyder(pmw2125), Varun Jagdish Shetty(vs2567)

The video is shared at-

https://youtu.be/_nRAcdfiPMg

This was an implementation of the Color Tracking problem covered in class. Our target object color was set at a distance from the robot and we were using the following techniques to track the object using its color and area to move the robot accordingly. The code basically does these steps-

1) Wait for the click on the a particular object on the frame. Once the click is received it checks for BGR values of the imagepixel based on its co-ordinates and sets about creating an HSV mask for the BGR value to create an object boundary
2) Once the mask is created, we run it across a HSV converted format of the image to binarize the image for a hue saturation value range for the chosen color and post that we binarize the image using a threshold function
3) Once, the threshold is created, we erode and dilate the image to get a smoother and binarized image of the chosen object bereft of noise to make our color tracker better.
4) Once the optimized image is received we basically use the moments function to create a blob around the image for getting the area and the centroid of the image to track. 
5) Our move forward function is dependent on these values received from our image feed and we basically make our movements based on two factors, if the centroid has moved from its original location(centre of the image feed where if the object were off center when clicking on it, the robot would adjust itself first so the object is at the center of its field of view)- if it has, rotate to the angle where the centroid has shifted and if it hasn't check if the area of the object has changed. If yes then move forward or backward based on decrease or increase in area accordingly

Following were few considerations/assumptions made on our part for the purpose of the assignment - 
1 - The lighting should not flucuate much                        
2 - The chosen object should be of a bright color                        
3 - There's a threshold for when the robot should move front or back where we divide the area by  a tolerance factor 4500 and if that value changes, then we move the robot. This factor may change with different sizes of the objects


Our robot was able to perform all the above steps satisfactorily. 

Our code should handle the extra credit part equally well.

