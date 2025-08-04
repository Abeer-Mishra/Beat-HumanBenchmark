#This Script tell your pointer location and give you a rectangle.
# Used to Change the dimensions in Monitor dict which is located in other scripts that use mss library


#Go to your fist position and then press space. Same with the second position. To Exit, press CTRL + C

import pyautogui
import keyboard

pos = []

while True:
    keyboard.wait('space')
    x,y = pyautogui.position()
    pos.append((x,y))
    print(pos)