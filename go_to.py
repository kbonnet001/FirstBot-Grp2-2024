import math
from tools import *
from motors import *
from Timer import *
from plot import plot_position_orientation_comparaison

# C'est le chantier ahhhhhhhhhhhhhh

def go_to(m, x_target, y_target, theta_target, x_start = 0.0, y_start=0.0, theta_start=0.0, 
          K_v = 2.0 , K_theta = 2.0):
  """
  /!\ les K ne sont pas définis, à choisir !!!!!!!!!!!!!!!!!!!!!!!!!!
  
  Guide the robot to a given position (x_target, y_target) and orientation (theta_target).
  Monitors the real wheel speeds and computes the real position and orientation.
  1) Adjust the orientation 
  2) Go to the position x y 
  3) Adjust the orientation
  
  Boucle while to check with current odometry informations from motors
  
  Args:
  - x_target, y_target: Coordinates of the target position (m)
  - theta_target: Target orientation (rad)
  - dt: Time interval (s)
  - x_start, y_start, theta_start: Initial position and orientation (rad)
    (default 0.0)
  
  Returns:
  - Updated real position and orientation of the robot
  """
  motors = Motors()

  # Initial position and orientation
  x_n, y_n, theta_n = x_start, y_start, theta_start

  # Real position and orientation (tracked based on real motor speeds)
  x_real, y_real, theta_real = x_start, y_start, theta_start
  
  # Time initialisation
  t1 = time.time()
  
  # Tolerance for reaching the target
  tolerance_pos = 0.01  # 1 cm tolerance for position
  tolerance_theta = 0.1  # 0.1 rad tolerance for orientation
  
  # (optionnal) save theorical and real values of position and orientation
  list_x = []
  list_y = []
  list_theta = []
  list_vg = []
  list_vd = []
  list_dt = []

  while True:
    print("---")
    # Compute the distance and angle to the target
    
    x_n = x_real
    y_n = y_real
    theta_n = theta_real
    print("début", "x_n", x_n, "y_n = ", y_n, "theta_n = ", theta_n)
    
    distance_to_target = math.sqrt((x_target - x_n)**2 + (y_target - y_n)**2)
    print("distance to target = ", distance_to_target)
    
    angle_to_target = math.atan2(y_target - y_n, x_target - x_n)
    print("angle to target = ", angle_to_target)
    
    # Compute errors
    error_angle = angle_to_target - theta_n
    print("error angle = ", error_angle)
    
    # If within tolerance, stop the robot, it's finish :)
    if distance_to_target < tolerance_pos and abs(theta_n - theta_target) < tolerance_theta:
      m.stop()
      break

    # Calculate x_dot and theta_dot
    if abs(error_angle) > tolerance_theta: # if the orientation isn't correct
      # Rotation needed
      print("rotation")
      x_dot = 0  # No forward movement
      theta_dot = K_theta * error_angle  # Angular velocity proportional to the error
        
    else: # orientation is correct, let's go !
      print("avancer")
      # Moving straight to the target
      x_dot = K_v * distance_to_target  # Linear velocity proposrtional to the distance
      theta_dot = 0  # No angular velocity needed, already oriented correctly
      
    # Use inverse kinematics to get wheel speeds
    v_gauche, v_droit = inverse_kinematic(x_dot, theta_dot)
    print("vg = ", v_gauche) # si les deux positifs alors ça tourne, et un + un - alors ça avance
    print("vd =", v_droit)
    m.spin_wheels(motors, v_gauche, v_droit)
    
    # Retrieve real speeds from motors (simulated by get_current_speed())
    v_gauche_motor, v_droit_motor = m.get_current_speed_wheels() 
    
    x_dot, theta_dot = direct_kinematics(v_gauche, v_droit) # theorie
    x_dot_real, theta_dot_real = direct_kinematics(v_gauche_motor, v_droit_motor) # real
    
    t0 = t1
    t1 = time.time()
    dt = t1 - t0
    x_n, y_n, theta_n = tick_odom(x_n, y_n, theta_n, x_dot, theta_dot, dt) # theorie
    print("x_n", x_n, "y_n = ", y_n, "theta_n = ", theta_n)
    x_real, y_real, theta_real = tick_odom(x_real, y_real, theta_real, x_dot_real, theta_dot_real, dt) # real 
    print("x_real", x_real, "y_real = ", y_real, "theta_real = ", theta_real)
    
    # print(f"Real: x={x_real:.3f}, y={y_real:.3f}, theta={theta_real:.3f}")
    # print(f"Target: x={x_n:.3f}, y={y_n:.3f}, theta={theta_n:.3f}")
    #################################################################################
    # attention à la fréquence du while, peut être un peu vener...
    # faudrait pas que ça devienne trop lourd pour la ptite carte '^'
    
    # list_x.append([x_n, x_real])
    # list_y.append([y_n, y_real])
    # list_theta.append([theta_n, theta_real])
    # list_vg.append([v_gauche, v_gauche_motor])
    # list_vd.append([v_droit, v_droit_motor])
    # list_dt.append(dt)

  return list_x, list_y, list_theta, list_vg, list_vd, list_dt

with measure_time() as timer:
  list_x, list_y, list_theta, list_vg, list_vd, list_dt = go_to(1.0, 1.0, 1.0, x_start = 0.0, 
                                                                y_start=0.0, theta_start=0.0, 
                                                                K_v = 1.0 , K_theta = 2.0)
  plot_position_orientation_comparaison(list_x, list_y, list_theta, list_vg, list_vd, list_dt)
  
print(f"Time execution: {timer.execution_time:.6f} seconds")