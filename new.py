import cv2
import numpy as np

def colorBalance(img_path):
    b, g, r = cv2.split(img_path)
    B = np.mean(b)
    G = np.mean(g)
    R = np.mean(r)
    K = (R + G + B) / 3
    Kb = K / B
    Kg = K / G
    Kr = K / R
    cv2.addWeighted(b, Kb, 0, 0, 0, b)
    cv2.addWeighted(g, Kg, 0, 0, 0, g)
    cv2.addWeighted(r, Kr, 0, 0, 0, r)
    merged = cv2.merge([b,g,r])
    return merged


cap = cv2.VideoCapture('C:/Users/DELL/Documents/endoscope/endoscope_PyQt5/endovideo.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('image', colorBalance(frame))
    # cv2.imshow('image', frame)
    k = cv2.waitKey(20)  
    if (k & 0xff == ord('q')):
        break  

cap.release()
cv2.destoryALLWindows()