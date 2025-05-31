import mss
import pyautogui
import numpy as np
import cv2
import time

sct = mss.mss()

# Define screen region
monitor = dict(top=134, left=240, width=1000, height=420)

# HSV color ranges
lower_blue = np.array([90, 50, 50])   # More lenient
upper_blue = np.array([130, 255, 255])

lower_green = np.array([36, 50, 50])
upper_green = np.array([86, 255, 255])

print("🛠️  Setup your screen. Starting in 3 seconds...")
time.sleep(3)

cv2.namedWindow("mask_blue")
cv2.namedWindow("mask_green")
cv2.namedWindow("dummy")  # For capturing ESC key

clicked_blue = False

while True:
    key = cv2.waitKey(1)
    if key != -1 and (key & 0xFF) == 27:  # ESC to quit
        print("🛑 ESC pressed. Exiting.")
        break

    # Take screenshot
    screenshot = np.array(sct.grab(monitor))
    img = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow("dummy", np.zeros((1, 1), dtype=np.uint8))

    if not clicked_blue:
        print("🔄 Checking for blue...")
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        # cv2.imshow("mask_blue", mask_blue)

        contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(biggest)
            area = w * h
            print(f"🔎 Blue detected with area: {area}")
            if area > 50:
                cx = monitor["left"] + x + w // 2
                cy = monitor["top"] + y + h // 2
                pyautogui.moveTo(cx, cy, duration=0.1)
                pyautogui.click()
                print("🟦 Clicked on Blue - Test Started")
                clicked_blue = True


    elif clicked_blue:
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        # cv2.imshow("mask_green", mask_green)

        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(biggest)
            area = w * h
            print(f"🔎 Green detected with area: {area}")
            if area > 50:
                cx = monitor["left"] + x + w // 2
                cy = monitor["top"] + y + h // 2
                pyautogui.moveTo(cx, cy, duration=0.1)
                pyautogui.click()
                print("🟩 Clicked on Green - Test Ended")
                break

cv2.destroyAllWindows()
