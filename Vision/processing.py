import cv2
import numpy as np

# Load the image
image = cv2.imread('red.png')

# Scale the image to 10%
height, width = image.shape[:2]
scaled_image = cv2.resize(image, (int(0.1 * width), int(0.1 * height)))

scaled_image = cv2.GaussianBlur(scaled_image, (7, 7), 0)

# Convert the scaled image to the HSV color space
hsv = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2HSV)

# Define a lower and upper threshold for red color in HSV
lower_red1 = np.array([0, 100, 20])
upper_red1 = np.array([20, 255, 255])

lower_red2 = np.array([159, 100, 20])
upper_red2 = np.array([179, 255, 255])

# Create a binary mask for red regions
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

cmask = cv2.bitwise_or(mask1, mask2)


contours, _ = cv2.findContours(cmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(scaled_image, (x, y), (x + w, y + h), (255, 0, 0), 2)


# Display the original image, scaled image, and the result
cv2.imshow('Red Object Detection', scaled_image)
cv2.waitKey(0)
cv2.destroyAllWindows()