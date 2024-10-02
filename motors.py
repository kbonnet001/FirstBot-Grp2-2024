import pypot.dynamixel
import time

MOVE_SPEED = 360

def go_forward():
    dxl_io.set_moving_speed({1: MOVE_SPEED})
    dxl_io.set_moving_speed({2: -MOVE_SPEED})

def stop():
    dxl_io.set_moving_speed({1: 0})
    dxl_io.set_moving_speed({2: 0})
     
def turn_left(l, t):
    dxl_io.set_moving_speed({2: -l})
    t0 = time.time()
    while True:
        t1 = time.time()
        if (t1 - t0) > t:
            break
    go_forward()

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

go_forward()
time.sleep(1)
turn_left(100, 1)
time.sleep(1)
turn_right(100, 1)
time.sleep(1)
stop()

dxl_io.close()