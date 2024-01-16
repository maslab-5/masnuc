import numpy as np
import cv2
import CreateMasks

# Load and blur image
img = cv2.imread('../img/Green.png')
height, width = img.shape[:2]
img = cv2.GaussianBlur(img, (3, 3), 0)
img = cv2.resize(img, (int(0.5 * width), int(0.5 * height)))
img = cv2.GaussianBlur(img, (3, 3), 0)

# Creating all black image
h, w, _ = img.shape
zero = np.zeros((h+2, w+2), np.uint8)

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Get masks
processed_green_mask = CreateMasks.greenMask(hsv)
processed_red_mask = CreateMasks.redMask(hsv)

# Get and combine contours
green_contours, _ = cv2.findContours(processed_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
red_contours, _ = cv2.findContours(processed_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contours = green_contours + red_contours

# Identifying Shapes
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02* cv2.arcLength(contour, True), True)
    if cv2.arcLength(approx, closed=True) > 800:
        print("Sqaure")
        print(approx)
        rect = cv2.minAreaRect(approx)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        angle = rect[-1]
        print (angle,"deg")

        cv2.drawContours(img, [box], 0, (255, 0, 0), 10)
        cv2.drawContours(img, [approx], 0, (0, 255, 0), 10)

# Show images
# cv2.imshow('Mask',processed_green_mask)
# cv2.imshow('Zero',zero)
cv2.imshow('Image',img)
cv2.waitKey()

# https://medium.com/simply-dev/detecting-geometrical-shapes-in-an-image-using-opencv-bad67c40174f
