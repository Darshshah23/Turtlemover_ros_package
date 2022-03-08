





## Introduction

This package includes a node that simulates the turtle's Lawnmower pattern movement (from the package turtlesim).

The user is asked for the start point, length, and width of the lawnmower pattern by the turtle. Throughout the trajectory, the turtle uses a feedback control mechanism to correct its position and orientation. The turtle first rotates until it is facing directly at the target position, then moves toward the goal position. This cycle of rotation and movement continues until the pattern is completed.

Ensure the robot handles the case where it hits the wall, adjust the pattern when the scenario is encountered.


A special velocity message containing only the turtle's planar forward and planar rotational velocities is included in the package.

## Implemetation

1. **Create a new workspace and clone the demonstration code.**
```
# clone the demonstration code
cd catkin_ws/src
git clone https://github.com/Darshshah23/Turtlemove.git

# return to catkin_ws root
cd ../ 
```
2. **Build the workspace and activate it.**
```
catkin_make
source devel/setup.bash
```
3. **Launch the node.**
```
roslaunch Turtlemover_ros_package Turtlemover.launch
```



