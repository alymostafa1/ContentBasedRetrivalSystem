from __future__ import division
from __future__ import print_function
import cv2
import cv2 as cv
from imutils import paths

Allimages = []  # All images in the dataset
similarImages = []  # Images that have similar histogram to the source image
histvalues = []   #Array having the histogram values of all images in database


def Read_All_Images(path):  # Function to read all images in a folder to simulate a database
    imagePaths = list(paths.list_images(path))
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        Allimages.append(image)

    return Allimages  # Array containing all images in the database


def hist_computation(image):    #Function to calcualte the histogram of given image    

    hsv_base = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    return hist_base    #returns the value of the histogram


def Compare_Histo(hist_base, hist_test1):  # Function that compares the histograms of the soure image and test image

    base_test1 = cv.compareHist(hist_base, hist_test1, 0)
    if base_test1 >= 0.75:  # if similarity greater than or equal 0.75 then put the test image in the SimilarImages array
        return 1, base_test1
    else:
        return 0, base_test1


# def main():     #Made for testing the algorithm
#    src = cv2.imread("C:/Users/Aly EL-kady/Desktop/image.JPG")  #source image that we need to find similar images to it
#     Allimages = Read_All_Images('DataSet/Images')
#    histsrc = hist_computation(src)

     # for image in Allimages:  # loop to compare all images in the dataset with the source image
     #    histvalues.append(hist_computation(image))


#     for x in range(0,len(histvalues)):      #Function to compare the histogram source image with all hisgrams of images in the dataset
#         if Compare_Histo(histsrc, histvalues[x])==1:
#             similarImages.append(Allimages[x])      #if histogram value is similar to the soure image copy the image to similar images array


#     for image in similarImages:  # loop to show the captured images
#         cv.imshow('calcHist Demo', image)
#         cv.waitKey()


# if __name__ == '__main__':
#     main()
