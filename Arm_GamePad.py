"""
Move Robot Arm with a Gaming Controller
Press select button to record arm position
"""



from inputs import get_gamepad
from time import sleep
import serial
import json

speed = 20

node_mcu = serial.Serial("COM3", 9600)
def rotate_left():
  global rotation
  rotation += speed
  if rotation>=0 & rotation<=180 :
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def rotate_right():
  global rotation
  rotation -= speed
  if rotation>=0 & rotation<=180 :
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def move_forward():
  global forward
  forward += speed
  if forward>=50 & forward<=180:
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def move_backward():
  global forward
  forward -= speed
  if forward>=50 & forward<=180:
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def tilt_forward():
  global tilt
  tilt -= speed
  if tilt>=80 & tilt<=180:
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def tilt_backward():
  global tilt
  tilt += speed
  if tilt>=80 & tilt<=180:
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def grab_item():
  global grab
  grab = 0
  node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def release_item():
  global grab
  grab = 70
  node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def back_to_start():
  global rotation, tilt, forward, grab
  rotation, tilt, forward, grab = [90, 104, 51, grab]
  node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
  sleep(0.1)
def add_to_file():
  with open("data.json", "r") as file:
    data = json.load(file)
  with open("data.json", "w") as file:
    data.append([rotation, tilt, forward, grab])
    data_json = json.dumps(data)
    file.write(data_json)
    print("Done")

rotation = 90
tilt = 104
forward = 51
grab = 70
while True:
  events = get_gamepad()
  for event in events:
    if event.code == "BTN_TL" and event.state == 1:
      rotate_left()
    elif event.code == "BTN_TR" and event.state == 1:
      rotate_right()
    elif event.code == "BTN_NORTH" and event.state == 1:
      move_forward()
    elif event.code == "BTN_SOUTH" and event.state == 1:
      move_backward()
    elif event.code == "BTN_EAST" and event.state == 1:
      tilt_forward()
    elif event.code == "BTN_WEST" and event.state == 1:
      tilt_backward()
    elif event.code == "ABS_Z" and event.state >= 100:
      grab_item()
    elif event.code == "ABS_RZ" and event.state >= 100:
      release_item()
    elif event.code == "BTN_START" and event.state == 1:
      back_to_start()
    elif event.code == "BTN_SELECT" and event.state == 1:
      add_to_file()
