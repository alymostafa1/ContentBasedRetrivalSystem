import sqlite3
import cv2
from CBVR import *
from RGB_CBIR import *
from helper_Function import *


def video_search(path,conn,method):
    ##input keyframes
    c= conn.cursor()
    c.execute("SELECT count(*) FROM VIDEO")
    numOfvideos = len(c.fetchall())
    in_keyframes= keyframeDetection('path','D:\ContentBasedRetrivalSystem\inputvideoFrames',0.5)
    
    if (method=="RGB_MEAN"):
        
        in_avg_rgb=np.zeros((len(in_keyframes),3))
        diff=np.zeros((numOfvideos,1))
        for i in range(len(in_keyframes)):
            in_avg_rgb[i] = RGB_MEAN(in_keyframes[i]) ############rgb input video
            
        for i in range(numOfvideos):
            sql ="SELECT avg_rgb FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id AND V.id=i"
            c.execute(sql)
            t= c.fetchall()
            db_avg_rgb=np.zeros((len(t),3))
            for h in range(len(t)):
                db_avg_rgb[h]=stringToList(t[h][0]) ############rgb video[i] in db
            for j in range(len(in_keyframes)):
                for k in range(len(t)): 
                    diff[i]= np.min(abs(np.mean(((in_avg_rgb[j]-db_avg_rgb[k])),axis=1)))
                    
        video_index=np.argmin(diff)
        c.execute("SELECT path FROM VIDEO as V WHERE V.id=video_index")
        video_path= c.fetchall()
        return video_path
    #elif method=="HIST":
    #elif method=="FEATURES_EXTR":
        #sql ="SELECT KF.path,avg_rgb FROM KEYFRAMES as KF INNER JOIN VIDEO as V ON KF.vid_id=V.id"
        #c.execute(sql) 
        #rows = c.fetchall()

path1='D:\ContentBasedRetrivalSystem\DataSet\Videos\acrobacia.mp4'
conn=sqlite3.connect("multimedia.db")
c= conn.cursor()
videopath=video_search(path1,conn,"RGB_MEAN")
print(videopath)
        