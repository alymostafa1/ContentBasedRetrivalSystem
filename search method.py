# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 01:49:37 2021

@author: My Lap
"""
from helper_Function import *
import sqlite3
import os
from RGB_CBIR import *

def search (path2,conn,method):
    # TODO: ADD OTHER IF COND. FOR METHODS
    diffL=[]
    c=conn.cursor()
    c.execute("SELECT * FROM IMG")
    table=c.fetchall()
    image2 = cv2.imread(path2)
    if (method=="RGB_MEAN"):
        vals2 = RGB_MEAN(image2) 
    for i in range(len(table)):
      vals1=stringToList(table[i][2])
      diff = abs(numpy.mean((vals1 - vals2)))
      diffL.append(diff)
      if(min(diffL)):
          img_path=table[i][1]
 
    return img_path 

path2=r'E:\4th CSE\2nd Term\MM\DataSet\IMG_2866.JPG'
conn=sqlite3.connect("multimedia.db")
print(search(path2,conn,"RGB_MEAN")) 

#c=conn.cursor()
#c.execute("SELECT * FROM IMGG")
# table=c.fetchall()
