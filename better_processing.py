import cv2
import numpy as np

image = cv2.imread('red.png')

height = image.shape[0]
width = image.shape[1]

dimensions = (int(0.1 * width), int(0.1 * height))
scaled_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA) #INTER_LINEAR

kernel = (7,7)
sigmaX = 0
scaled_image = cv2.GaussianBlur(scaled_image, kernel, sigmaX)

hsv = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2HSV)
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
cmask = cv2.bitwise_or(mask1, mask2)

contours, _ = cv2.findContours(cmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.rectangle(scaled_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

output_path = 'processed_red.png'
cv2.imwrite(output_path, scaled_image)
output_path