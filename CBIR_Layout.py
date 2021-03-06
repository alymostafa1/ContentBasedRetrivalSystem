import cv2  
import numpy as np
from CBIR_Hist import *


# from histogram import *
from CBIR_Layout import *

def sliceImage_Vect(Image_path,divisions):

    '''
    Original img
    '''
    img = cv2.imread(Image_path)
    height = img.shape[0]
    width = img.shape[1]
    
    '''
    Transforming into grey image 
    '''
    d1, d2, d3= img.shape
    
    # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray_image = img 
    
    new_height = height/np.sqrt(divisions)
    new_width = width/np.sqrt(divisions)
    d1_1, d2_2, d3_3 = gray_image.shape
    
    pre_img = np.split(gray_image, (d2_2/new_width))  
    img = []
    
    for arr in pre_img:
        img.extend(np.split(arr, arr.shape[1]/(new_width), axis=1))

        
    # for i in range(len(img)):
    #     new_image_path = "DataSet\Images\Image" + str(i)  + '.jpg'
    #     cv2.imwrite(new_image_path, img[i]) 
    return img

def SliceImage_X_Vect(image_input,divisions):
    
    '''
    Original img
    '''
    # img = cv2.imread(Image_path)
    img = image_input
    height = img.shape[0]
    width = img.shape[1]
    
    h_2 = height/np.sqrt(divisions)
    w_2 = width/np.sqrt(divisions)

    _img =[]
    
    #image cropping 
    i=0    
    x=0
    y=0
    
    for i in range(int(np.sqrt(divisions))):
        y=0
        for j in range(int(np.sqrt(divisions))):   
            image= img[ int(y): int(h_2+y), int(x) :int(w_2+x) , : ]
            # cv2.imwrite("image"+ str(i) + str(j) + ".jpg",image)
            y += h_2            
            _img.append(image)
        
        x += w_2
        
    return _img

'''
Test for Image Slicer
'''
# divisions= 16
# path="image.jpg"
# sliced_img = sliceImage(path,divisions)

'''
Test for Hist computation for sliced images
'''

def Slicer_hist(image_input,divisions):
    Dict = {}
    image_hist = []
    images = SliceImage_X_Vect(image_input,divisions)
    
    for image in images: 
        image_hist.append(hist_computation(image))
        
           
    return image_hist

# divisions= 16
# path="DataSet\Images\image.jpg"
# image = cv2.imread(path)
# Image_Hists = Slicer_hist(image,divisions)
        
        
    
    
    

