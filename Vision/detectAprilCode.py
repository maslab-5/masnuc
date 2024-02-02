import numpy as np
import cv2
from pupil_apriltags import Detector

at_detector = Detector(
   families="tag36h11",
   nthreads=1,
   quad_decimate=5,
   quad_sigma=0.2,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)

def aprilCode(img):
    # Detect tags
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(
            gray_img,
            estimate_tag_pose=False,
            camera_params=None,
            tag_size=None,
        )

    #Using corners of each tag to draw lines
    for tag in tags:
        corners = tag.corners
        center = tag.center
        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))
        corner_03 = (int(corners[2][0]), int(corners[2][1]))
        corner_04 = (int(corners[3][0]), int(corners[3][1]))

        cv2.circle(img, (center[0], center[1]), 7, (255, 0, 0), 4)

        cv2.line(img, (corner_01[0], corner_01[1]), (corner_02[0], corner_02[1]), (255, 0, 0), 4)
        cv2.line(img, (corner_02[0], corner_02[1]), (corner_03[0], corner_03[1]), (255, 0, 0), 4)
        cv2.line(img, (corner_03[0], corner_03[1]), (corner_04[0], corner_04[1]), (255, 0, 0), 4)
        cv2.line(img, (corner_04[0], corner_04[1]), (corner_01[0], corner_01[1]), (255, 0, 0), 4)

        # right_distance = np.linalg.norm(np.array(list(corner_02)) - np.array(list(corner_03)))
        # left_distance = np.linalg.norm(np.array(list(corner_04)) - np.array(list(corner_01)))
        # print(right_distance,left_distance)

    return img

cap = cv2.VideoCapture('Videos/IMG_3761.mp4')

first_frame = 1
while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = aprilCode(frame)

    cv2.imshow("Frame", processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample/blob/main/sample.py
