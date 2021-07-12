import cv2 as cv
from Lollipop_Detection import lollipop_position
from Open_Mouth_Detection import find_open_mouth, distance_2d
import time
import serial

#==========Some Variables===========
mouth_open_time = 2
node_mcu = serial.Serial('COM3', 9600)
near = 50
speed = 5
grab = 0
#===================================
def open_mouth_activator(is_mouth_open):
  global feed_lollipop
  if not feed_lollipop:
    global last_mouth_open, mouth_open_time
    if is_mouth_open:
      if int(time.time() - last_mouth_open) >= mouth_open_time:
        print("Feeding Lollipop")
        feed_lollipop = True
        last_mouth_open = time.time()
    else:
      last_mouth_open = time.time()
def feeding_lollipop(pos_lol, pos_mou):
  if feed_lollipop:
    arm_movement(pos_mou, pos_lol)

def arm_movement(mou, lol):
  global rotation, tilt, forward, last_pos
  if lol[0] < mou[0]:
    forward -= speed
  elif lol[0] > mou[0]:
    forward += speed
  if lol[1] < mou[1]:
    tilt -= speed
  elif lol[1] > mou[1]:
    tilt += speed
  print(tilt, forward)
  if forward in range(50, 180) and tilt in range(80, 180):
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
    last_pos = [tilt, forward]
    print(f"moved to ({tilt}, {forward})")
    time.sleep(0.1)
  else:
    tilt, forward = last_pos

rotation, tilt, forward = [90, 104, 51]
last_pos = [tilt, forward]
# moving arm to ideal position
node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
time.sleep(0.25)

mouth_last, lollipop_last = [0,0]
feed_lollipop = False
last_mouth_open = 0
cap = cv.VideoCapture(0)
while True:
  open_mouth = False
  _, frame = cap.read()
  lollipop_pos = lollipop_position(frame)
  mouth_pos = find_open_mouth(frame)
  if mouth_pos:
    open_mouth = True
    if lollipop_pos:
      if distance_2d(lollipop_pos, mouth_pos) > near:
        feeding_lollipop(lollipop_pos, mouth_pos)
      if distance_2d(lollipop_pos, mouth_pos) <= near:
        feed_lollipop = False
        node_mcu.write(f"R50T{tilt}F{forward}G{grab}".encode())
        time.sleep(0.25)

  cv.imshow("test", frame)
  open_mouth_activator(open_mouth)
  cv.waitKey(1)
