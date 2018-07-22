#!/home/callum/anaconda2/bin/python
import rospy
from move_base_msgs.msg import *
from actionlib_msgs.msg import GoalStatusArray

def sendGoal1(publisher):
    goal = MoveBaseActionGoal()
    goal.goal.target_pose.header.frame_id = "map"
    goal.goal.target_pose.pose.orientation.w = 1.0
    goal.goal.target_pose.pose.position.x = 0
    goal.goal.target_pose.pose.position.y = -5
    publisher.publish(goal)

def sendGoal2(publisher):
    goal = MoveBaseActionGoal()
    goal.goal.target_pose.header.frame_id = "map"
    goal.goal.target_pose.pose.orientation.w = 1.0
    goal.goal.target_pose.pose.position.x = 2
    goal.goal.target_pose.pose.position.y = 2
    publisher.publish(goal)

def checkStatus(msg):
    global status
    # print(msg.status_list[0])
    status = msg.status_list[-1].status

if __name__=="__main__":
    rospy.init_node("goal_sender")
    pub = rospy.Publisher("move_base/goal", MoveBaseActionGoal)
    sub = rospy.Subscriber("move_base/status", GoalStatusArray, checkStatus)
    rate = rospy.Rate(1)
    status = 0

    while not rospy.is_shutdown():
        print("Going to goal 1")
        sendGoal1(pub)
        rate.sleep()

        while status != 3:
            rate.sleep()

        rate.sleep()
        print("Going to goal 2")
        sendGoal2(pub)
        rate.sleep()

        while status != 3:
            rate.sleep()
        rate.sleep()