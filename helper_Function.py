# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:06:38 2021

@author: My Lap
"""
import math

def Array2String(Array):
    sep=','
    strings=[]
    for element in Array:
      strings.append(str(element))    
    s=sep.join(strings)
    return(s)


# numbers=Array2String([1,2,3,5,6])
# print (numbers)

def stringToList(string):
    p=[]
    string=string[1:len(string)-1]
    string=string.replace('  ',' ')
    listRes = list(string.split(" "))
    for _ in range(listRes.count('')):
        
        
    # if (listRes.count('')>0): 
        listRes.remove('')
        
    for element in listRes:
          element_=float(element)
          p.append(element_)  
    return p


# strA = "[1 2 3 4 5]"
# print(stringToList(strA))
