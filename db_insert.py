import sqlite3
import os
from RGB_CBIR import *
from CBVR import *
from histogram import *
from Img_Slicer import *
from helper_Function import *

def create_db(name):
    conn = sqlite3.connect(name)  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
    
    c.execute("DROP TABLE IF EXISTS IMG")
    c.execute("DROP TABLE IF EXISTS SLICES")
    c.execute("DROP TABLE IF EXISTS VIDEO")
    c.execute("DROP TABLE IF EXISTS KEYFRAMES")
    
    # Create table - IMG
    c.execute("""CREATE TABLE IMG (
        id  INT NOT NULL,
        path  CHAR(100),
        avg_rgb CHAR(200),
        hist_bg CHAR(30000),
        PRIMARY KEY (id))""")
    
    # Create table - slices
    c.execute("""CREATE TABLE SLICES (
        id  INT NOT NULL,
        img_id INT NOT NULL,
        hist CHAR(30000),
        PRIMARY KEY (id, img_id)
        FOREIGN KEY (img_id) REFERENCES IMG(id) ON UPDATE CASCADE ON DELETE CASCADE)""")
    
    # Create table - VIDEO
    c.execute("""CREATE TABLE VIDEO (
        id INT NOT NULL,
        path CHAR(100),
        PRIMARY KEY (id))""")
    
    # Create table - KEYFRAMES
    c.execute("""CREATE TABLE KEYFRAMES (
        id INT NOT NULL,
        vid_id INT NOT NULL,
        path CHAR(100),
        avg_rgb CHAR(200),
        hist_bg CHAR(30000),
        PRIMARY KEY (id, vid_id),
        FOREIGN KEY (vid_id) REFERENCES VIDEO(id) ON UPDATE CASCADE ON DELETE CASCADE)""")
    
    return conn
    
          
def insert_images(path, conn):
    c = conn.cursor()
    images = os.listdir(path)
    for i in range(len(images)):
        img_path = path + '\\' + images[i]
        image = cv2.imread(img_path)
        avg_rgb = RGB_MEAN(image)
        histo = hist_computation(image)
        str_hist = Array2String(histo)
        # INSERT RECORDS INTO TABLE IMG
        sql = "INSERT INTO IMG(id, path, avg_rgb, hist_bg) VALUES ('%d', '%s', '%s', '%s') " % (i, img_path, avg_rgb, str_hist)
        c.execute(sql)
        conn.commit()
        
        histograms = Slicer_hist(img_path,16)
        cntr = 0
        for key,item in histograms.items():
            for val in item:
                hist = np.array(val)
                str_hist = Array2String(hist)
                sql = "INSERT INTO SLICES(id, img_id, hist) VALUES ('%d', '%s', '%s') " % (cntr, i, str_hist)
                c.execute(sql)
                conn.commit()
                cntr += 1
            

def insert_videos(path, conn):
    c = conn.cursor()
    videos = os.listdir(path)
    for i in range(len(videos)):
        vid_path = path + '\\' + videos[i]
        sql = "INSERT INTO VIDEO(id, path) VALUES ('%d', '%s') " % (i, vid_path)
        c.execute(sql)
        conn.commit()
        keyframes, keyframePath = keyframeDetection(vid_path, 'Project', 0.5)
        for j in range(len(keyframes)):
            frame_path = os.path.join(keyframePath , 'keyframe'+ str(j+1) +'.jpg')
            avg_rgb = RGB_MEAN(keyframes[j])
            histo = hist_computation(keyframes[j])
            str_hist = Array2String(histo)
            sql = "INSERT INTO KEYFRAMES(id, vid_id, path, avg_rgb, hist_bg) VALUES ('%d','%d', '%s', '%s', '%s') " % (j, i, frame_path, avg_rgb, str_hist)
            c.execute(sql)
            conn.commit()
            

path1 = 'DataSet/Images'
path2 = 'DataSet/Videos'

conn = create_db('multimedia.db')

insert_images(path1, conn)
insert_videos(path2, conn)
c = conn.cursor()

c.execute('SELECT * FROM SLICES') 
table = c.fetchall()
for row in table:
    print(row)