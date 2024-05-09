import cv2
import numpy as np
import pyautogui
from robot.api.deco import keyword

class MyCompareImage:
    @keyword('My Find Image')
    def my_find_image(self, small_image_path, large_image_path, threshold=0.8):
        # Load the two images
        img1 = cv2.imread(small_image_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(large_image_path, cv2.IMREAD_GRAYSCALE)

        # Use template matching to find the location of the small image within the large image
        res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # Check if a match was found
        if len(loc[0]) > 0:
            return True
        return False

    @keyword('My Click On Image')
    def my_click_image(self,small_image_path, large_image_path, threshold=0.8):
        # Load the two images
        img1 = cv2.imread(small_image_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(large_image_path, cv2.IMREAD_GRAYSCALE)

        # Use template matching to find the location of the small image within the large image
        res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # Check if a match was found
        if len(loc[0]) > 0:
            # Get the top-left corner of the matched region
            top_left = (loc[1][0], loc[0][0])

            # Calculate the average of all matched locations
            avg_x = int(np.mean(loc[1]) + img1.shape[1] // 2)
            avg_y = int(np.mean(loc[0]) + img1.shape[0] // 2)

            # Perform the click action at the center of the matched region
            pyautogui.click(avg_x, avg_y)

            return True
        else:
            return False