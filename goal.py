#!/usr/bin/env python
import rospy
import string
import math
import time
import sys

from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionResult
from actionlib_msgs.msg import GoalStatusArray
from geometry_msgs.msg import PoseStamped

class Goal:
    def __init__(self, goalX, goalY, retry, map_frame):
        self.sub = rospy.Subscriber('move_base/result', MoveBaseActionResult, self.statusCB, queue_size=10)
        self.pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)   
        # params & variables
        self.goalX = goalX
        self.goalY = goalY
        self.retry = retry
        self.goalMsg = PoseStamped()
        self.goalMsg.header.frame_id = map_frame
        self.goalMsg.pose.orientation.z = 0.0
        self.goalMsg.pose.orientation.w = 1.0
        # Publish the first goal
        time.sleep(1)
        self.goalMsg.header.stamp = rospy.Time.now()
        self.goalMsg.pose.position.x = self.goalX
        self.goalMsg.pose.position.y = self.goalY
        self.pub.publish(self.goalMsg) 
        rospy.loginfo("Initial goal published! Goal ") 
         

    def statusCB(self, data):
        if data.status.status == 3: # reached
            self.goalMsg.header.stamp = rospy.Time.now()                
            self.goalMsg.pose.position.x = self.goalX
            self.goalMsg.pose.position.y = self.goalY
            self.pub.publish(self.goalMsg)  
            rospy.loginfo("Initial goal published! Goal ")              
                


if __name__ == "__main__":
    try:    
        # ROS Init    
        rospy.init_node('multi_goals', anonymous=True)

        # Get params
        map_frame = rospy.get_param('~map_frame', 'map' )
        retry = rospy.get_param('~retry', '1') 
	goalListX = 0.5
	goalListY = 0.4
        mg = Goal(goalListX, goalListY, retry, map_frame)          
        rospy.spin()

    except KeyboardInterrupt:
        print("shutting down")
