import sqlite3
import cv2
from CBVR import *
from RGB_CBIR import *
from helper_Function import *
from Img_Ret import *


def video_search(path,conn,method):
    ##input keyframes
    c= conn.cursor()
    c.execute("SELECT count(*) FROM VIDEO")
    numOfvideos = len(c.fetchall())
    in_keyframes= keyframeDetection(path,0.5)
    
    if (method=="RGB_MEAN"):
        in_avg_rgb=np.zeros((len(in_keyframes),3))
        diff=np.zeros((numOfvideos,1))
        for i in range(len(in_keyframes)):
            in_avg_rgb[i] = RGB_MEAN(in_keyframes[i]) ############rgb input video
            
        for i in range(numOfvideos):
            sql ="SELECT avg_rgb FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id AND V.id='%d'"% (i)
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
        diff=np.zeros((numOfvideos,1))
        for i in range(len(in_keyframes)):
            in_histo[i] = hist_computation(in_keyframes[i]) ############hist input video
            
        for i in range(numOfvideos):
            sql ="SELECT hist_bg FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id AND V.id='%d'"% (i)
            c.execute(sql)
            t= c.fetchall()
            db_histo=np.zeros((len(t),256))
            for h in range(len(t)):
                db_histo[h]=stringToList(t[h][0]) ############histo video[i] in db
            for j in range(len(in_keyframes)):
                diff[i]= np.min(abs(np.mean((in_histo[j]-db_histo),axis=1)))
                    
        video_index=np.argmin(diff)
        #c.execute("SELECT path FROM VIDEO as V WHERE V.id='%d'"% (video_index))
        c.execute("SELECT * FROM VIDEO")
        t= c.fetchall()
        video_path=t[video_index][1]
        return video_path
        
    ##elif method=="FEATURES_EXTR":
        #sql ="SELECT KF.path,avg_rgb FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id"
        #c.execute(sql) 
        #rows = c.fetchall()

# path1='D:/ContentBasedRetrivalSystem/DataSet/Videos/acrobacia.mp4'
# conn=sqlite3.connect("multimedia.db")
# c= conn.cursor()
# videopath=video_search(path1,conn,"HIST")
# print(videopath)
        