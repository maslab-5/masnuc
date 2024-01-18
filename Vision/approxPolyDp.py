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
    erosion = cv2.erode(green_mask, kernel, iterations=3)

    # Perform dilation to bring back the original size of the white regions
    processed_green_mask = cv2.dilate(erosion, kernel, iterations=5)
    processed_green_mask = processed_green_mask.astype(np.uint8)

    return processed_green_mask

def redMask(hsv):
    # Define a range for red color in HSV
    # 150 to 180
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    red_mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    # 0 to 30
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([20, 255, 255])
    red_mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine masks
    red_mask = cv2.bitwise_or(red_mask_1, red_mask_2)
    red_mask = np.float32(red_mask)

    # Perform erosion to remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(red_mask, kernel, iterations=4)

    # Perform dilation to bring back the original size of the white regions
    processed_red_mask = cv2.dilate(erosion, kernel, iterations=4)
    processed_red_mask = processed_red_mask.astype(np.uint8)

    return processed_red_mask

def approxPolyDP(img):
    # Load and blur image
    # img = cv2.imread('../img/GreenRedGreen.png')
    height, width = img.shape[:2]
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.resize(img, (int(0.5 * width), int(0.5 * height)))
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # Creating all black image
    # zero = np.zeros((height+2, width+2), np.uint8)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get masks
    processed_green_mask = greenMask(hsv)
    processed_red_mask = redMask(hsv)

    # Get and combine contours
    green_contours, _ = cv2.findContours(processed_green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    red_contours, _ = cv2.findContours(processed_red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = green_contours + red_contours

    # Identifying Shapes
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if cv2.arcLength(approx, closed=True) > 500:
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            angle = rect[-1]
            print (angle,"deg")

            cv2.drawContours(img, [box], 0, (255, 0, 0), 5)
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 10)

    return img

    # Show images
    # cv2.imshow('Red',processed_red_mask)
    # cv2.imshow('Green',processed_green_mask)
    # cv2.imshow('Zero',zero)
    # cv2.imshow('Image',img)
    # cv2.waitKey()

    # https://medium.com/simply-dev/detecting-geometrical-shapes-in-an-image-using-opencv-bad67c40174f

# Video
cap = cv2.VideoCapture('Videos/IMG_6320.mp4')

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = approxPolyDP(frame)
    # out.write(processed_frame)

    cv2.imshow('Fuck', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
