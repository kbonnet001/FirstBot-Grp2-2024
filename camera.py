import math
import cv2
import numpy as np
from enum import Enum
import tools
import motors
import time

class Color(Enum):
  RED = (0, 0, 255)
  BLACK = (0, 0, 0)
  YELLOW = (0, 255, 255)

# Mask 
#-----

def getRedMask(hsv):
  lower_red1 = np.array([0,50,50])
  upper_red1 = np.array([10,255,255])

  lower_red2 = np.array([170,50,50])
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
  upper_yellow = np.array([35,255,255])

  mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

  return mask

def getBlackMask(hsv):
  lower_black = np.array([0,0,0])
  upper_black = np.array([180,255,90])

  mask = cv2.inRange(hsv, lower_black, upper_black)

  return mask

camera_w_size = 0.04
camera_h_size = 0.03

# Upper sampling line, 0.6 for position, higher values
sampling_line_u = 0.6

# Lower sampling line, the value needs to be greater than sampling_line_u and less than 1."
sampling_line_l = 0.9

#camera_index is the video device number of the camera 
camera_index = 0
cam = cv2.VideoCapture(camera_index)

m = motors.Motors()
try:
  while(True):
    t0 = time.time()
    ret, image = cam.read()

    h = image.shape[0]
    w = image.shape[1]

    center_x = int(w / 2)
    real_center_y = 0.052 + camera_h_size/2

    px_by_cm = h / camera_h_size

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = None
    #cv2.imwrite('./image.jpg', image)
    c = Color.RED
    match c:
      case Color.RED:
        mask = getRedMask(hsv)
          
      case Color.BLACK:
        mask = getBlackMask(hsv)

      case Color.YELLOW:
        mask = getYellowMask(hsv)

    mask = cv2.erode(mask, None, iterations=1)  # Eroding operation to remove noise
    mask = cv2.dilate(mask, None, iterations=1)  # Expansion operation enhances the target line

    #cv2.imwrite('./' + c.name + 'mask.jpg', mask)
    res = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imwrite('./' + c.name + 'image.jpg', res)

    # Detect the target line based on the positions of the upper and lower 
    # sampling lines, and calculate steering and velocity control signals according to the detection results
    sampling_hu = int(h * sampling_line_u)
    sampling_hl = int(h * sampling_line_l)

    get_sampling_u = mask[sampling_hu]
    get_sampling_l = mask[sampling_hl]

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
        sampling_center_u= int((sampling_left_u + sampling_right_u) / 2)  # Index of the center of the upper sampling line target line
    # If a target line is detected at the lower sampling line, calculate the target line center position
    if sam_2:
        sampling_left_l  = line_index_l[0][0]
        sampling_right_l = line_index_l[0][sampling_width_l - 1]
        sampling_center_l= int((sampling_left_l + sampling_right_l) / 2)

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

    #cv2.imwrite('./debugimage.jpg', image)

    t2 = time.time()

    tolerance_theta1 = math.pi/4
    tolerance_theta2 = 0.05

    tolerance_center = w * 0.3

    delta_center_1 = center_x - sampling_center_u
    delta_sampling_1 = (px_by_cm * real_center_y) - sampling_hu
    theta1 = math.atan(delta_center_1/delta_sampling_1)

    delta_center_2 = sampling_center_l - sampling_center_u
    delta_sampling_2 = sampling_hl - sampling_hu
    theta2 = math.atan(delta_center_2/delta_sampling_2)

    print(theta1)
    print(theta2)
    print(delta_center_1)
    print(delta_center_2)

    if(sam_1 and sam_2):
      if(abs(delta_center_1) > tolerance_center):
        #cv2.imwrite('./debugimage.jpg', image)
        m.rotate(theta1)
        #m.move_forward_distance(real_center_y)
        #m.rotate_two_wheels(-theta1)
      #elif(abs(delta_center_2) > tolerance_center):
      # m.rotate_two_wheels(theta2)
      else:
        m.move_forward_distance(camera_h_size)
    else:
      m.move_backward_distance(camera_h_size)
    
    t3 = time.time()
    
    print("Temps pour le traitement d'image: " + str(round(t1 - t0, 3)) + " s")
    print("Temps pour le dessin de la ligne: " + str(round(t2 - t1, 3)) + " s")
    print("Temps pour donner la consigne au robot: " + str(round(t3 - t2, 3)) + " s")
    
    
except BaseException as e:
  m.stop()
  cam.release()
  cv2.destroyAllWindows()
  print(e)