import os
import cv2
import csv
import numpy as np
import time
import peakutils

def keyframeDetection(source, dest, Thres, verbose=False):
    
    keyframePath = dest +'/keyFrames'
    if not os.path.exists(keyframePath):
            os.makedirs(keyframePath)

    cap = cv2.VideoCapture(source)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  
    if (cap.isOpened()== False):
        print("Error opening video file")

    lastfrm = []
    lastdiffMag = []
    full_color = []
    lastFrame = None
    
    # Read until video is completed
    for i in range(length):
        ret, frame = cap.read()
        blur_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
        lastfrm.append(frame_number)
        full_color.append(frame)
        if frame_number == 0:
            lastFrame = blur_gray

        diff = cv2.subtract(blur_gray, lastFrame)
        diffMag = cv2.countNonZero(diff)
        lastdiffMag.append(diffMag)
        lastFrame = blur_gray

    cap.release()
    y = np.array(lastdiffMag)
    base = peakutils.baseline(y, 2)
    indices = peakutils.indexes(y-base, Thres, min_dist=1)

    cnt = 1 
    for x in indices:
        cv2.imwrite(os.path.join(keyframePath , 'keyframe'+ str(cnt) +'.jpg'), full_color[x])
        cnt +=1
    cv2.destroyAllWindows()
    
keyframeDetection('C:/Users/Aly EL-kady/Desktop/acrobacia.mp4', 'C:/Users/Aly EL-kady/Desktop/Project', 0.5)