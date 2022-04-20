#!/usr/bin/env python
# import necesary modules
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt,sin,cos,tan
from cmath import pi
import time



class TurtleBots:
    def __init__(self):
        # Creates a node with name 'two_body_simulation' and make sure it is a unique node (using anonymous=True).
        rospy.init_node('two_body_simulation', anonymous=True)


        #################### TURTLE-1 #######################
        # to publish to turtle1 to move
        self.velocity1_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        # subscribe to topic for getting own position, calls function to update own position
        self.pose1_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        # pose object for own position
        self.pose1 = Pose()


        #################### TURTLE-2 ########################
        # to publish to turtle2 to move
        self.velocity2_publisher = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        # subscribe to topic for getting own position, calls function to update own position
        self.pose2_subscriber = rospy.Subscriber('/turtle2/pose', Pose, self.update_pose2)
        # pose object for own position
        self.pose2 = Pose()


        self.rate = rospy.Rate(100)


    # function to update own postion
    def update_pose(self, data):
        self.pose1 = data
        self.pose1.x = round(self.pose1.x, 4)
        self.pose1.y = round(self.pose1.y, 4)
    def update_pose2(self, data):
        self.pose2 = data
        self.pose2.x = round(self.pose2.x, 4)
        self.pose2.y = round(self.pose2.y, 4)

    def euclidean_distance(self):
        return sqrt(pow(( self.pose2.x- self.pose1.x), 2) +pow((self.pose1.y - self.pose2.y), 2))
    
    def angle(self):
        a=atan2(self.pose2.y-self.pose1.y,self.pose2.x-self.pose1.x)
        return a

    
    def simulate_gravity(self):

        v_msg1 = Twist()
        v_msg2 = Twist()

        v_msg1.linear.x = 2  # Hyperparameter1
        v_msg1.linear.y = 0
        v_msg1.linear.z = 0
        v_msg1.angular.x = 0
        v_msg1.angular.y = 0
        v_msg1.angular.z = 0

        v_msg2.linear.x = 2  # HYperparameter 2
        v_msg2.linear.y = 0
        v_msg2.linear.z = 0
        v_msg2.angular.x = 0
        v_msg2.angular.y = 0
        v_msg2.angular.z = 0
        
        
        time.sleep(1)
        self.velocity1_publisher.publish(v_msg1)
        self.velocity2_publisher.publish(v_msg2)



        while not rospy.is_shutdown():
            d=self.euclidean_distance()
            
            # print(self.pose2.x,self.pose1.x,self.pose1.y,self.pose2.y,d)
            a1 = 40/pow(d,2)  #GM2/d^2
            a2 = 40/pow(d,2)  #GM1/d^2  #Magnitude only
            ang=self.angle()

            #update 1
            vx1 = v_msg1.linear.x*cos(self.pose1.theta)+a1*cos(ang)*0.01
            vy1 = v_msg1.linear.x*sin(self.pose1.theta)+a1*sin(ang)*0.01
            #update 2
            vx2 = v_msg2.linear.x*cos(self.pose2.theta)-a2*cos(ang)*0.01
            vy2 = v_msg2.linear.x*sin(self.pose2.theta)-a2*sin(ang)*0.01
                    
            v_msg1.linear.x=sqrt(pow(vx1,2)+pow(vy1,2))
            v_msg2.linear.x=sqrt(pow(vx2,2)+pow(vy2,2))

            # ANGULAR VELOCITY UPDATE
            ang1_update = atan2(vy1,vx1)
            ang2_update = atan2(vy2,vx2)

            v_msg1.angular.z = ((ang1_update-self.pose1.theta)%(2*pi))/0.01 # FEED delta theta1/delta t
            v_msg2.angular.z = ((ang2_update-self.pose2.theta)%(2*pi))/0.01 # FEED delta theta1/delta t
           
            
            # Publishing our vel_msg
            self.velocity1_publisher.publish(v_msg1)
            self.velocity2_publisher.publish(v_msg2)
            

            # Publish at the desired rate.
            self.rate.sleep()        

if __name__ == '__main__':
    try:
        x = TurtleBots()
        x.simulate_gravity()
    except rospy.ROSInterruptException:
        pass





       
    
    