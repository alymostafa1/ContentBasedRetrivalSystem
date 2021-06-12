import sqlite3
import os
from CBIR_RGB import *
from CBIR_Layout import *
import math
import cv2
from CBVR import *



'''
##############################################################################
 id   |     path      |      RGB-Mean     |      Hist     | Sliced-Hist
##############################################################################
'''


def Array2String(Array):
    sep=' '
    strings=[]
    for element in Array:
      strings.append(str(element))    
    s=sep.join(strings)
    return(s)

def stringToList(string):
    p=[]
    string=string[1:len(string)-1]
    string=string.replace('  ',' ')
    listRes = list(string.split(" "))
    for _ in range(listRes.count('')):        
        listRes.remove('')
        
    for element in listRes:
          element_=float(element)
          p.append(element_)  
    return p

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

def video_search(path,conn,method):
    ##input keyframes
    c= conn.cursor()
    c.execute("SELECT * FROM VIDEO")
    numOfvideos = len(c.fetchall())
    in_keyframes= keyframeDetection(path,0.5)
    
    if method=="RGB_MEAN":
        in_avg_rgb=np.zeros((len(in_keyframes),3))
        diff=np.zeros((numOfvideos,1))
        for i in range(len(in_keyframes)):
            in_avg_rgb[i] = RGB_MEAN(in_keyframes[i]) ############rgb input video
            
        for i in range(numOfvideos):
            sql ="SELECT avg_rgb FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id AND V.id='%d'"% (i+1)
            c.execute(sql)
            t= c.fetchall()
            db_avg_rgb=np.zeros((len(t),3))
            for h in range(len(t)):
                db_avg_rgb[h]=stringToList(t[h][0]) ############rgb video[i] in db
            for j in range(len(in_keyframes)):
                #for k in range(len(t)): 
                diff[i]= np.min(abs(np.mean((in_avg_rgb[j]-db_avg_rgb),axis=1)))
                #diff[i]=cv.compareHist(hist_base, hist_test1, 0)
                    
        video_index=np.argmin(diff)
        #c.execute("SELECT path FROM VIDEO as V WHERE V.id='%d'"% (video_index))
        c.execute("SELECT * FROM VIDEO")
        t= c.fetchall()
        video_path=t[video_index][1]
        return video_path
    
    elif method=="HIST":
        in_histo=np.zeros((len(in_keyframes),256))
        diff=np.zeros((numOfvideos,len(in_keyframes)))
        fdiff=np.zeros((numOfvideos,1))
        for i in range(len(in_keyframes)):
            in_histo[i] = hist_computation(in_keyframes[i]) ############hist input video
            
        for i in range(numOfvideos):
            sql ="SELECT hist_bg FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id AND V.id='%d'"% (i+1)
            c.execute(sql)
            t= c.fetchall()
            db_histo=np.zeros((len(t),256))
            for h in range(len(t)):
                db_histo[h]=stringToList(t[h][0]) ############histo video[i] in db
            for j in range(len(in_keyframes)):
                temp=0
                for k in range(len(t)):
                    correlation = Compare_Histo(in_histo[j], db_histo[k])
                    if correlation>temp and correlation>0.6:
                        temp=correlation
                diff[i,j]=temp       
        fdiff=np.mean(diff,axis=1)    
                    
        video_index=np.argmax(fdiff)
        #c.execute("SELECT path FROM VIDEO as V WHERE V.id='%d'"% (video_index))
        c.execute("SELECT * FROM VIDEO")
        t= c.fetchall()
        video_path=t[video_index][1]
        return video_path
        
    ##elif method=="FEATURES_EXTR":
        #sql ="SELECT KF.path,avg_rgb FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id"
        #c.execute(sql) 
        #rows = c.fetchall()



def ImageSearch (path,conn,method):

    diffL=[10000]    
    diffL_2=[0]  
    diffL_3=[]
    img = cv2.imread(path)
    image = cv2.resize(img, (200,200), interpolation = cv2.INTER_AREA)        
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
            # if (Val):
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


# path=r'H:\kolya\4th year\2nd Term\Multimedia\Images/40-200x300.jpg'

# conn=sqlite3.connect("multimedia.db")
# print(ImageSearch(path,conn,"SLiced-Histogram")) 
# print(ImageSearch(path,conn,"Histogram")) 
# print(ImageSearch(path,conn,"RGB_MEAN")) 
#c=conn.cursor()
#c.execute("SELECT * FROM IMGG")
# table=c.fetchall()




#path1=r'D:\ContentBasedRetrivalSystem\DataSet\Videos\skating.mp4'
#conn=sqlite3.connect("multimedia.db")
#c= conn.cursor()
#videopath=video_search(path1,conn,"HIST")
#print(videopath)


#path1=r'D:\ContentBasedRetrivalSystem\DataSet\Videos\skating.mp4'
#conn=sqlite3.connect("multimedia.db")
#c= conn.cursor()
#videopath=video_search(path1,conn,"HIST")
#print(videopath)