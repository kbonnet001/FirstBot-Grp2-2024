from motors import *
import time
from tools import *
from plot import *
from SkyviewMap import SkyviewMap

def odometry(m, x_n = 0.0, y_n = 0.0, theta_n = 0.0, width = 600, height = 600, scale = 300, name_map="odometry_map") :
  """ Robot will be moved (using "passive wheels" mode) on the round.
  After some time, you will indicate where the robot is located relative 
  to its initial position (x, y, theta), using only the motor encoders.

  Args : 
  - m (Motors) : motors
  - x_n, y_n (m) : start position (default origin 0.0)
  - theta_n (rad) : start orientation (defaut 0.0)
  
  for skyview map : 
  width (pixel) : width of image (default 600)
  height (pixel) : height of image (default 600)
  name_map (str) : name for the saved image 
  """ 
  # Preparation of lists for plot
  list_x = [x_n]
  list_y = [y_n]
  list_theta = [theta_n]
  list_vg = [0.0]
  list_vd = [0.0]
  list_t = [0.0]
  last_time = time.time()  # horodotage initialisation
  
  # Prepare map
  map = SkyviewMap(width, height, scale, name_map)

  m.passive_wheels() # go to passive mode
  t_n = time.time()
  
  try:
    while True : 
      print("---")
      x_n_1 = x_n
      y_n_1 = y_n
      theta_n_1 = theta_n
      t_n_1 = t_n
      
      # Retrieve real speeds from motors (simulated by get_current_speed())
      v_droit_motor, v_gauche_motor = m.get_current_speed_wheels()
      x_n, y_n, theta_n, t_n = m.compute_position_orientation(v_droit_motor, v_gauche_motor, x_n_1, y_n_1, theta_n_1, t_n_1)
      
      # print("v_droit_motor = ", v_droit_motor, " v_gauche_motor = ", v_gauche_motor)
      
      # x_dot_real, theta_dot_real = direct_kinematics(v_gauche_motor, - v_droit_motor) # real droit - car dans l'autre sens
      # print("x_dot_real = ", x_dot_real, " theta_dot_real = ", theta_dot_real)
      
      # t_n = time.time()
      # print("tn - 1= ", t_n_1, " tn = ", t_n)
      # x_n, y_n, theta_n = tick_odom(x_n_1, y_n_1, theta_n_1, t_n_1, x_dot_real, theta_dot_real, t_n) # real 
      # print(f"x = {x_n}, y = {y_n}, theta = {theta_n}")
      
      if t_n - last_time >= 0.5 : #every second
        
        # Add line on map
        map.trace_position_on_map((list_x[-1], list_y[-1]), (x_n, y_n))
        
        # append
        list_x.append(x_n)
        list_y.append(y_n)
        list_theta.append(theta_n%(2*math.pi))
        list_vg.append(v_gauche_motor)
        list_vd.append(-v_droit_motor)
        list_t.append(list_t[-1] + t_n - t_n_1)
        
        last_time = t_n
  
  except KeyboardInterrupt:   
    m.DXL_IO.close()
    print(f"Fin de l'odometrie : \n x = {x_n}, y = {y_n}, theta = {theta_n%(2*math.pi)}")
    plot_position_orientation_comparaison(list_x, list_y, list_theta, list_vg, list_vd, list_t, "odometry_plot")
    map.display_and_save_map()
