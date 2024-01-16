import numpy as np
import cv2
from helperFunctions import twoNeighbors
import createMasks

# Load and blur image
img = cv2.imread('Green.png')
height, width = img.shape[:2]
img = cv2.GaussianBlur(img, (3, 3), 0)
img = cv2.resize(img, (int(0.5 * width), int(0.5 * height)))
img = cv2.GaussianBlur(img, (3, 3), 0)

# Creating all black image
h, w, _ = img.shape
zero = np.zeros((h+2, w+2), np.uint8)

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

processed_green_mask = createMasks.greenMask(hsv)
# processed_red_mask = createMasks.redMask(hsv)

contours, _ = cv2.findContours(processed_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# red_contours, _ = cv2.findContours(processed_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# contours = tuple([green_contours[i] + red_contours[i] for i in range(len(green_contours))])

# Identifying Shapes
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02* cv2.arcLength(contour, True), True)
    if cv2.arcLength(approx, closed=True) > 800:
        cv2.drawContours(img, [approx], 0, (255, 0, 0), 1)
        # When work has to be done
        if len(approx) == 4:
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if not(aspectRatio >= 0.95 and aspectRatio < 1.05):
                print("Rectangle")
                # Detect corners using Shi-Tomasi algorithm
                zero = cv2.GaussianBlur(zero, (5, 5), 0)
                corners = cv2.goodFeaturesToTrack(zero, maxCorners=16, qualityLevel=0.10, minDistance=100)

                # Convert corners to integer coordinates
                corners = np.intp(corners)

                # Draw circles around detected corners
                for corner in corners:
                    x, y = corner.ravel()
                    cv2.circle(zero, (x, y),10, 255, -1)

                # What to do if mutliple blocks are aligned with each other
                # Create new contour(s) to draw
            else:
                print("Sqaure")
                print(approx)
                rect = cv2.minAreaRect(approx)
                box = cv2.boxPoints(rect)
                box = np.intp(box)

                angle = rect[-1]
                print (angle,"deg")

                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                # cv2.drawContours(img, [approx], 0, (255, 0, 0), 10)
        else:
            print("Not a square")
            # Detect corners using Shi-Tomasi algorithm
            zero = cv2.GaussianBlur(zero, (5, 5), 0)
            corners = cv2.goodFeaturesToTrack(zero, maxCorners=16, qualityLevel=0.10, minDistance=100)

            # Convert corners to integer coordinates
            corners = np.intp(corners)

            twoNeighbors(corners[0],corners)

            # Draw circles around detected corners
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(zero, (x, y),10, 255, -1)

            # What to do if mutliple blocks are touching each other
            # Create new countor(s) to draw
            # Iterate through every point, starting from the top, find two closest points, then see if angle and distance match up
            # If they do, reomve them from the list of points and draw a square using them
            # If a point is already removed, then don't draw the sqaure

# Show images
# cv2.imshow('Mask',processed_green_mask)
# cv2.imshow('Zero',zero)
cv2.imshow('Image',img)
cv2.waitKey()

# https://medium.com/simply-dev/detecting-geometrical-shapes-in-an-image-using-opencv-bad67c40174f
# x = approx.ravel()[0]
# y = approx.ravel()[1] - 5

# # Thresholding?
# _, thrash = cv2.threshold(processed_green_mask, 240 , 255, cv2.CHAIN_APPROX_NONE)
# thrash = thrash.astype(np.uint8)
