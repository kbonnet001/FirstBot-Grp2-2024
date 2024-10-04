import math
from tools import *
from motors import *
from Timer import *
  
def go_to(m, x_target, y_target, theta_target, x_start = 0.0, y_start=0.0, theta_start=0.0, speed_rot = 3.0, speed_go = 3.0):
  """
  Guide the robot to a given position (x_target, y_target) and orientation (theta_target).
  Monitors the real wheel speeds and computes the real position and orientation.
  1) Adjust the orientation 
  2) Go to the position x y 
  3) Adjust the orientation
  
  x + forward | y - back
  y + left | y - right
  
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
  print("distance_to_target = ", distance_to_target)
  print("angle_to_target = ", angle_to_target)
  
  # 1) Ajust orientation
  # Compute angle
  turn_angle = angle_to_target - theta_start
  time_go_to = m.rotate_two_wheels_go_to(turn_angle, speed_rot)
  print("1", time_go_to)
  time.sleep(time_go_to)
  m.stop()
  
  # 2) Go to the point xy
  time_go_to = m.move_forward_distance_go_to(distance_to_target, speed_go)
  print("2", time_go_to)
  time.sleep(time_go_to)
  m.stop()
  
  # 3) Ajust orientation 
  final_turn = theta_target - angle_to_target
  print("final_turn = ", final_turn)
  time_go_to = m.rotate_two_wheels_go_to(final_turn, speed_rot)
  print("3", time_go_to)
  time.sleep(time_go_to)
  m.stop()
  
  # Stop motors and close communication
  m.stop()
  m.DXL_IO.close()