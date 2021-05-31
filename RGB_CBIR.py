import cv2 
import os
import numpy

'''
Path of Dataset
'''
# path = os.getcwd()
# full_path = path + '/DataSet'
# Images = os.listdir(full_path)


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
            # results.append(BGR_Avg_Color)
            results[img] = BGR_Avg_Color     
    return results
    
# image = cv2.imread('DataSet\IMG_0595.JPG')              
# BGR_Avg_Color = RGB_MEAN(image)   
# print(BGR_Avg_Color) 


# Folder_path= 'DataSet'
# results = ImagesRGBData(Folder_path)
# print(results)