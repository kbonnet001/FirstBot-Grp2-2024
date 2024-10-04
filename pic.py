import cv2
import numpy as np
import enum as Enum

"""
class Color(Enum):
	RED = (0, 0, 255)
	BLACK = (0, 0, 0)
	YELLOW = (0, 255, 255)
"""

def getYellowMask(hsv):
  lower_yellow = np.array([20,50,50])
  upper_yellow = np.array([80,255,255])

  mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

  return mask

def getBlackMask(hsv):
  lower_black = np.array([0,0,0])
  upper_black = np.array([180,255,10])

  mask = cv2.inRange(hsv, lower_black, upper_black)

  return mask

def getBlackThresh(gray):
  _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
  return thresh

def getRedMask(hsv):
  lower_red1 = np.array([0,0,0])
  upper_red1 = np.array([20,255,255])

  lower_red2 = np.array([160,0,0])
  upper_red2 = np.array([180,255,255])


  mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
  mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

  mask = mask1 | mask2

  return mask

# Upper sampling line, 0.6 for position, higher values
sampling_line_u = 0.6

# Lower sampling line, the value needs to be greater than sampling_line_u and less than 1."
sampling_line_l = 0.9

cam = cv2.VideoCapture(0)
_, img = cam.read()

h = img.shape[0]
w = img.shape[1]

cv2.imwrite('./pic.jpg', img)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#mask = getBlackMask(hsv)

#mask = getBlackThresh(gray)
mask = getRedMask(hsv)
#mask = getYellowMask(hsv)

mask = cv2.erode(mask, None, iterations=1)  # Eroding operation to remove noise
mask = cv2.dilate(mask, None, iterations=1)  # Expansion operation enhances the target line

cv2.imwrite('./gray.jpg', gray)
cv2.imwrite('./mask.jpg', mask)

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

if sam_1:
	sampling_left_u  = line_index_u[0][0]  # Index of the leftmost index of the upper sampling line target line
	sampling_right_u = line_index_u[0][sampling_width_u - 1]  # Index to the far right of the upper sampling line target line
	sampling_center_u= int((sampling_left_u + sampling_right_u) / 2)  # Index of the center of the upper sampling line target line
	sampling_center_u= line_index_u[0][int(len(line_index_u[0])/2)]
# If a target line is detected at the lower sampling line, calculate the target line center position
if sam_2:
	sampling_left_l  = line_index_l[0][0]
	sampling_right_l = line_index_l[0][sampling_width_l - 1]
	sampling_center_l= int((sampling_left_l + sampling_right_l) / 2)
	sampling_center_l= line_index_l[0][int(len(line_index_l[0])/2)]

if sam_1:
	# Draw c.value marker lines at the ends of the target line at the upper sample line
	cv2.line(img, (sampling_left_u, sampling_hu+20), (sampling_left_u, sampling_hu-20), (0, 0, 255), 2)
	cv2.line(img, (sampling_right_u, sampling_hu+20), (sampling_right_u, sampling_hu-20), (0, 0, 255), 2)
if sam_2:
	# Draw c.value marker lines at the ends of the target line at the lower sampling line
	cv2.line(img, (sampling_left_l, sampling_hl+20), (sampling_left_l, sampling_hl-20), (0, 0, 255), 2)
	cv2.line(img, (sampling_right_l, sampling_hl+20), (sampling_right_l, sampling_hl-20), (0, 0, 255), 2)
if sam_1 and sam_2:
	# If the target line is detected at both the upper and lower sample lines, draw a c.value line from the center of the upper sample line to the center of the lower sample line.
	cv2.line(img, (sampling_center_u, sampling_hu), (sampling_center_l, sampling_hl), (0, 0, 255), 2)

cv2.line(img, (0, sampling_hu), (w, sampling_hu), (0, 255, 0), 2)
cv2.line(img, (0, sampling_hl), (w, sampling_hl), (0, 255, 0), 2)

cv2.imwrite('./picdebug.jpg', img)

cam.release()