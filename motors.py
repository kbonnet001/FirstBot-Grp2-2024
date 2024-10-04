import pypot.dynamixel
import time
import math
import tools

r = 0.0256
L = 0.1284
ROTATION_SPEED = 360

class Motors():
    def __init__(self):
        self.PORTS = pypot.dynamixel.get_available_ports()
        self.port = self.PORTS[0]
        self.DXL_IO =  pypot.dynamixel.DxlIO(self.port)
        self.found_ids  =  self.DXL_IO.scan(range(5))
        self.ids = self.found_ids[:2]
        self.DXL_IO.enable_torque(self.ids)

        self.DXL_IO.set_wheel_mode([1])
        self.DXL_IO.set_wheel_mode([2])

    def go_forward(self):
        """ Go forward"""
        self.DXL_IO.set_moving_speed({1: -ROTATION_SPEED})
        self.DXL_IO.set_moving_speed({2: ROTATION_SPEED})

    def stop(self):
        self.DXL_IO.set_moving_speed({1: 0})
        self.DXL_IO.set_moving_speed({2: 0})
        
    # Turn
    def turn_left(self, l, t):
        """ 
        Slow down left wheel for l seconds
        
        Args :
        l = degrees/s
        t = time in seconds
        
        """
        self.DXL_IO.set_moving_speed({2: l})
        t0 = time.time()
        while True:
            t1 = time.time()
            if (t1 - t0) > t:
                break
        self.go_forward()

    def turn_right(self, r, t):
        """
        Slow down right wheel for l seconds
        Args :
        r = degrees/s
        t = time in seconds
        """
        self.DXL_IO.set_moving_speed({1: -r})
        t0 = time.time()
        while True:
            t1 = time.time()
            if (t1 - t0) > t:
                break
        self.go_forward()

    def get_wheel_info(self):
        
        print("---")
        # current angular position motors
        positions = self.DXL_IO.get_present_position([1, 2])
        print(f"Position des moteurs: {positions}")

        # current speed of motors
        speeds = self.DXL_IO.get_present_speed([1, 2])
        print(f"Vitesse des moteurs: {speeds}")

        # current temp of motors
        temperatures = self.DXL_IO.get_present_temperature([1, 2])
        print(f"Température des moteurs: {temperatures}")

        # current vol of motors
        voltages = self.DXL_IO.get_present_voltage([1, 2])
        print(f"Voltage des moteurs: {voltages}")
    ###

    def get_current_speed_wheels(self) : 
        """ 
        Get the current speed of wheels

        Returns : 
        - v_droit and v_gauche : wheel speeds (rad/s)
    
        """
        vd, vg = self.DXL_IO.get_present_speed([1, 2]) #/!\ deg/s
        return (vd/180) * math.pi, (vg/180) * math.pi

    ###############################################
    def spin_wheels(self, v_gauche, v_droite):
        """ Spin wheels with given values 
        To stop the robot, choose 0 for each wheels

        Args:
        - v_gauche and v_droit : wheel speeds rad/s
        
        """
        vd = math.degrees(v_droite)
        vg = math.degrees(v_gauche) # --> deg/s
        
        self.DXL_IO.set_moving_speed({1: -vd})
        self.DXL_IO.set_moving_speed({2: vg})

    def rotate(self, n, omega_roue = 3.0):
        """ 
        Rotation of the robot 
        
        Arg : 
        - n (rad) : angle
        omega_roue = 3  # Vitesse angulaire fixe (rad/s)
        """

        # Calculer la distance à parcourir par la roue active
        dist = ((n*180/math.pi) / 360) * 2 * math.pi * (L / 2)
        
        # Calculer le nombre de tours que la roue doit effectuer
        num_tours = dist / (2 * math.pi * r)
        
        # Calculer le temps nécessaire pour tourner
        # Distance parcourue par la roue divisée par sa vitesse angulaire
        temps_rotation = abs(num_tours / (omega_roue / (2 * math.pi)))
        
        if n > 0:
            self.spin_wheels(0, 2 * omega_roue)
        else:
            self.spin_wheels(2 * omega_roue, 0)

    def rotate_two_wheels(self, n, omega_roue = 3.0): 
        """ 
        Rotation of the robot 
        
        Arg : 
        - n (rad) : angle
        omega_roue = 3  # Vitesse angulaire fixe (rad/s)
        """
        # Calculer la distance à parcourir par la roue active
        dist = ((n*180/math.pi) / 360) * 2 * math.pi * (L / 2)
        
        # Calculer le nombre de tours que la roue doit effectuer
        num_tours = dist / (2 * math.pi * r)

        # Calculer le temps nécessaire pour tourner
        # Distance parcourue par la roue divisée par sa vitesse angulaire
        temps_rotation =  abs(num_tours / (omega_roue / (2 * math.pi)))
        
        if n > 0:
            self.spin_wheels(-omega_roue, omega_roue)
        else:
            self.spin_wheels(omega_roue, -omega_roue)

    #####################
    def move_forward_distance(self, distance, angular_speed=3.0):
        """
        Go foward to a choosen distance
        Arg : 
        - distance (m) : a choosen distance
        - angular_speed (rad/s) : default 3.0, speed
        """
        # Compute wheel circumference
        wheel_circumference = math.pi * r

        # Number of rotations needed
        num_rotations = distance / (wheel_circumference * 2)

        # Compute time
        time_to_travel = num_rotations / (angular_speed / (2 * math.pi))

        # Give speed to motors
        self.spin_wheels(angular_speed, angular_speed)

    #####################
    def move_backward_distance(self, distance, angular_speed=3.0):
        """
        Go foward to a choosen distance
        Arg : 
        - distance (m) : a choosen distance
        - angular_speed (rad/s) : default 3.0, speed
        """
        # Compute wheel circumference
        wheel_circumference = math.pi * r

        # Number of rotations needed
        num_rotations = distance / (wheel_circumference * 2)

        # Compute time
        time_to_travel = num_rotations / (angular_speed / (2 * math.pi))

        # Give speed to motors
        self.spin_wheels(-angular_speed, -angular_speed)
        
        # Wait the good time to do the distance
        #time.sleep(time_to_travel)

        #self.stop()
        
    def passive_wheels(self) :
        """ Go to passive mode, torque = 0.0""" 
        self.DXL_IO.disable_torque(self.ids)
        
    #### go to
    def rotate_two_wheels_go_to(self, n, omega_roue = 3.0): 
        """ 
        Rotation of the robot 
        
        Arg : 
        - n (rad) : angle
        - omega_roue = 3  # Vitesse angulaire fixe (rad/s)
        
        Return : 
        - temps_rotation (s) : time to do the correct distance
        
        """
        # Calculer la distance à parcourir par la roue active
        dist = ((n*180/math.pi) / 360) * 2 * math.pi * (L / 2)
        
        # Calculer le nombre de tours que la roue doit effectuer
        num_tours = dist / (2 * math.pi * r)

        # Calculer le temps nécessaire pour tourner
        # Distance parcourue par la roue divisée par sa vitesse angulaire
        temps_rotation =  abs(num_tours / (omega_roue / (2 * math.pi)))
        
        if n > 0:
            self.spin_wheels(-omega_roue, omega_roue)
        else:
            self.spin_wheels(omega_roue, -omega_roue)
        
        return temps_rotation

    def move_forward_distance_go_to(self, distance, angular_speed=3.0):
        """
        Go foward to a choosen distance
        Arg : 
        - distance (m) : a choosen distance
        - angular_speed (rad/s) : default 3.0, speed
        
        Return : 
        - time_to_travel (s) : time to do the correct distance
        """
        # Compute wheel circumference
        wheel_circumference = math.pi * r

        # Number of rotations needed
        num_rotations = distance / (wheel_circumference * 2)

        # Compute time
        time_to_travel = num_rotations / (angular_speed / (2 * math.pi))

        # Give speed to motors
        self.spin_wheels(angular_speed, angular_speed)
        
        return time_to_travel
    
    def compute_position_orientation(self, vd, vg, x_n_1, y_n_1, theta_n_1, t_n_1):
        print("v_droit_motor = ", vd, " v_gauche_motor = ", vg)
        
        x_dot_real, theta_dot_real = tools.direct_kinematics(vg, - vd) # real droit - car dans l'autre sens
        print("x_dot_real = ", x_dot_real, " theta_dot_real = ", theta_dot_real)
        
        t_n = time.time()
        x_n, y_n, theta_n = tools.tick_odom(x_n_1, y_n_1, theta_n_1, t_n_1, x_dot_real, theta_dot_real, t_n) # real 
        print(f"x = {x_n}, y = {y_n}, theta = {theta_n}")
      
        return x_n, y_n, theta_n, t_n