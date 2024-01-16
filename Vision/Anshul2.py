import cv2
import numpy as np

def process_frame(frame):
    height, width = frame.shape[:2]
    dimensions = (int(0.1 * width), int(0.1 * height))
    scaled_frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    kernel = (7, 7)
    sigmaX = 0
    blurred = cv2.GaussianBlur(scaled_frame, kernel, sigmaX)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    cmask = cv2.bitwise_or(mask1, mask2)
    contours = cv2.findContours(cmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        origin = (x, y)
        endpoint = (x + w, y + h)
        cv2.rectangle(scaled_frame, origin, endpoint, (255, 0, 0), 2)

    return scaled_frame

video_input = cv2.VideoCapture('img/red.MOV') 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
output = cv2.VideoWriter('tests/video/output_red.MOV', fourcc, 20.0, (640, 480)) 

while True:
    ret, frame = video_input.read()
    if not ret:
        break

    processed_frame = process_frame(frame)
    output.write(processed_frame)

video_input.release()
output.release()
cv2.destroyAllWindows()
