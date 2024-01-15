import numpy as np
import cv2

# Load image
img = cv2.imread('Green.png')

height, width = img.shape[:2]
scaled_image = cv2.GaussianBlur(img, (3, 3), 0)

scaled_image = cv2.resize(scaled_image, (int(0.5 * width), int(0.5 * height)))

img = cv2.GaussianBlur(scaled_image, (3, 3), 0)

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

# Threshhold
# _, thrash = cv2.threshold(processed_green_mask, 240 , 255, cv2.CHAIN_APPROX_NONE)
# thrash = thrash.astype(np.uint8)
processed_green_mask = processed_green_mask.astype(np.uint8)
contours , _ = cv2.findContours(processed_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Creating all black image
h,w = processed_green_mask.shape
zero = np.zeros((h+2, w+2), np.uint8)

# Identifying Shapes
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02* cv2.arcLength(contour, True), True)
    if cv2.arcLength(contour, closed=True) > 800:
        cv2.drawContours(zero, [approx], 0, (255, 0, 0), 1)
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if not(aspectRatio >= 0.95 and aspectRatio < 1.05):
            print("not a sqaure")
        #     cv2.drawContours(img, [approx], 0, (255, 0, 0), 10)
        #     x = approx.ravel()[0]
        #     y = approx.ravel()[1] - 5

# Detect corners using Shi-Tomasi algorithm
zero = cv2.GaussianBlur(zero, (5, 5), 0)
corners = cv2.goodFeaturesToTrack(zero, maxCorners=16, qualityLevel=0.10, minDistance=100)

# Convert corners to integer coordinates
corners = np.intp(corners)

# Draw circles around detected corners
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(zero, (x, y),10, 255, -1)

# Show images
# cv2.imshow('Mask',processed_green_mask)
cv2.imshow('Zero',zero)
# cv2.imshow('Image',img)
cv2.waitKey()

# https://medium.com/simply-dev/detecting-geometrical-shapes-in-an-image-using-opencv-bad67c40174f
