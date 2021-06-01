# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:06:38 2021

@author: My Lap
"""

def Array2String(Array):
    sep=','
    strings=[]
    for element in Array:
      strings.append(str(element))
    
    s=sep.join(strings)
    return(s)


numbers=Array2String([1,2,3,5,6])
print (numbers)


def stringToList(string):
    p=[]
    listRes = list(string.split(","))
    for element in listRes:
       p.append(int(element))
    return p


strA = "1,2,3,4,5"
print(stringToList(strA))