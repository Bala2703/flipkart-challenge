#!/usr/bin/env python
from inspect import trace
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import math
import time
target = 90
kp = 0.09


class TurtleBot:
    def __init__(self):
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher(
            '/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber(
            '/turtle1/pose', Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)
        self.r2 = rospy.Rate(5)
        self.yaw = 0
    def update_pose(self,data:float):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.theta = data.theta
    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.y - self.pose.y), 2))  
    def linear_vel(self, goal_pose, constant=0.1):
        return constant * self.euclidean_distance(goal_pose) 
    def euclidean_distance_x(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2))  
    def linear_vel_x(self, goal_pose, constant=0.1):
        return constant * self.euclidean_distance_x(goal_pose)    
    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)  
    def angular_vel(self, goal_pose, constant=1):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)
    def move_y(self):
        goal_pose = Pose()
        goal_pose.x = 0
        goal_pose.y = -0.6
        distance_tolerance = 0.09
        vel_msg = Twist()
        while self.euclidean_distance(goal_pose) >= distance_tolerance:
            vel_msg.linear.x = self.linear_vel(goal_pose)
            rospy.loginfo("linear velocity Move y --> %f",vel_msg.linear.x)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            # Publish at the desired rate.
            self.rate.sleep()
            # Stopping our robot after the movement is over.
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
             # If we press control + C, the node will stop.
   
    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()
        # Get the input from the user.
        goal_pose.x = 0.6
        goal_pose.y = -0.6
     #    float(input("Set your y goal: "))
        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = 0.1
     #    float(input("Set your tolerance: "))
        vel_msg = Twist()
        while self.euclidean_distance_x(goal_pose) >= distance_tolerance:
            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control
            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            rospy.loginfo("linear velocity Move x --> %f goal distance --> %f",vel_msg.linear.x,self.euclidean_distance(goal_pose))
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            # Publish at the desired rate.
            self.rate.sleep()
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        # If we press control + C, the node will stop.

    def rotate(self):
        command =Twist()
        stop = Twist()
        stop.linear.x = 0 
        stop.angular.z = 0
        while(True):
            target_rad = target*math.pi/180
            command.angular.z = -0.3
            self.velocity_publisher.publish(command)
            self.r2.sleep()
            self.velocity_publisher.publish(stop)
            time.sleep(1)
            print("target={} current:{}", target,math.degrees(self.pose.theta))
            if(math.degrees(self.pose.theta)>85 and math.degrees(self.pose.theta)<100):
                self.velocity_publisher.publish(stop)
                print("reached")
                break

if __name__ == '__main__':
   try:
        x = TurtleBot()
        x.move_y()
        x.rotate()
        x.move2goal()
        x.move_y()
        x.rotate()
        x.move2goal()
   except rospy.ROSInterruptException:
       pass

