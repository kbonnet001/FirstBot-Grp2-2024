import math
from tools import *
from motors import *
from Timer import *
  
def go_to(m, x_target, y_target, theta_target, x_start = 0.0, y_start=0.0, theta_start=0.0, speed = 3.0):
  """
  Guide the robot to a given position (x_target, y_target) and orientation (theta_target).
  Monitors the real wheel speeds and computes the real position and orientation.
  1) Adjust the orientation 
  2) Go to the position x y 
  3) Adjust the orientation
  
  Boucle while to check with current odometry informations from motors
  
  Args:
  - m (Motors) : Motors
  - x_target, y_target (m) : Coordinates of the target position 
  - theta_target (rad) : Target orientation 
  - x_start, y_start (m) : Coordinates of the start position (default 0.0)
  - theta_target (rad) : Start orientation  (default 0.0)
  - speed (rad/s) : default 3.0
  
  Returns:
  - Updated real position and orientation of the robot
  """

  # Compute the distance and angle to the target
  distance_to_target = math.sqrt((x_target - x_start)**2 + (y_target - y_start)**2)
  angle_to_target = math.atan2(y_target - y_start, x_target - x_start)
  
  # 1) Ajust orientation
  # Compute angle
  turn_angle = angle_to_target - theta_start
  m.rotate_two_wheels(turn_angle, speed)
  time.sleep(1)
  
  # 2) Go to the point xy
  m.move_forward_distance(distance_to_target, speed)
  time.sleep(1)
  
  # 3) Ajust orientation 
  final_turn = theta_target - angle_to_target
  m.rotate_two_wheels(final_turn, speed)
  time.sleep(1)
  
  # Stop motors and close communication
  m.stop()
  m.DXL_IO.close()