import pypot.dynamixel
import time
import math

ROTATION_SPEED = 360

class Motors():
    PORTS = pypot.dynamixel.get_available_ports()
    port = PORTS[0]
    DXL_IO =  pypot.dynamixel.DxlIO(port)
    found_ids  =  DXL_IO.scan(range(5))
    ids = found_ids[:2]
    DXL_IO.enable_torque(ids)

    DXL_IO.set_wheel_mode([1])
    DXL_IO.set_wheel_mode([2])


# def initMotors():
#   ports = pypot.dynamixel.get_available_ports()
#   if not ports:
#       raise IOError('no port found!')

#   port = ports[0]
#   print(port)
#   dxl_io = pypot.dynamixel.DxlIO(port)

#   found_ids  =  dxl_io.scan(range(5))
#   print(found_ids )

#   if len(found_ids) < 2:
#           raise IOError('You should connect at least two motors on the bus for this test.')

#   ids = found_ids[:2]
#   dxl_io.enable_torque(ids)

#   dxl_io.set_wheel_mode([1])
#   dxl_io.set_wheel_mode([2])

def go_forward(m):
    """ Go forward"""
    m.DXL_IO.set_moving_speed({1: -ROTATION_SPEED})
    m.DXL_IO.set_moving_speed({2: ROTATION_SPEED})

def stop(m):
    m.DXL_IO.set_moving_speed({1: 0})
    m.DXL_IO.set_moving_speed({2: 0})
    
# Turn
def turn_left(m, l, t):
    """ 
    Slow down left wheel for l seconds
    
    Args :
    l = degrees/s
    t = time in seconds
    
    """
    m.DXL_IO.set_moving_speed({2: l})
    t0 = time.time()
    while True:
        t1 = time.time()
        if (t1 - t0) > t:
            break
    go_forward(m)

def turn_right(m, r, t):
    """
    Slow down right wheel for l seconds
    Args :
    r = degrees/s
    t = time in seconds
    """
    m.DXL_IO.set_moving_speed({1: -r})
    t0 = time.time()
    while True:
        t1 = time.time()
        if (t1 - t0) > t:
            break
    go_forward(m)

def get_wheel_info(m):
    
    print("---")
    # current angular position motors
    positions = m.DXL_IO.get_present_position([1, 2])
    print(f"Position des moteurs: {positions}")

    # current speed of motors
    speeds = m.DXL_IO.get_present_speed([1, 2])
    print(f"Vitesse des moteurs: {speeds}")

    # current temp of motors
    temperatures = m.DXL_IO.get_present_temperature([1, 2])
    print(f"Température des moteurs: {temperatures}")

    # current vol of motors
    voltages = m.DXL_IO.get_present_voltage([1, 2])
    print(f"Voltage des moteurs: {voltages}")
###

def get_current_speed_wheels(m) : 
    """ 
    Get the current speed of wheels

    Returns : 
    - v_gauche and v_droit : wheel speeds (rad/s)
    """
    return m.DXL_IO.get_present_speed([1, 2])


###############################################
def spin_wheels(m, v_gauche, v_droite):
    """ Spin wheels with given values 
    To stop the robot, choose 0 for each wheels

    Args:
    - v_gauche and v_droit : wheel speeds rad/s
    
    """
    vd = math.degrees(v_droite)
    vg = math.degrees(v_gauche) # --> deg/s
    
    m.DXL_IO.set_moving_speed({1: -vd})
    m.DXL_IO.set_moving_speed({2: vg})


# def function(theta, K_theta = 2.0) : 
    
#     x_dot = 0  # No forward movement
#     theta_dot = K_theta * theta 
#     v_gauche, v_droit = inverse_kinematic(x_dot, theta_dot)
#     spin_wheels(v_gauche, v_droit)

# spin_wheels(3.14, 0)
# time.sleep(3)
motors = Motors()

stop(motors)