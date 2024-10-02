import pypot.dynamixel

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



dxl_io.close()