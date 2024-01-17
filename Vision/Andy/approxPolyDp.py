import numpy as np
import cv2
import createMasks

def approxPolyDP(img):
    # Load and blur image
    # img = cv2.imread('../img/Green.png')
    height, width = img.shape[:2]
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (int(0.5 * width), int(0.5 * height)))
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Creating all black image
    # zero = np.zeros((height+2, width+2), np.uint8)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get masks
    processed_green_mask = createMasks.greenMask(hsv)
    processed_red_mask = createMasks.redMask(hsv)

    # Get and combine contours
    green_contours, _ = cv2.findContours(processed_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    red_contours, _ = cv2.findContours(processed_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = green_contours + red_contours

    # Identifying Shapes
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02* cv2.arcLength(contour, True), True)
        if cv2.arcLength(approx, closed=True) > 800:
            print(approx)
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            angle = rect[-1]
            print (angle,"deg")

            cv2.drawContours(img, [box], 0, (255, 0, 0), 10)
            # cv2.drawContours(img, [approx], 0, (0, 255, 0), 10)

    # Show images
    # cv2.imshow('Mask',processed_green_mask)
    # cv2.imshow('Zero',zero)
    # cv2.imshow('Image',img)
    # cv2.waitKey()

    # https://medium.com/simply-dev/detecting-geometrical-shapes-in-an-image-using-opencv-bad67c40174f

cap = cv2.VideoCapture('/Vision/img/red.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = approxPolyDP(frame)
    out.write(processed_frame)

    cv2.imshow('frame', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
