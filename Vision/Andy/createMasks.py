import numpy as np
import cv2

def greenMask(hsv):
    # Define a range for green color in HSV
    lower_green = np.array([35, 20, 20])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_mask = np.float32(green_mask)

    # Perform erosion to remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(green_mask, kernel, iterations=2)

    # Perform dilation to bring back the original size of the white regions
    processed_green_mask = cv2.dilate(erosion, kernel, iterations=5)
    processed_green_mask = processed_green_mask.astype(np.uint8)

    return processed_green_mask

def redMask(hsv):
    # Define a range for green color in HSV
    lower_red = np.array([35, 20, 20])
    upper_red = np.array([90, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red_mask = np.float32(red_mask)

    # Perform erosion to remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(red_mask, kernel, iterations=2)

    # Perform dilation to bring back the original size of the white regions
    processed_red_mask = cv2.dilate(erosion, kernel, iterations=5)
    processed_red_mask = processed_red_mask.astype(np.uint8)

    return processed_red_mask
