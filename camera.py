import cv2
import numpy as np

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


#camera_index is the video device number of the camera 
camera_index = 0
cam = cv2.VideoCapture(camera_index)

ret, image = cam.read()

cv2.imwrite('./image.jpg', image)

h = image.shape[0]
w = image.shape[1]

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

bluemask = getBlueMask(hsv)
redmask = getRedMask(hsv)
yellowmask = getYellowMask(hsv)

res = cv2.bitwise_and(image,image, mask=bluemask)

cv2.imwrite('./blueimage.jpg', res)

res = cv2.bitwise_and(image,image, mask=redmask)

cv2.imwrite('./redimage.jpg', res)

res = cv2.bitwise_and(image,image, mask=yellowmask)

cv2.imwrite('./yellowimage.jpg', res)
cam.release()
cv2.destroyAllWindows()