#include "ros/ros.h"
#include "std_msgs/String.h"
#include<bits/stdc++.h>
using namespace std;

 

/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
// %Tag(CALLBACK)%



void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  
  ROS_INFO("I heard: [%s]",msg->data.c_str());
  /**s.data=reverse((msg->data.c_str()).begin(),(msg->data.c_str()).end());*/
  string a=(msg->data.c_str());
  reverse(a.begin(),a.end());
  std_msgs::String s;
  s.data=a;
  ros::NodeHandle nu;
  ros::Publisher abhiyaan_pub = nu.advertise<std_msgs::String>("/naayihba_maet", 2);

    
  
  
  
  ros::Rate loop_rate(10);
 

  while (ros::ok())
  {
    abhiyaan_pub.publish(s);
    ros::spinOnce();
    loop_rate.sleep();
  }


}
// %EndTag(CALLBACK)%

int main(int argc, char **argv)
{
  ros::init(argc, argv, "node_reverse");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/team_abhiyaan", 1000, chatterCallback);
  ros::spin();
  
  
  
  return 0;

}
