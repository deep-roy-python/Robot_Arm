"""
Repeat the recorded movement saved with gaming controller
"""

import json
import serial
import time

node_mcu = serial.Serial("COM3", 9600)

with open("arm_gamepad_data.json", "r") as file:
  file_data = json.load(file)
  for data in file_data:
    rotation = data[0]
    tilt = data[1]
    forward = data[2]
    grab = data[3]
    node_mcu.write(f"R{rotation}T{tilt}F{forward}G{grab}".encode())
    time.sleep(1)
