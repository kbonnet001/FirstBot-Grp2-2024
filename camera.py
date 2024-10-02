import cv2
import numpy as np
from enum import Enum

class Color(Enum):
   RED = 0
   BLUE = 1
   YELLOW = 2

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


# Upper sampling line, 0.6 for position, higher values
sampling_line_1 = 0.6

# Lower sampling line, the value needs to be greater than sampling_line_1 and less than 1."
sampling_line_2 = 0.9

#camera_index is the video device number of the camera 
camera_index = 0
cam = cv2.VideoCapture(camera_index)

ret, image = cam.read()

cv2.imwrite('./image.jpg', image)

h = image.shape[0]
w = image.shape[1]

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

mask = None

for c in Color:
  match c:
      case Color.RED:
        mask = getRedMask(hsv)
         
      case Color.BLUE:
        mask = getBlueMask(hsv)

      case Color.YELLOW:
        mask = getYellowMask(hsv)
  mask = cv2.erode(mask, None, iterations=1)  # Eroding operation to remove noise
  mask = cv2.dilate(mask, None, iterations=1)  # Expansion operation enhances the target line

  cv2.imwrite('./' + c.name + 'mask.jpg', mask)
  res = cv2.bitwise_and(image, image, mask=mask)
  cv2.imwrite('./' + c.name + 'image.jpg', res)

  # Detect the target line based on the positions of the upper and lower sampling lines, and calculate steering and velocity control signals according to the detection results
  sampling_h1 = int(h * sampling_line_1)
  sampling_h2 = int(h * sampling_line_2)

  get_sampling_1 = mask[sampling_h1]
  get_sampling_2 = mask[sampling_h2]

  # Calculate the width of the target line at the upper and lower sampling lines
  sampling_width_1 = np.sum(get_sampling_1 == 255)
  sampling_width_2 = np.sum(get_sampling_2 == 255)

  if sampling_width_1:
      sam_1 = True
  else:
      sam_1 = False
  if sampling_width_2:
      sam_2 = True
  else:
      sam_2 = False

  # Get the edge index of the target line at the upper and lower sampling lines
  line_index_1 = np.where(get_sampling_1 == 255)
  line_index_2 = np.where(get_sampling_2 == 255)

  # If the target line is detected at the upper sampling line, calculate the center position of the target line
  if sam_1:
      sampling_1_left  = line_index_1[0][0]  # Index of the leftmost index of the upper sampling line target line
      sampling_1_right = line_index_1[0][sampling_width_1 - 1]  # Index to the far right of the upper sampling line target line
      sampling_1_center= int((sampling_1_left + sampling_1_right) / 2)  # Index of the center of the upper sampling line target line
  # If a target line is detected at the lower sampling line, calculate the target line center position
  if sam_2:
      sampling_2_left  = line_index_2[0][0]
      sampling_2_right = line_index_2[0][sampling_width_2 - 1]
      sampling_2_center= int((sampling_2_left + sampling_2_right) / 2)

  print("")
  print(c.name)
  print("Upper line: " + str(sam_1))
  if sam_1:
     print("Upper line left: " + str(sampling_1_left))
     print("Upper line right: " + str(sampling_1_right))
     print("Upper line width: " + str(sampling_width_1))
     print("Upper line middle: " + str(sampling_1_center))
  print("Lower line: " + str(sam_2))
  if sam_2:
     print("Lower line left: " + str(sampling_2_left))
     print("Lower line right: " + str(sampling_2_right))
     print("Lower line width: " + str(sampling_width_2))
     print("Lower line middle: " + str(sampling_2_center))

  

cam.release()
cv2.destroyAllWindows()