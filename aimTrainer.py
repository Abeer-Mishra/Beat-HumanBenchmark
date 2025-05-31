import mss
import pyautogui
import numpy as np
import cv2
import time

sct = mss.mss()

monitor = {
    "top": 134,
    "left": 240,
    "width": 1000,
    "height": 420
}

end_check = {
    "top": 134,
    "left": 240,
    "width": 1000,
    "height": 420
}

lower_blue = np.array([95, 40, 180])
upper_blue = np.array([115, 160, 255])

lower_yellow = np.array([20, 100, 150])
upper_yellow = np.array([40, 255, 255])

print("⚡ Ready to GO in 2 second...")
time.sleep(2)

cv2.namedWindow("dummy")  # create a small window for keyboard capture

while True:
    # Check ESC key press via OpenCV
    if cv2.waitKey(1) & 0xFF == 27:
        print("🛑 ESC pressed. Exiting.")
        break

    end_img = np.array(sct.grab(end_check))
    hsv_end = cv2.cvtColor(end_img, cv2.COLOR_BGRA2BGR)
    hsv_end = cv2.cvtColor(hsv_end, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_end, lower_yellow, upper_yellow)

    yellow_count = cv2.countNonZero(yellow_mask)
    if yellow_count > 300:
        print(f"🟡 Found yellow! Pixels: {yellow_count} — Stopping.")
        break
    else:
        print(f"🕵️ Yellow Pixels: {yellow_count}")

    img = np.array(sct.grab(monitor))
    hsv = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        if w * h > 100:
            center_x = monitor["left"] + x + w // 2
            center_y = monitor["top"] + y + h // 2
            pyautogui.moveTo(center_x, center_y, duration=0)
            pyautogui.click()

    cv2.imshow("dummy", np.zeros((1, 1), dtype=np.uint8))  # refresh dummy window


cv2.destroyAllWindows()
