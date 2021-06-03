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

def TableRetrieve(method, table1,table2):
    vals1 = []
    vals9=[]
    
    for i in range(len(table1)):             
      if method == "RGB_MEAN":
        vals1.append(stringToList(table1[i][2]))
      elif method == "Histogram":
        vals1.append(stringToList(table1[i][3]))   
      elif method == "SLiced-Histogram":
          for j in range (0,16):
             vals9.append(stringToList(table2[(i*16)+j][2]))
          vals1.append(vals9)
          vals9=[]
    return vals1



def ImageSearch (path,conn,method):
    # TODO: ADD OTHER IF COND. FOR METHODS

    diffL=[10000]    
    diffL_2=[0]  
    diffL_3=[]
    image = cv2.imread(path)        
    c=conn.cursor()
    c.execute("SELECT * FROM IMG")
    table_img=c.fetchall()
    
    v=conn.cursor()
    v.execute("SELECT * FROM SLICES")
    table_slice=v.fetchall() 
    
    
    
    vals1 = TableRetrieve(method, table_img,table_slice)      # Array 
    
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
                    img_path=table_img[i][1]
            
        if method == "Histogram":
            diff = Compare_Histo(val, vals2)            
            if (diff > max(diffL_2)):
                    diffL_2.append(diff)
                    img_path = table_img[i][1]
                    
                    
                    
        if method=="SLiced-Histogram":
            summ=0
            for j in range (0,16):
                diff = Compare_Histo(val[j], vals2[j])
                summ+=diff
                
            summ=summ/16
            diffL_3.append(summ)
    if (method=="SLiced-Histogram"):
        
        Max_index=diffL_3.index(max(diffL_3))
        img_path=table_img[Max_index][1]
    
    return img_path


            
            
                
    

path=r'E:\4th CSE\2nd Term\MM\DataSet\Images\image.JPG'
conn=sqlite3.connect("multimedia.db")
print(ImageSearch(path,conn,"SLiced-Histogram")) 
print(ImageSearch(path,conn,"Histogram")) 
print(ImageSearch(path,conn,"RGB_MEAN")) 
#c=conn.cursor()
#c.execute("SELECT * FROM IMGG")
# table=c.fetchall()
