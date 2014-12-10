import direction_handler
import roslib
import rospy
from ir_converter.msg import Distance
from navigation_msgs.srv import *
from navigation_msgs.msg import *
from direction_handler import *

SIDE_BLOCKED_THRESHOLD = 0.35
FRONT_BLOCKED_THRESHOLD = 0.25
ROBOT_DIAMETER = 0.25
fit_blob_service = None

compass_direction = Node.EAST
distance = Distance()

class ObstacleHandler:

    rospy.wait_for_service('/mapping/fitblob')
    fit_blob_service = rospy.ServiceProxy('/mapping/fitblob', navigation_msgs.srv.FitBlob)

    @staticmethod
    def map_dir_blocked(map_dir):
    	return ObstacleHandler.robot_dir_blocked(map_to_robot_dir(map_dir, compass_direction))

    @staticmethod
    def robot_dir_blocked(robot_dir):
        if robot_dir == RobotDirections.LEFT:
            return not ObstacleHandler.can_turn_left()
        if robot_dir == RobotDirections.RIGHT:
            return not ObstacleHandler.can_turn_right()
        if robot_dir == RobotDirections.FORWARD:
            return ObstacleHandler.obstacle_ahead()
        if robot_dir == RobotDirections.BACKWARD:
            return ObstacleHandler.obstacle_behind()
    
    @staticmethod
    def north_blocked():
        return ObstacleHandler.map_dir_blocked(Node.NORTH)

    @staticmethod
    def west_blocked():
        return ObstacleHandler.map_dir_blocked(Node.WEST)

    @staticmethod
    def south_blocked():
        return ObstacleHandler.map_dir_blocked(Node.SOUTH)

    @staticmethod
    def east_blocked():
        return ObstacleHandler.map_dir_blocked(Node.EAST)

    @staticmethod
    def can_turn_left():
        return True if distance.fl_side > SIDE_BLOCKED_THRESHOLD and distance.bl_side > SIDE_BLOCKED_THRESHOLD else False

    @staticmethod
    def can_turn_right():
        return True if distance.fr_side > SIDE_BLOCKED_THRESHOLD and distance.br_side > SIDE_BLOCKED_THRESHOLD else False

    @staticmethod
    def obstacle_ahead():
        return True if distance.l_front < FRONT_BLOCKED_THRESHOLD or distance.r_front < FRONT_BLOCKED_THRESHOLD else False

    @staticmethod
    def obstacle_behind():
        response = fit_blob_service.call(FitBlobRequest("robot", -ROBOT_DIAMETER+0.03, 0.0, 0.08, 0.05))
        return not response.fits

        
    	