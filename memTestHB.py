import mss
import pyautogui
import numpy as np
import cv2
import time
import keyboard  # Make sure you install this using: pip install keyboard

# --- SETUP ---
sct = mss.mss()

monitor = {
    "top": 134,
    "left": 240,
    "width": 1000,
    "height": 510
}

screen_width, screen_height = pyautogui.size()

lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])

print("⚡ Memory Game Bot Ready. Press 'Q' to stop anytime.")
time.sleep(2)

# --- MAIN LOOP ---
while True:
    if keyboard.is_pressed('q'):
        print("🛑 Q pressed. Exiting safely.")
        break

    # STEP 1: Screenshot and convert
    img = np.array(sct.grab(monitor))
    hsv = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    white_positions = []

    # STEP 2: Find all white tiles
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 100:  # ignore small dots
            center_x = monitor["left"] + x + w // 2
            center_y = monitor["top"] + y + h // 2

            # Check if within screen bounds
            if 0 < center_x < screen_width and 0 < center_y < screen_height:
                white_positions.append((center_x, center_y))

    if white_positions:
        print(f"🧠 Memorized {len(white_positions)} white block(s). Waiting for them to disappear...")
        time.sleep(1.5)  # let the white disappear

        print("👆 Clicking remembered positions...")
        for pos in white_positions:
            pyautogui.moveTo(pos[0], pos[1], duration=0.1)
            pyautogui.click()
            time.sleep(0.1)

    time.sleep(0.05)  # don’t overload CPU
