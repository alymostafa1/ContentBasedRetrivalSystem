import cv2
import os
import operator




def Hist_Search(path, image_name):    
    index = {} # Dic to store the image name and it's Hist
    results = {} 
    path_2 = os.getcwd()
    full_path = path_2 + '/DataSet'
    Images = os.listdir(full_path)
    for img in Images: 
        img_path = path + '/' + img
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # cv2.imshow("Image",image)
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],[0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        index[img] = hist
        
    for (k, hist) in index.items():
    		d = cv2.compareHist(index[image_name], hist, cv2.HISTCMP_CORREL)
    		results[k] = d
    
    # results = sorted([(v, k) for (k, v) in results.items()])
    results = dict(sorted( results.items(),key=operator.itemgetter(1), reverse=True))
    
    return results


path = "H:\kolya\4th year\2nd Term\Multimedia\ContentBasedRetrivalSystem\DataSet"
image_name = "IMG_4185.JPG"

Hist_Search(path, image_name)