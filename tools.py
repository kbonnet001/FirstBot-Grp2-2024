import math

r = 0.0256
L = 0.1

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
    
def odom(x_dot, theta_dot, dt) : 
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
  dx = x_dot * dt * math.cos(theta_dot) # distance dx * angle
  dy = x_dot * dt * math.sin(theta_dot)
  d_theta = theta_dot * dt
  
  return dx, dy, d_theta

def tick_odom(x_n_1, y_n_1, theta_n_1, x_dot, theta_dot, dt) : 
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
  - x_n : position on x axis at t in world frame (m)
  - y_n : position on y axis at t in world frame (m)
  - theta_n : orientation at t in world frame (rad)
  """
  # Compute variations of positions and orientation 
  dx_global, dy_global, theta_global = odom(x_dot, theta_dot, dt)
  
  # Update position in world frame
  # Last position in world frame (n-1) + variation 
  x_n = x_n_1 + dx_global
  y_n = y_n_1 + dy_global
  
  # Update orientation
  # Last orientation in world frame (n-1) + variation 
  theta_n = theta_n_1 + theta_global
  
  return x_n, y_n, theta_n


######################################

def inverse_kinematic(x_dot, teta_dot) :
  """
  Compute wheels left and right speeds

  Args
  x_dot : linear speed (m/s)
  teta_dot : angular speed (rad/s)

  Returns
  v_gauche, v_droite : angular target speed of wheels
  """
  v_gauche = teta_dot * (L/4) + x_dot
  v_droite = x_dot - (L/4) * teta_dot

  return v_gauche, v_droite