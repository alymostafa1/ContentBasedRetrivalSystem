from helper_Function import *
import sqlite3
import os
from RGB_CBIR import *
from Img_Slicer import *

'''
##############################################################################
 id   |     path      |      RGB-Mean     |      Hist     | Sliced-Hist
##############################################################################
'''

def TableRetrieve(method, table):
    vals1 = []
    
    for i in range(len(table)):             
      if method == "RGB_MEAN":
        vals1.append(stringToList(table[i][2]))
      elif method == "Histogram":
        vals1.append(stringToList(table[i][3]))   
      elif method == "SLiced-Histogram":
          vals1.append(stringToList(table[i][4]))                                   
    return vals1



def ImageSearch (path,conn,method):
    # TODO: ADD OTHER IF COND. FOR METHODS

    diffL=[10000]    
    diffL_2=[0]    
    image = cv2.imread(path)        
    c=conn.cursor()
    c.execute("SELECT * FROM IMG")
    table_img=c.fetchall() 
    vals1 = TableRetrieve(method, table_img)      # Array 
    
    if method == "RGB_MEAN":
        vals2 = RGB_MEAN(image)  #array of 1 
    elif method == "Histogram":
        vals2 = hist_computation(image)
    elif method == "SLiced-Histogram":
        vals2 = Slicer_hist(image,divisions = 16)
        
        
    for i, val in enumerate(vals1):
        if method == "RGB_MEAN":
            Val, diff = RGBcompare(val , vals2)
            if (Val):
                if (diff < min(diffL)):
                    diffL.append(diff)
                    img_path=table[i][1]
            
        if method == "Histogram":
            Val, diff = Compare_Histo(val, vals2)            
            if (Val):
                if (diff > max(diffL_2)):
                    diffL_2.append(diff)
                    img_path = table[i][1]
                 
    return img_path    
   

      

path=r'C:/Users/Aly EL-kady/Desktop/IMG_2866.JPG'
conn=sqlite3.connect("multimedia.db")
print(ImageSearch(path,conn,"SLiced-Histogram")) 

#c=conn.cursor()
#c.execute("SELECT * FROM IMGG")
# table=c.fetchall()
