# Shortest-Path-using-Image-Processing

#
**Using Image Processing this code finds a shortest path between two junctions in the given image of line maze.**
 
There are 3 python scripts named path_finding.py, helper_functions.py, helper_class.py 
path_finding.py is the main script. 
cv2 and numpy are the modules used. 

#
**Flow of code:** 
 
Image is read, resized and filtered to find junctions. 
These junction co-ordinates are then used to make a graph. 
This graph is then used to find shortest path. 
 
#
**How to run the program:** 

Run the path_finding.py file. 
"Arena" and "solution_img" windows will appear. 
Using mouse **left click** select any point on line as **_start point_** and **right click** for **_end point_** in the window named "Arena". 
Square will be marked at the start point and circle at the end point. 
Shortest path will be highlighted in **green**. 
Now, different start and end points can also be selected. 
Press enter to change the image in window "Arena" and "q" to exit. 

#
IDE used is JetBrains PyCharm Community Edition 2019.2.5 x64
