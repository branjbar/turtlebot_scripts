#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import random as RD
import math

global robot_name, mode

MAX_LINEAR_SPEED = .2
MAX_ANGULAR_SPEED =  1.2
mode = "STRAIGHT"

def get_laser(msg):
	global mode
	MIN_DISTANCE = 1 # obstacle avoidance distance
	
	scan = msg.ranges # a list of all scanned ranges
	HALF_RANGE = len(scan) / 2  # half of the laser resolution

        modified_scan = []
        for i in scan:
                if math.isnan(i):
                        modified_scan.append(10)
                else:
                        modified_scan.append(i)

	scan = modified_scan
	closest = min(scan[HALF_RANGE / 3 : 5 * HALF_RANGE / 3]) # distance to the closest obstacle
	

	sum_of_left_beams = sum(scan[HALF_RANGE:])
	sum_of_right_beams = sum(scan[:HALF_RANGE])

	if closest > MIN_DISTANCE: # if there is no obstacle near by
 		mode = "STRAIGHT"
	else:
		if mode == "STRAIGHT": 
			if sum_of_left_beams < sum_of_right_beams: # if there is an obstacle, check which side there are less obstacles 
				mode = "TURN CCW"
			else:
				mode = "TURN CW"
				 
	#print sum(scan[:HALF_RANGE]), sum(scan[HALF_RANGE:])			
	#print sum_of_left_beams < sum_of_right_beams, mode
	talker(mode)
    
    
def listener():
    rospy.init_node('listener',anonymous=True)
    rospy.Subscriber("/scan", LaserScan, get_laser)
    rospy.spin()

def set_twist(x,z):
	twist = Twist()
	twist.linear.x = x  # our forward speed
	twist.linear.y = 0 
	twist.linear.z = 0 # we can't use these!        
 	
	twist.angular.x = 0 
	twist.angular.y = 0   
	twist.angular.z = z # rotate CCW
	
	return twist

def talker(mode):
    	pub = rospy.Publisher('/mobile_base/commands/velocity',Twist)
	
	if mode == "STRAIGHT":
		twist = set_twist(MAX_LINEAR_SPEED,0)
	if mode == "TURN CCW":
		twist = set_twist(MAX_LINEAR_SPEED / 10, MAX_ANGULAR_SPEED)	
	if mode == "TURN CW":
		twist = set_twist(MAX_LINEAR_SPEED / 10, -1 * MAX_ANGULAR_SPEED)
	
	pub.publish(twist)

if __name__ == '__main__':
	global robot_name	
	import sys
#	try:
#	robot_name = sys.argv[1]
#	except:
#	print 'ERROR: no robot_name provided, try: \n$$ python stdr_random_walk.py robot[XX] '
#		exit()
	
#	print robot_name, ' started to walk randomly.'   	
	listener()	
	
