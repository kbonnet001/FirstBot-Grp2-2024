import math
import cv2
import numpy as np
from enum import Enum
import tools
import motors
import time
from SkyviewMap import SkyviewMap
from plot import plot_position_orientation_comparaison

class Color(Enum):
  RED = (0, 0, 255)
  BLACK = (0, 0, 0)
  YELLOW = (0, 255, 255)

# Mask 
#-----

def getRedMask(hsv):
  lower_red1 = np.array([0,50,50])
  upper_red1 = np.array([15,255,255])

  lower_red2 = np.array([165,50,50])
  upper_red2 = np.array([180,255,255])


  mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
  mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

  mask = mask1 | mask2

  return mask

def getBlueMask(hsv):
  lower_blue = np.array([100,50,50])
  upper_blue = np.array([140,255,255])

  mask = cv2.inRange(hsv, lower_blue, upper_blue)

  return mask

def getYellowMask(hsv):
  lower_yellow = np.array([20,50,50])
  upper_yellow = np.array([80,255,255])

  mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

  return mask

def getBlackMask(gray):
  _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
  return thresh

camera_w_size = 0.04
camera_h_size = 0.03

# Upper sampling line, 0.6 for position, higher values
sampling_line_u = 0.6

# Lower sampling line, the value needs to be greater than sampling_line_u and less than 1."
sampling_line_l = 0.9

sampling_line_yellow = 0.5

speed = 6.0

#camera_index is the video device number of the camera 
camera_index = 0
cam = cv2.VideoCapture(camera_index)

c = Color.BLACK

yellow_already_detected = True

m = motors.Motors()
x_n = 0.0
y_n = 0.0 
theta_n = 0.0
t_n = time.time()

# Preparation of lists for plot
list_x = [x_n]
list_y = [y_n]
list_theta = [theta_n]
list_vg = [0.0]
list_vd = [0.0]
list_t = [0.0]
last_time = time.time()  # horodotage initialisation

