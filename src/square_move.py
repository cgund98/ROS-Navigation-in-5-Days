#!/home/callum/anaconda2/bin/python
import rospy
from math import pi
from geometry_msgs.msg import *

class MoveWrapper(object):
    def __init__(self):
        self._vel_pub = rospy.Publisher("husky_velocity_controller/cmd_vel", Twist)
        self._vel = Twist()
        self._pose_sub = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.pose_cb)
        self._pose = Pose()
        self._rate = rospy.Rate(10)

        self._lspeed = .5
        self._aspeed = .25

    def pose_cb(self, msg):
        self._pose = msg.pose.pose

    def move(self, direction):
        if direction == "forwards":
            self._vel.linear.x = self._lspeed
            self._vel.angular.z = 0
        if direction == "backwards":
            self._vel.linear.x = -self._lspeed
            self._vel.angular.z = 0
        if direction == "left":
            self._vel.linear.x = 0
            self._vel.angular.z = self._aspeed
        if direction == "right": 
            self._vel.linear.x = 0
            self._vel.angular.z = -self._aspeed
        if direction == "stop":
            self._vel = Twist()
        self._vel_pub.publish(self._vel)

    def move_square(self):
        global shutdown
        print("Starting...")
        print("Moving Left")
        while self._pose.orientation.z < .49 and not shutdown:
            self.move("left")
            self._rate.sleep()
        print("Moving Forwards")
        while self._pose.position.y < 1 and not shutdown:
            self.move("forwards")
            self._rate.sleep()
        print("Moving Left")
        while self._pose.orientation.z < .99 and not shutdown:
            self.move("left")
            self._rate.sleep()
        print("Moving Forwards")
        while self._pose.position.x > -3 and not shutdown:
            self.move("forwards")
            self._rate.sleep()
        print("Moving Left")
        while self._pose.orientation.z < -.51 or self._pose.orientation.z > -.49 and not shutdown:
            self.move("left")
            self._rate.sleep()
        print("Moving Forwards")
        while self._pose.position.y > -2 and not shutdown:
            self.move("forwards")
            self._rate.sleep()
        print("Moving Left")
        while self._pose.orientation.z < -.01 and not shutdown:
            self.move("left")
            self._rate.sleep()
        print("Moving Forwards")
        while self._pose.position.x < 0 and not shutdown:
            self.move("forwards")
            self._rate.sleep()
        self.move("stop")
        print("Done...")

def shutdownhook():
    global shutdown
    shutdown = True

if __name__ == "__main__":
    rospy.init_node("move_square")
    move_wrapper = MoveWrapper()
    shutdown = False

    rospy.on_shutdown(shutdownhook)

    move_wrapper.move_square()

    move_wrapper.move("stop")


