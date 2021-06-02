import cv2  
import numpy as np


from histogram import *

def sliceImage(Image_path,divisions):

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
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    new_height = height/np.sqrt(divisions)
    new_width = width/np.sqrt(divisions)
    d1_1, d2_2= gray_image.shape
    
    pre_img = np.split(gray_image, (d2_2/new_width))  
    img = []
    
    for arr in pre_img:
        img.extend(np.split(arr, arr.shape[1]/(new_width), axis=1))
        
    # for i in range(len(img)):
    #     new_image_path = "Image" + str(i)  + '.jpg'
    #     cv2.imwrite(new_image_path, img[i]) 
    return img



# divisions= 16
# path="image.jpg"
# sliced_img = sliceImage(path,divisions)

def Slicer_hist(Image_path,divisions):
    Dict = {}
    image_hist = []
    images = sliceImage(Image_path,divisions)
    
    for image in images: 
        image_hist.append(hist_computation(image))
        
    Dict[Image_path] = image_hist           
    return Dict

# divisions= 16
# path="DataSet\Images\image.jpg"
# Image_Hist = Slicer_hist(path,divisions)
        
        
    
    
    

