#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import pow, atan2, sqrt
from turtlesim.msg import Pose


class turtlemover:
    def __init__(self):
        rospy.init_node('Turtle_mover',anonymous=True)
        self.velocity_publisher= rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, self.callback)                                   
        self.pose=Pose()
        self.rate=rospy.Rate(10)
        
    def get_distance(self,goal_pose):
        distance = sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))
        return distance
                      
    def callback(self,data):
        self.pose=data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.theta=round(self.pose.theta,4)
        
    def s_angle(self,goal_pose):
        angle= atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
        return angle

    def v_contoller(self,goal_pose):
        if  self.get_distance(goal_pose)<1:
            return 1*self.get_distance(goal_pose)
        else:
            return 1

    def move2position(self,X,Y):
        goal_pose= Pose()
        goal_pose.x=  X
        goal_pose.y = Y
        distance_tolerance = 0.01
        vel_msg = Twist()
        while self.get_distance(goal_pose) >= distance_tolerance:
            vel_msg.linear.x = self.v_contoller(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 1*(self.s_angle(goal_pose)-self.pose.theta)
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        
    def rotate(self,X,Y):
        goal_pose=Pose()
        goal_pose.x=  X
        goal_pose.y = Y
        vel_msg = Twist()
        angle_tolerance = 0.001
         
        while abs(self.s_angle(goal_pose)-(self.pose.theta)) >= angle_tolerance:
            print(abs(self.s_angle(goal_pose)-(self.pose.theta)))
            #linear velocity in X-axis
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            
            #angular velocity in the Z-axis
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 1*(self.s_angle(goal_pose)-self.pose.theta)
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        x = turtlemover()
        
        #coordinates
        X0 = float(input("set your x Coordinates: "))
        Y0 = float(input("set your y Coordinates: "))
        a = float(input("enter length: "))
        b = float(input("enter height: "))
        X1 = X0 + a
        Y1 = Y0 + b
        Y2 = 2*b + Y0
        
        X_max = 11 
        Y_max = 11
        
        if X1>X_max and Y1>Y_max:
           a = a - (X1 - X_max)
           X1 = X0 + a
           b = b - (Y1 - Y_max)
           Y1 = Y0 + b
           C = [[X0,Y0], [X1,Y0], [X1,Y1], [X0,Y1]]
        else:
           if X1> X_max:
              a = a - (X1 - X_max)
              X1 = X0 + a
           if Y1>Y_max:
              b = b - (Y1 - Y_max)
              Y1 = Y0 + b
           if Y2> Y_max:
              Y2 = Y_max   
       
           C = [[X0,Y0], [X1,Y0], [X1,Y1], [X0,Y1], [X0,Y2], [X1,Y2]]
        
        for i in range(len(C)):
            x.rotate(C[i][0],C[i][1])
            x.move2position(C[i][0],C[i][1]) 
        x.rotate(5.5,5.5)
        x.move2position(5.5,5.5)
        x.rotate(10,5.5)

    except rospy.ROSInterruptException:
        pass


