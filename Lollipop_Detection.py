import cv2 as cv
import numpy as np

#===========Some Variables=============
lower_red = np.array([0,114,159])
upper_red = np.array([6,239,255])
color = (255,0,0)
lollipop_width = 70
#======================================

def lollipop_position(image):
  global lower_red, upper_red
  hsv_img = cv.cvtColor(image, cv.COLOR_BGR2HSV)
  mask = cv.inRange(hsv_img, lower_red, upper_red)
  contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
  center = False
  for cnt in contours:
    area = cv.contourArea(cnt)
    if area > 500:
      perimeter = cv.arcLength(cnt, True)
      approx = cv.approxPolyDP(cnt, 0.02 * perimeter, True)
      x, y, w, h = cv.boundingRect(approx)
      center = (int(x + w // 2), int(y + h // 2))
      draw_outline(image, center, lollipop_width)

  return center

def draw_outline(image, center, width):
  pt1 = (center[0] - int(width/2), center[1] - int(width/2))
  pt2 = (center[0] + int(width/2), center[1] + int(width/2))
  cv.rectangle(image, pt1, pt2, color, 2)

  return image