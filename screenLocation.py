#This Script tell your pointer location and give you a rectangle.
# Used to Change the dimensions in Monitor dict which is located in other scripts that use mss library

import pyautogui
import time

print("Move your mouse to top-left corner of target area...")
time.sleep(3)
print("Top-left:", pyautogui.position())

time.sleep(10)

print("Now move to bottom-right corner...")
time.sleep(3)
print("Bottom-right:", pyautogui.position())
