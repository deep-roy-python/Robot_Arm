import cv2 as cv
from imutils import face_utils
import dlib
import math

#===========Variables============
mouth_threshold = 15
color = (0,255,0)
font = cv.FONT_HERSHEY_SIMPLEX
#================================

model_name = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model_name)

def find_open_mouth(image):
  gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  result = detector(gray_img, 0)
  center = False
  for (i, rect) in enumerate(result):
    shape = predictor(gray_img, rect)
    shape = face_utils.shape_to_np(shape)
    x1, y1, x2, y2 = [shape[51][0], shape[51][1], shape[57][0], shape[57][1]]
    gap = distance_2d([x1, y1], [x2, y2])
    if gap >= mouth_threshold:
      center = draw_mouth(image, shape[51], shape[54], shape[57], shape[48])
  return center

def distance_2d(p1, p2):
  distance = math.sqrt(
    math.pow(p1[0]-p2[0], 2) +
    math.pow(p1[1]-p2[1], 2)
  )
  return int(distance)

def draw_mouth(img,a,b,c,d):
  ac = distance_2d(a,c)
  p1 = d[0], d[1]-int(ac/2)
  p2 = b[0], b[1]+int(ac/2)
  center = (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))
  cv.rectangle(img, p1, p2, color, 1)
  cv.putText(img, "Open", p2, font, 0.5, color, 0, cv.LINE_AA)
  return center