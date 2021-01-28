import cv2
# superimposing two images
import numpy as np

import time

cap = cv2.VideoCapture(0)


time.sleep(2)  # 2 sec time to adjust cam with time


background = 0

# capturing the background
for i in range(30):  # 30 times

    ret = cap.set(3, 720)  # Increasing the frame length
    ret = cap.set(4, 720)  # Increasing the frame width

    ret, background = cap.read()

while (cap.isOpened()):

    ret, img = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hsv values
    lower_green = np.array([36, 0, 0])
    upper_green = np.array([86, 255, 255])

    mask1 = cv2.inRange(hsv, lower_green, upper_green)  # seperating the cloak part

    lower_green = np.array([36, 0, 0])
    upper_green = np.array([86, 255, 255])

    mask2 = cv2.inRange(hsv, lower_green, upper_green)

    mask1 = mask1 + mask2  # OR (Combining)
# #remove  noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,
                             np.ones((3, 3), np.uint8), iterations=2)

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,
                             np.ones((3, 3), np.uint8), iterations=1)

# mask2 --> Everything except cloak
    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(background, background,
                           mask=mask1)  # used for segmentation
    # used to substitute the cloak part
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow("Got yaa", final_output)

    if cv2.waitKey(1) == 13:  # Ascii code for enter key

        break

cap.release()
cv2.destroyAllWindows()
