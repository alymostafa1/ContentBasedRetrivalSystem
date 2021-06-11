import os
import cv2
import csv
import numpy as np
import time
import peakutils
import matplotlib.pyplot as plt

def print_diff(Array_1, Array_2):
    plt.subplot(311)
    plt.title('Original', fontsize=10)
    ax = plt.gca()
    ax.set_facecolor('xkcd:salmon')
    plt.plot(Array_1 , 'r')
    
    plt.subplot(312)
    plt.title('Base-Line removal',fontsize = 10 )
    ax = plt.gca()
    ax.set_facecolor('xkcd:sky blue')
    plt.plot(Array_2 , 'b')

    plt.subplot(313)
    plt.title('Diff', fontsize=10)
    ax = plt.gca()
    ax.set_facecolor('tab:olive')
    plt.plot((Array_1 - Array_2), 'g')  
    
def keyframeDetection(source, Thres):
    
    # keyframePath = dest +'/keyFrames'
    # if not os.path.exists(keyframePath):
    #         os.makedirs(keyframePath)
    
    lastdiffMag = []
    full_color = []
    lastFrame = None

    cap = cv2.VideoCapture(source)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  

    # Read until video is completed
    for i in range(length):
        ret, frame = cap.read()
        blur = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
        full_color.append(frame)
        if frame_number == 0:
            lastFrame = blur

        _diff = cv2.subtract(blur, lastFrame)
        diff_Num = cv2.countNonZero(_diff)
        lastdiffMag.append(diff_Num)
        lastFrame = blur

    cap.release()
    y = np.array(lastdiffMag)
    base = peakutils.baseline(y, 2)
    indices = peakutils.indexes(y - base, Thres, min_dist=1)
    out = []
    cnt = 1 
    # print_diff(y, base)
    for x in indices:
        # cv2.imwrite(os.path.join('DataSet/Videos', 'keyframe'+ str(cnt) +'.jpg'), full_color[x])
        cnt +=1
        out.append(full_color[x])
    cv2.destroyAllWindows()
    return np.array(out)
    
# out = keyframeDetection('DataSet/Videos/acrobacia.mp4', 0.5)
# x=0