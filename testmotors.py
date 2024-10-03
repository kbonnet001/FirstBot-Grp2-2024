import motors
import time
from go_to_without_odom import *

m = motors.Motors()

# m.move_forward_distance(0.5, 3) #1 m
# m.stop()

# m.rotate(1.5)
# m.stop()
# time.sleep(2)
# m.rotate_two_wheels(1.5)
# m.stop()

# test go_to
# go_to(m, 0.5, 0.14, 0.0, x_start = 0.0, y_start=0.0, theta_start=0.0)

go_to(m, -0.97, -0.55, 0.0, x_start = 0.0, y_start=0.0, theta_start=0.0)

#m.DXL_IO.close()