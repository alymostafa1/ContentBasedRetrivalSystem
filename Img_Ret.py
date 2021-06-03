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
    
    if intersection > 0.98 and intersection <= 1: 
        return 1, intersection
    else:
        return 1, intersection        
    

# def Compare_Histo(image1, image2):
#     hist1 = hist_computation(image1)
#     hist2 = hist_computation(image2)
    
#     # base_test1 = cv2.compareHist(hist1, hist2, 0)
#     best_test1 = (hist1 - hist2)
#     return (best_test1)
#     # if :
        
#     #     return 1, base_test1
#     # else:
#     #     return 0, base_test1    
    
    
    

# def Hist_Search(path, image_name):    
#     index = {} # Dic to store the image name and it's Hist
#     results = {} 
#     path_2 = os.getcwd()
#     full_path = path_2 + '/DataSet'    
#     Images = os.listdir(full_path)
#     for img in Images: 
#         img_path = 'DataSet/' + img
#         image = cv2.imread(img_path)
        
#         ## Resisizing Image size
#         width = int(image.shape[1] * 40 / 100)
#         height = int(image.shape[0] * 40 / 100)
        
#         ## dsize
#         dsize = (width, height)
        
#         ## Resize
#         image = cv2.resize(image, dsize)
#         # cv2.imshow('OriginalImage', image)
        
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

#         hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],[0, 256, 0, 256, 0, 256])
#         hist = cv2.normalize(hist, hist).flatten()
#         index[img] = hist
        
#     for (k, hist) in index.items():
#     		d = cv2.compareHist(index[image_name], hist, cv2.HISTCMP_CORREL)
#     		results[k] = d
    
#     # results = sorted([(v, k) for (k, v) in results.items()])
#     results = dict(sorted( results.items(),key=operator.itemgetter(1), reverse=True))
    
#     return results


# path = "DataSet/images/IMG_2866.jpg"
# path1 = "IMG_4184.jpg"

# image1 = cv2.imread(path)
# image2 = cv2.imread(path1)

# hist1 = hist_computation(image1)
# hist2 = hist_computation(image2)
# val, val1 = Compare_Histo(hist1, hist2)
# print(val1)
