import motors
import time
from go_to_without_odom import *
from odometry import *

m = motors.Motors()

#2) GO TO (without odom)
# x + forward | y - back
# y + left | y - right
# 90 rad = 1,5708 rad tourne vers la gauche (+ = gauche et - = droite)
# 180 rad = 3,14159 deg

# x_to_go = 1.0
# y_to_go = - 1.0
# angle_to_go = math.pi
# go_to(m, x_to_go, y_to_go, angle_to_go, x_start = 0.0, y_start=0.0, theta_start=0.0, speed_rot = 3.0, speed_go = 5.0) #ok

#3) ODOMETRY
odometry(m)

#################################################################

# m.move_forward_distance(0.5, 3) #1 m
# m.stop()

# m.rotate(1.5) #90 deg
# m.stop()
# time.sleep(2)
# m.rotate_two_wheels(1.5) #90 deg
# m.stop()

# test go_to
#go_to(m, 0.5, 0.5, 0.0, x_start = 0.0, y_start=0.0, theta_start=0.0) #ok

# go_to(m, -0.97, -0.55, 0.0, x_start = 0.0, y_start=0.0, theta_start=0.0) #ok

# t0 = time.time()

# m.passive_wheels() # go to passive mode
# while True : 
#   v_droit_motor, v_gauche_motor = m.get_current_speed_wheels() # à tester si bonnes roues
#   print("v_gauche_motor = ", v_gauche_motor, "v_droit_motor = ",v_droit_motor)
#   time.sleep(0.1)
#   if (time.time() - t0 > 10) :
#     break

# m.DXL_IO.close()

###########################################################################

