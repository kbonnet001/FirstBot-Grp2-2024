import pypot.dynamixel
import time

ROTATION_SPEED = 360

def go_forward():
    dxl_io.set_moving_speed({1: ROTATION_SPEED})
    dxl_io.set_moving_speed({2: -ROTATION_SPEED})

def stop():
    dxl_io.set_moving_speed({1: 0})
    dxl_io.set_moving_speed({2: 0})

"""
Slow down left wheel for l seconds
Args :
l = degrees/s
t = time in seconds
"""
def turn_left(l, t):
    dxl_io.set_moving_speed({2: -l})
    t0 = time.time()
    while True:
        t1 = time.time()
        if (t1 - t0) > t:
            break
    go_forward()

"""
Slow down right wheel for l seconds
Args :
r = degrees/s
t = time in seconds
"""
def turn_right(r, t):
    dxl_io.set_moving_speed({1: r})
    t0 = time.time()
    while True:
        t1 = time.time()
        if (t1 - t0) > t:
            break
    go_forward()

ports = pypot.dynamixel.get_available_ports()
if not ports:
    raise IOError('no port found!')

port = ports[0]
print(port)
dxl_io = pypot.dynamixel.DxlIO(port)

found_ids  =  dxl_io.scan(range(5))
print(found_ids )

if len(found_ids) < 2:
        raise IOError('You should connect at least two motors on the bus for this test.')

ids = found_ids[:2]
dxl_io.enable_torque(ids)

dxl_io.set_wheel_mode([1])
dxl_io.set_wheel_mode([2])

###
def get_wheel_info():
    # current angular position motors
    positions = dxl_io.get_present_position([1, 2])
    print(f"Position des moteurs: {positions}")

    # current speed of motors
    speeds = dxl_io.get_present_speed([1, 2])
    print(f"Vitesse des moteurs: {speeds}")

    # current temp of motors
    temperatures = dxl_io.get_present_temperature([1, 2])
    print(f"Température des moteurs: {temperatures}")

    # current vol of motors
    voltages = dxl_io.get_present_voltage([1, 2])
    print(f"Voltage des moteurs: {voltages}")
###

get_wheel_info() #ici
go_forward()
time.sleep(10)
get_wheel_info() #ici
stop()

dxl_io.close()




# # Read servo position.
# try:
#     while True:
#         (position, result, error_code) = servo.read2ByteTxRx(port, DXL_ID, ADDR_PRESENT_POSITION)
#         if result != COMM_SUCCESS:
#             error_message = servo.getRxPacketError(error_code)
#             print(f'Error reading servo position: "{error_message}"')
#             break

#         print(position)
# except KeyboardInterrupt:
#     pass


