import time
import matplotlib as plt
import matplotlib.pyplot as plt
from Timer import *

def wait_3_s() : 
  ts, speeds = step_to_go()

def step_to_go() : 
  ts = []
  speeds = []
  for k in range(3) : 
    time.sleep(1)
    ts.append(k)
    speeds.append(2*k)
  return speeds, ts
    
    
def plot_speed(speed, time) : 
  plt.figure(figsize=(10, 5))
  plt.plot(time, speed, marker='o')
  plt.xlabel("Time (s)")
  plt.ylabel("Speed ")
  plt.title(f"Evolution of speed as function of time", fontweight='bold')
  plt.legend()
  plt.show()  # Display the plot


# with measure_time() as timer:
#   wait_3_s()
# print(f"Time execution: {timer.execution_time:.6f} seconds")

################
# re le soir

import matplotlib.pyplot as plt

# Exemple 
list_x = [1, 2, 3]
list_y = [1, 2, 3]
list_theta = [1, 2, 3]
list_vg = [1, 2, 3]
list_vd = [1, 2, 3]
list_dt = [0.0, 1.0, 2.0]

def plot_position_orientation_comparaison(list_x, list_y, list_theta, list_vg, list_vd, list_dt) :
  
  # x_n, x_real = zip(*list_x)
  # y_n, y_real = zip(*list_y)
  # theta_n, theta_real = zip(*list_theta)
  # vg_n, vg_real = zip(*list_vg)
  # vd_n, vd_real = zip(*list_vd)

  fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 10))
  fig.delaxes(ax6)

  # list_x
  ax1.plot(list_dt, list_x, marker='o', label='x_n', markersize=2)
  ax1.set_title('Position x')
  ax1.set_xlabel('Position x (m)', fontsize='smaller')
  ax1.set_ylabel('Time (s)', fontsize='smaller')
  ax1.legend()

  # list_y
  ax2.plot(list_dt, list_y, marker='o', label='y_n', markersize=2)
  ax2.set_title('Position y comparaison')
  ax2.set_xlabel('Position y (m)', fontsize='smaller')
  ax2.set_ylabel('Time (s)', fontsize='smaller')
  ax2.legend()

  # list_theta
  ax3.plot(list_dt, list_theta, marker='o', label='theta_n', markersize=2)
  ax3.set_title('Orientation theta comparaison')
  ax3.set_xlabel('Orientation theta (rad)', fontsize='smaller')
  ax3.set_ylabel('Time (s)', fontsize='smaller')
  ax3.legend()
  
  # list_vg
  ax4.plot(list_dt, list_vg, marker='o', label='vg_n', markersize=2)
  ax4.set_title('Speed left wheel comparaison')
  ax4.set_xlabel('Speed left wheel (rad)', fontsize='smaller')
  ax4.set_ylabel('Time (s)', fontsize='smaller')
  ax4.legend()
  
  # list_vd
  ax5.plot(list_dt, list_vd, marker='o', label='vd_n', markersize=2)
  ax5.set_title('Speed right wheel comparaison')
  ax5.set_xlabel('Speed right wheel (rad)', fontsize='smaller')
  ax5.set_ylabel('Time (s)', fontsize='smaller')
  ax5.legend()

  fig.suptitle(f"Theorical and real values of position and orientation", fontweight='bold')
  plt.tight_layout()
  plt.show() #show plot
  # file_path = os.path.join(directory_path, file_name)
  plt.savefig('./plot_position_orientation.jpg') 

# test
plot_position_orientation_comparaison(list_x, list_y, list_theta, list_vg, list_vd, list_dt)