# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 01:49:37 2021

@author: My Lap
"""
from helper_Function import *
import sqlite3
import os
from RGB_CBIR import *

def search (path2,table,method):
    # TODO: ADD OTHER IF COND. FOR METHODS
    img_paths=[]
    image2 = cv2.imread(path2)
    if (method=="RGB_MEAN"):
        vals2 = RGB_MEAN(image2) 
    for i in range(len(table)):
      vals1=stringToList(table[i][2])
      diff = abs(numpy.mean((vals1 - vals2)))
      if diff <2:
          img_paths.append(table[i][1])
 
    return img_paths 

path2=r'E:\\4th CSE\\2nd Term\\MM\\DataSet/IMG_0595.JPG'
conn=sqlite3.connect("cbir4.db")
c=conn.cursor()
c.execute("SELECT * FROM IMGG")
table=c.fetchall()

print(search(path2,table,"RGB_MEAN")) 