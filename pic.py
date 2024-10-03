import cv2

cam = cv2.VideoCapture(0)
_, img = cam.read()

cv2.imwrite('./pic.jpg', img)
cam.release()