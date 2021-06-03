import cv2
import os
import operator
import matplotlib.pyplot as plt
import numpy as np

def hist_computation(image):
    hist, _ = np.histogram(image, bins=256)
        
    return hist

def Compare_Histo(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))

    return intersection        
    
    
# path = "DataSet/images/IMG_2866.jpg"
# path1 = "IMG_4184.jpg"

# image1 = cv2.imread(path)
# image2 = cv2.imread(path1)

# hist1 = hist_computation(image1)
# hist2 = hist_computation(image2)
# val, val1 = Compare_Histo(hist1, hist2)
# print(val1)
