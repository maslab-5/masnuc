'''
import cv2
import numpy as np

img = cv2.imread("GroundWithPlatform.png")
img = cv2.resize(img,(0,0),fx=0.4,fy=0.4)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([100,100,100])
upper_blue = np.array([130,255,255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

result = cv2.bitwise_and(img,img,mask)

cv2.imshow("test",result)
cv2.imshow("mask",mask)
cv2.waitKey()
'''

import cv2
import numpy as np

# Read the image
image = cv2.imread('GroundWithPlatform.png')

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for the blue color in HSV
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask for the blue color
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the bounding box of the largest contour (assumed to be the blue line)
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Keep the portion of the image under the blue line
    result = image[y:y + h, :]

    # Display the result
    cv2.imshow('Portion Under Blue Line', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No blue line found in the image.")
