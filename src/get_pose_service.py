#!/home/callum/anaconda2/bin/python
import rospy
from localization_tests.srv import *
from geometry_msgs.msg import * 
from tf2_msgs.msg import *

def handle_req(req):
    global currentPose
    resp = GetPoseResponse()
    resp.pose = currentPose
    return resp 

def pose_callback(msg):
    global currentPose
    print("yeet")
    currentPose = msg.pose.pose

global currentPose

if __name__ == "__main__":
    rospy.init_node("get_pose_server")
    sub = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, pose_callback)
    currentPose = Pose()
    serv = rospy.Service("get_pose", GetPose, handle_req)

    print("Good to go")
    
    rospy.spin()
