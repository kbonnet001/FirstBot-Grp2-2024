
radius = 0,256

def direct_kinematics(v_gauche, v_droit) : 
  """
  Compute linear and angular speeds of robot
  v = w * r
  -  v is the linear velocity in meters per second (m/s),
  - r is the radius of the circular path in meters (m),
  -  ω is the angular velocity in radians per second (rad/s).
  
  Args
  - v_gauche and v_droit : wheel speeds rad/s
  
  Returns : 
  x_dot, teta_dot"""
  
  teta_dot = (v_gauche + v_droit) / 2
  x_dot = teta_dot * radius
    
  return x_dot, teta_dot
    
def odom(x_dot, teta_dot, dt) : 
  """
  dx, dy, d_teta
  Takes as parameters linear and angular speed of the robot, and returns the position (m) and orientation (rad) variation in the robot frame

  """
  
  

  
  