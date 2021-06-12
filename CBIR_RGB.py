import cv2 
import os
import numpy


def RGBcompare(vals1, vals2):
    # vals1 = RGB_MEAN(image1)
    # vals2 = RGB_MEAN(image2)
    
    diff = abs(numpy.mean((vals1 - vals2)))
    if diff < 10:
        return 1, diff # IMAGE FOUND
    else:
        return 0, diff # IMAGE NOT FOUND

def RGB_MEAN(image):
    avg_color_per_row = numpy.average(image, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)    
    return avg_color #BGR Values


def ImagesRGBData(path):
    '''
    Input: Path of the images folder 
    output: Dict with every image assigned with the Avg color
    '''
    results = {}
    resultss = []
    Images = os.listdir(path)
    for img in Images: 
            image_path = path + '/' + img
            image = cv2.imread(image_path)
            BGR_Avg_Color = RGB_MEAN(image) 
            results[img] = BGR_Avg_Color     
    return results
    
# image = cv2.imread('DataSet\images\IMG_0595.JPG')              
# BGR_Avg_Color = RGB_MEAN(image)   
# print(BGR_Avg_Color) 


# Folder_path= 'DataSet\images\\Images'
# results = ImagesRGBData(Folder_path)
# print(results)

# image1 = cv2.imread('DataSet\images\\IMG_4184.JPG')
# image2 = cv2.imread('DataSet\images\\IMG_4185.JPG')
# different = RGBcompare(image1, image2)