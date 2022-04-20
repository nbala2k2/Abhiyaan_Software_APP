#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
def talker():
    pub = rospy.Publisher('/team_abhiyaan', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        str_ab="Team Abhiyaan rocks:"
        pub.publish(str_ab)
        rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
