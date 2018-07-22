#!/home/callum/anaconda2/bin/python
import rospy
from move_base_msgs.msg import *
from geometry_msgs.msg import *
from nav_msgs.srv import *
from actionlib_msgs.msg import GoalStatusArray

def sendGoal1(service):
    global pose
    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.pose.orientation.w = 1.0
    goal.pose.position.x = 0
    goal.pose.position.y = -5
    return service(pose, goal, 0.0)

def sendGoal2(service):
    global pose
    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.pose.orientation.w = 1.0
    goal.pose.position.x = 2
    goal.pose.position.y = 2
    return service(pose, goal, 0.0)

def updatePose(msg):
    global pose
    # print(msg.status_list[0])
    pose.header = msg.header
    pose.pose = msg.pose.pose
    # status = msg.status_list[-1].status

if __name__=="__main__":
    rospy.init_node("goal_sender")
    rospy.wait_for_service("move_base/make_plan")
    serv = rospy.ServiceProxy("move_base/make_plan", GetPlan)
    sub = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, updatePose)
    rate = rospy.Rate(.5)
    pose = PoseStamped()
    # status = 0
    print("Ready")

    rate.sleep()
    print(sendGoal1(serv))

    # while not rospy.is_shutdown():
    #     print("Going to goal 1")
    #     sendGoal1(serv)
    #     rate.sleep()

    #     while status != 3:
    #         rate.sleep()

    #     rate.sleep()
    #     print("Going to goal 2")
    #     sendGoal2(serv)
    #     rate.sleep()

    #     while status != 3:
    #         rate.sleep()
    #     rate.sleep()