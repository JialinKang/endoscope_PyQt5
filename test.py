import cv2
import numpy as np


def undistort(frame):
    fx = 959.4900
    cx = 1059.5
    fy = 960.3653
    cy = 608.9216
    k1, k2, p1, p2, k3 = -0.3982, 0.1373, 0.0, 0.0, 0.0
 
    k = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    
    d = np.array([
        k1, k2, p1, p2, k3
    ])
    h, w = frame.shape[:2]
    mapx, mapy = cv2.initUndistortRectifyMap(k, d, None, k, (w, h), 5)
    return cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)


cap = cv2.VideoCapture('F:/endoscope/data/words.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('image', undistort(frame))
    # cv2.imshow('image', frame)
    k = cv2.waitKey(20)  
    if (k & 0xff == ord('q')):
        break  

cap.release()
cv2.destoryALLWindows()