# Prepare map
map = SkyviewMap(width = 600, height=600, scale=100, color=c.value, name="camera_map")
try:
  while(True):
    print("---")
    x_n_1 = x_n
    y_n_1 = y_n
    theta_n_1 = theta_n
    t_n_1 = t_n
    
    t0 = time.time()
    ret, image = cam.read()

    h = image.shape[0]
    w = image.shape[1]

    center_x = int(w / 2)
    real_center_y = 0.052 + camera_h_size/2

    px_by_cm = h / camera_h_size

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    followmask = None
    #cv2.imwrite('./image.jpg', image)

    yellowmask = getYellowMask(hsv)
    yellowmask = cv2.erode(yellowmask, None, iterations=1)  # Eroding operation to remove noise
    yellowmask = cv2.dilate(yellowmask, None, iterations=1)  # Expansion operation enhances the target line

    sampling_hy = int(h * sampling_line_yellow)

    get_sampling_y = yellowmask[sampling_hy]

    sampling_width_y = np.sum(get_sampling_y == 255)

    tolerance_yellow = 100

    if sampling_width_y > tolerance_yellow and not yellow_already_detected:
      yellow_already_detected = True
      match c:
        case Color.RED:
          c = Color.BLACK
          exit()
        case Color.BLACK:
          c = Color.RED
      map.color = c.value
    elif(not sampling_width_y):
       yellow_already_detected = False
       
    match c:
      case Color.RED:
        followmask = getRedMask(hsv)
      
      case Color.BLACK:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        followmask = getBlackMask(gray)
    
    followmask = cv2.erode(followmask, None, iterations=1)  # Eroding operation to remove noise
    followmask = cv2.dilate(followmask, None, iterations=1)  # Expansion operation enhances the target line

    #cv2.imwrite('./' + c.name + 'mask.jpg', mask)
    #res = cv2.bitwise_and(image, image, mask=followmask)
    #cv2.imwrite('./' + c.name + 'image.jpg', res)

    # Detect the target line based on the positions of the upper and lower 
    # sampling lines, and calculate steering and velocity control signals according to the detection results
    sampling_hu = int(h * sampling_line_u)
    sampling_hl = int(h * sampling_line_l)

    get_sampling_u = followmask[sampling_hu]
    get_sampling_l = followmask[sampling_hl]

    # Calculate the width of the target line at the upper and lower sampling lines
    sampling_width_u = np.sum(get_sampling_u == 255)
    sampling_width_l = np.sum(get_sampling_l == 255)

    if sampling_width_u:
        sam_1 = True
    else:
        sam_1 = False
    if sampling_width_l:
        sam_2 = True
    else:
        sam_2 = False

    # Get the edge index of the target line at the upper and lower sampling lines
    line_index_u = np.where(get_sampling_u == 255)
    line_index_l = np.where(get_sampling_l == 255)

    sampling_center_u = center_x
    sampling_center_l = center_x

    # If the target line is detected at the upper sampling line, calculate the center position of the target line
    if sam_1:
      sampling_left_u  = line_index_u[0][0]  # Index of the leftmost index of the upper sampling line target line
      sampling_right_u = line_index_u[0][sampling_width_u - 1]  # Index to the far right of the upper sampling line target line
      sampling_center_u= line_index_u[0][int(len(line_index_u[0])/2)]  # Index of the center of the upper sampling line target line
    # If a target line is detected at the lower sampling line, calculate the target line center position
    if sam_2:
      sampling_left_l  = line_index_l[0][0]
      sampling_right_l = line_index_l[0][sampling_width_l - 1]
      sampling_center_l= line_index_l[0][int(len(line_index_l[0])/2)]

    t1 = time.time()

    print()
    print(c.name)
    print("Upper line: " + str(sam_1))
    if sam_1:
        print("Upper line left: " + str(sampling_left_u))
        print("Upper line right: " + str(sampling_right_u))
        print("Upper line width: " + str(sampling_width_u))
        print("Upper line middle: " + str(sampling_center_u))
    print("Lower line: " + str(sam_2))
    if sam_2:
        print("Lower line left: " + str(sampling_left_l))
        print("Lower line right: " + str(sampling_right_l))
        print("Lower line width: " + str(sampling_width_l))
        print("Lower line middle: " + str(sampling_center_l))
    
    print("Time for one frame: " + str(round(time.time() - t0, 3)) + " s")

    """
    if sam_1:
      # Draw c.value marker lines at the ends of the target line at the upper sample line
      cv2.line(image, (sampling_left_u, sampling_hu+20), (sampling_left_u, sampling_hu-20), c.value, 2)
      cv2.line(image, (sampling_right_u, sampling_hu+20), (sampling_right_u, sampling_hu-20), c.value, 2)
    if sam_2:
      # Draw c.value marker lines at the ends of the target line at the lower sampling line
      cv2.line(image, (sampling_left_l, sampling_hl+20), (sampling_left_l, sampling_hl-20), c.value, 2)
      cv2.line(image, (sampling_right_l, sampling_hl+20), (sampling_right_l, sampling_hl-20), c.value, 2)
    if sam_1 and sam_2:
      # If the target line is detected at both the upper and lower sample lines, draw a c.value line from the center of the upper sample line to the center of the lower sample line.
      cv2.line(image, (sampling_center_u, sampling_hu), (sampling_center_l, sampling_hl), c.value, 2)

    cv2.line(image, (0, sampling_hu), (w, sampling_hu), (0, 255, 0), 2)
    cv2.line(image, (0, sampling_hl), (w, sampling_hl), (0, 255, 0), 2)
    """

    #cv2.imwrite('./debugimage.jpg', image)

    t2 = time.time()

    tolerance_theta1 = math.pi/4
    tolerance_theta2 = 0.05

    tolerance_center = w * 0.25

    delta_center_1 = center_x - sampling_center_u
    delta_sampling_1 = (px_by_cm * real_center_y) - sampling_hu
    theta1 = math.atan(delta_center_1/delta_sampling_1)

    """
    delta_center_2 = sampling_center_l - sampling_center_u
    delta_sampling_2 = sampling_hl - sampling_hu
    theta2 = math.atan(delta_center_2/delta_sampling_2)
    """

    delta_center_3 = center_x - sampling_center_l
    delta_sampling_3 = (px_by_cm * real_center_y) - sampling_hl
    theta3 = math.atan(delta_center_3/delta_sampling_3)

    print("Angle of correction : " + str(theta1))
    #print(theta2)
    print("Difference between centers : " + str(delta_center_1))
    #print(delta_center_2)

    if(sam_1 and sam_2):
      if(abs(delta_center_1) > tolerance_center):
        #cv2.imwrite('./debugimage.jpg', image)
        m.rotate(theta1, omega_roue=speed)
      else:
        m.move_forward_distance(angular_speed=speed)
    elif(sam_2):
      m.rotate(theta3, omega_roue=speed)
    else:
      m.move_forward_distance(angular_speed=speed)
    
    t3 = time.time()
    
    # odometry
    v_droit_motor, v_gauche_motor = m.get_current_speed_wheels()
    x_n, y_n, theta_n, t_n = m.compute_position_orientation(v_droit_motor, v_gauche_motor, x_n_1, y_n_1, theta_n_1, t_n_1)
    
    print("Temps pour le traitement d'image: " + str(round(t1 - t0, 3)) + " s")
    print("Images par secondes : " +  str(1/round(t1 - t0, 3)) + " fps")
    print("Temps pour le dessin de la ligne: " + str(round(t2 - t1, 3)) + " s")
    print("Temps pour donner la consigne au robot: " + str(round(t3 - t2, 3)) + " s")
    
    if t_n - last_time >= 0.5 : #every second
        
      # Add line on map
      map.trace_position_on_map((list_x[-1], list_y[-1]), (x_n, y_n))
      
      # append
      list_x.append(x_n)
      list_y.append(y_n)
      list_theta.append(theta_n%(2*math.pi))
      list_vg.append(v_gauche_motor)
      list_vd.append(-v_droit_motor)
      list_t.append(list_t[-1] + t_n - t_n_1)
        
      last_time = t_n
    
    
except BaseException as e:
  m.stop()
  cam.release()
  cv2.destroyAllWindows()
  print(e)

  print(f"Fin de l'odometrie : \n x = {x_n}, y = {y_n}, theta = {theta_n}")
  plot_position_orientation_comparaison(list_x, list_y, list_theta, list_vg, list_vd, list_t, "camera_plot")
  map.display_and_save_map()