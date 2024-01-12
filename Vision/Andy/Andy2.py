import cv2
import numpy as np

img = cv2.imread("GroundWithPlatform.png")
img = cv2.resize(img,(0,0),fx=0.4,fy=0.4)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([100,100,100])
upper_blue = np.array([130,255,255])
hsv = cv2.inRange(hsv, lower_blue, upper_blue)

print(np.where(hsv))

cv2.imshow("test",hsv)
cv2.waitKey()
