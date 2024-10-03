import math
import motors
import time

r = 0.0256
L = 0.1284

def direct_kinematics(v_gauche, v_droit) : 
  """
  Compute linear and angular speeds of robot
  Takes as parameters wheel speeds (rad/s) and returns linear (m/s) 
  and angular (rad/s) speeds of the robot
  v = w * r
  - v is the linear velocity in meters per second (m/s),
  - r is the radius of the circular path in meters (m),
  - ω is the angular velocity in radians per second (rad/s).
  
  Args
  - v_gauche and v_droit : wheel speeds rad/s
  - r : radius (m)
  - L : distance between 2 wheels (m)
  
  Returns : 
  x_dot : linear speed (m/s)
  theta_dot : angular speed (rad/s)
  """
  x_dot = (r / 2) * (v_gauche + v_droit)
  theta_dot = (r / L) * (v_droit - v_gauche)

  return x_dot, theta_dot
    
def odom(x_dot, theta_dot, t_n_1, t_n) : 
  """
  Compute position x y and orientation of the robot
  Takes as parameters linear and angular speed of the robot, and returns
  the position (m) and orientation (rad) variation in the robot frame

  Args 
  x_dot : linear speed (m/s)
  theta_dot : angular speed (rad/s)
  dt : time (s)
  
  Returns
  dx : position axis x (m)
  dy : position axis y (m)
  d_teta : orientation (rad)
  """
  dt = t_n - t_n_1
  dx = x_dot * dt * math.cos(theta_dot * dt) # distance dx * angle
  dy = x_dot * dt * math.sin(theta_dot * dt)
  d_theta = theta_dot * dt
  
  return dx, dy, d_theta

def tick_odom(x_n_1, y_n_1, theta_n_1, t_n_1, x_dot, theta_dot, t_n) : 
  """ 
  Compute new position and orientation in the world frame (update)
  Takes as parameters the position and orientation of the robot in the world frame,
  the variation of the robot position and orientation in the robot frame, and returns 
  new position and orientation of the robot in the world frame
  
  Args 
  x_n_1 : position on x axis at t-1 (m)
  y_n_1 : position on y axis at t-1 (m)
  theta_n_1 : orientation at t-1 (rad)
  x_dot : linear speed (m/s)
  theta_dot : angular speed (rad/s)
  dt : time (s)
  
  Returns 
  - x_world : position on x axis at t in world frame (m)
  - y_world : position on y axis at t in world frame (m)
  - theta_world : orientation at t in world frame (rad)
  """
  # Compute variations of positions and orientation 
  dx_relatif, dy_relatif, theta_relatif = odom(x_dot, theta_dot, t_n_1, t_n)
  
  # Update orientation
  # Last orientation in world frame (n-1) + variation 
  theta_world = theta_n_1 + theta_relatif
  
  dx_world, dy_world = fonction_de_transfert(dx_relatif, dy_relatif, theta_world)
  
  # Update position in world frame
  # Last position in world frame (n-1) + variation 
  x_world = x_n_1 + dx_world
  y_world = y_n_1 + dy_world
  
  return x_world, y_world, theta_world

######################################

def inverse_kinematic(x_dot, theta_dot) :
  """
  Compute wheels left and right speeds

  Args
  x_dot : linear speed (m/s)
  teta_dot : angular speed (rad/s)

  Returns
  v_gauche, v_droite : angular target speed of wheels (rad/s)
  """
  v_droite = theta_dot * (L/2) + x_dot #merci de laisser 2 voir test.py :)
  v_gauche = x_dot - (L/2) * theta_dot

  return v_gauche/r, v_droite/r

"""def calculate_theta_line_cam(sampling_h1, sampling_1_center, sampling_h2, sampling_2_center, h, center_x):
  
  tolerance_theta = 0.05

  delta_center_1 = sampling_1_center - center_x

  if(abs(delta_center_1) > tolerance_theta):
    

  delta_sampling_h = sampling_h2 - sampling_h1
  delta_sampling_center = abs(sampling_2_center - sampling_1_center)
  
  theta_line = math.atan(delta_sampling_center/delta_sampling_h)
  
  return theta_line

def turn_with_line(m, theta_line):
  
  tolerance_theta = 0.05
  
  #angle_line = abs(180 / math.pi * theta_line)
  
  #t = 2/(3*angle_line)
  #theta_speed = math.pi*2
  
  if theta_line < -tolerance_theta:
    #m.turn_right(angle_line/t, t)
    #t = theta_line / theta_speed
    #m.turn_right(theta_speed, t)
    m.rotate_two_wheels(theta_line)
  elif theta_line > tolerance_theta:
    #m.turn_left(angle_line/t, t)
    #t = theta_line / theta_speed
    #m.turn_left(theta_speed, t)    
    m.rotate_two_wheels(theta_line)
  else :
        #m.go_forward()
    m.move_forward_distance(0.04)"""
    
def fonction_de_transfert(x_relatif, y_relatif, theta):
  #theta correspond au nouveau theta
  """Robot frame to world frame """
  
  x = x_relatif * math.cos(theta) - y_relatif * math.sin(theta)
  y = x_relatif * math.sin(theta) - y_relatif * math.cos(theta)
  return x, y