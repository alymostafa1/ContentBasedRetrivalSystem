from __future__ import division
from __future__ import print_function
import cv2
import os
import operator
import matplotlib.pyplot as plt
from imutils import paths
import numpy as np

Allimages = []  # All images in the dataset
similarImages = []  # Images that have similar histogram to the source image
histvalues = []   #Array having the histogram values of all images in database

def hist_computation(image):
    hist, _ = np.histogram(image, bins=256)
        
    return hist

def Compare_Histo(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))

    return intersection       

def Read_All_Images(path):  # Function to read all images in a folder to simulate a database
    imagePaths = list(paths.list_images(path))
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        Allimages.append(image)

    return Allimages  # Array containing all images in the database


def hist_computation_HSV(image):    #Function to calcualte the histogram of given image    

    hsv_base = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    hist_base = cv2.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    return hist_base    #returns the value of the histogram

def Compare_Histo_HSV(hist_base, hist_test1):  # Function that compares the histograms of the soure image and test image

    base_test1 = cv2.compareHist(hist_base, hist_test1, 0)
    if base_test1 >= 0.75:  # if similarity greater than or equal 0.75 then put the test image in the SimilarImages array
        return 1, base_test1
    else:
        return 0, base_test1
    
    
# path = "DataSet/images/IMG_2866.jpg"
# path1 = "IMG_4184.jpg"

# image1 = cv2.imread(path)
# image2 = cv2.imread(path1)

# hist1 = hist_computation(image1)
# hist2 = hist_computation(image2)
# val, val1 = Compare_Histo(hist1, hist2)
# print(val1)
