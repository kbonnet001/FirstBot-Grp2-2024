from motors import *
import time
from tools import *

def odometry(m, x_real = 0.0, y_real = 0.0, theta_real = 0.0) :
  
  while True : 
    # Retrieve real speeds from motors (simulated by get_current_speed())
    v_gauche_motor, v_droit_motor = m.get_current_speed_wheels() 
    
    x_dot_real, theta_dot_real = direct_kinematics(v_gauche_motor, v_droit_motor) # real
    
    t_n = time.time()
    x_real, y_real, theta_real, t_n_1 = tick_odom(x_real, y_real, theta_real, t_n_1, x_dot_real, theta_dot_real, t_n) # real 
    
    if "touche n'importe laquelle est pressée" : 
      print(f"Fin de l'odometrie : \n x = {x_real}, y = {y_real}, theta = {theta_real}")
      break
    
    
  return 