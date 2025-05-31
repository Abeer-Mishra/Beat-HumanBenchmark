import cv2
import numpy as np
import pyautogui
import mss
import time

# Define the screen capture region (adjust these values for your screen)
monitor = dict(top=115, left=240, width=1000, height=440)

# Create screen capture tool
sct = mss.mss()

# Define HSV color ranges
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([40, 255, 255])

white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 40, 255])

def find_tile_centers(mask):
    """Returns list of center (x, y) of large enough white/yellow blocks."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 20 and h > 20:  # avoid tiny detections
            cx = monitor['left'] + x + w // 2
            cy = monitor['top'] + y + h // 2
            centers.append((cx, cy))
    return centers

def click_start_if_visible():
    """Detects the yellow Start button and clicks it."""
    screenshot = np.array(sct.grab(monitor))
    hsv = cv2.cvtColor(cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2HSV)
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    centers = find_tile_centers(mask_yellow)
    if centers:
        pyautogui.click(centers[0])
        print("🟨 Clicked Start")
        return True
    return False

# ----------- MAIN LOOP -----------
print("🔁 Starting Visual Memory Bot...")

# Step 1: Wait for yellow Start button and click it
print("🟡 Waiting for Start button...")
while not click_start_if_visible():
    time.sleep(0.5)

# Give time for level to load
time.sleep(1.5)

# Step 2: Level Loop
while True:
    print("🔎 Searching for flashing white tiles...")

    flashed_tiles = []

    # Step 2a: Detect flashing white tiles
    start_time = time.time()
    while time.time() - start_time < 3:
        screenshot = np.array(sct.grab(monitor))
        img = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask_white = cv2.inRange(hsv, white_lower, white_upper)
        centers = find_tile_centers(mask_white)

        if centers:
            flashed_tiles = centers
            print(f"✅ Memorized {len(flashed_tiles)} tile(s).")
            break
        time.sleep(0.05)

    if not flashed_tiles:
        print("❌ No tiles detected. Trying again...")
        continue

    # Step 2b: Wait for tiles to disappear
    time.sleep(1.2)

    # Step 2c: Click on memorized tiles
    print("🖱️ Clicking memorized tiles...")
    for (x, y) in flashed_tiles:
        pyautogui.click(x, y)
        time.sleep(0.1)

    # Step 2d: Wait a bit before next level
    print("🔁 Waiting for next level...")
    time.sleep(1.6)
