from motors import *
import time
from tools import *
from plot import *

def odometry(m, x_n = 0.0, y_n = 0.0, theta_n = 0.0) :
  """ Robot will be moved (using "passive wheels" mode) on the round.
  After some time, you will indicate where the robot is located relative 
  to its initial position (x, y, theta), using only the motor encoders.

  Args : 
  - m (Motors) : motors
  - x_n, y_n (m) : start position (default origin 0.0)
  - theta_n (rad) : start orientation (defaut 0.0)
  """ 
  list_x = [x_n]
  list_y = [y_n]
  list_theta = [theta_n]
  list_vg = [0.0]
  list_vd = [0.0]
  list_t = [0.0]
  
  m.passive_wheels() # go to passive mode
  t_n = time.time()
  
  t0 = time.time()
  while True : 
    print("---")
    x_n_1 = x_n
    y_n_1 = y_n
    theta_n_1 = theta_n
    t_n_1 = t_n
    
    # Retrieve real speeds from motors (simulated by get_current_speed())
    v_droit_motor, v_gauche_motor = m.get_current_speed_wheels() # à tester si bonnes roues
    print("v_droit_motor = ", v_droit_motor, " v_gauche_motor = ", v_gauche_motor)
    
    x_dot_real, theta_dot_real = direct_kinematics(v_gauche_motor, - v_droit_motor) # real droit - car dans l'autre sens
    print("x_dot_real = ", x_dot_real, " theta_dot_real = ", theta_dot_real)
    
    t_n = time.time()
    print("tn - 1= ", t_n_1, " tn = ", t_n)
    x_n, y_n, theta_n = tick_odom(x_n_1, y_n_1, theta_n_1, t_n_1, x_dot_real, theta_dot_real, t_n) # real 
    print(f"x = {x_n}, y = {y_n}, theta = {theta_n}")
    
    # append
    list_x.append(x_n)
    list_y.append(y_n)
    list_theta.append(theta_n)
    list_vg.append(v_gauche_motor)
    list_vd.append(-v_droit_motor)
    list_t.append(t_n)
    
    if(time.time()-t0>15):
      print(f"Fin de l'odometrie : \n x = {x_n}, y = {y_n}, theta = {theta_n}")
      m.DXL_IO.close()
      print(list_x[0:10], len(list_x))
      print(list_y[0:10], len(list_y))
      print(list_theta[0:10], len(list_theta))
      print(list_vg[0:10], len(list_vg))
      print(list_vd[0:10], len(list_vd))
      print(list_t[0:10], len(list_t))
      plot_position_orientation_comparaison(list_x, list_y, list_theta, list_vg, list_vd, list_t)
      break
      
