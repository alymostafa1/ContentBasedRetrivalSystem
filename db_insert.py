import sqlite3
import os
from RGB_CBIR import *
from CBVR import *


def create_db(name):
    conn = sqlite3.connect(name)  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
    
    c.execute("DROP TABLE IF EXISTS IMG")
    c.execute("DROP TABLE IF EXISTS VIDEO")
    c.execute("DROP TABLE IF EXISTS KEYFRAMES")
    
    # Create table - IMG
    c.execute("""CREATE TABLE IMG (
        id  INT NOT NULL,
        path  CHAR(100),
        avg_rgb CHAR(200),
        hist CHAR(5000),
        PRIMARY KEY (id))""")
    
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
        hist CHAR(5000),
        PRIMARY KEY (id, vid_id),
        FOREIGN KEY (vid_id) REFERENCES VIDEO(id) ON UPDATE CASCADE ON DELETE CASCADE)""")
    
    return conn
    
          
def insert_images(path, conn):
    c = conn.cursor()
    images = os.listdir(path)
    for i in range(2,len(images)):
        img_path = path + "/" + images[i]
        image = cv2.imread(img_path)
        avg_rgb = RGB_MEAN(image)
        
        ### HISTOGRAM FUNCTION RETURNS ARRAY AND ENTERED IN HIST COLUMN ###
        
        # INSERT RECORDS INTO TABLE IMG
        sql = "INSERT INTO IMG(id, path, avg_rgb) VALUES ('%d', '%s', '%s') " % (i, img_path, avg_rgb)
        c.execute(sql)
        conn.commit()

def insert_videos(path, conn):
    c = conn.cursor()
    videos = os.listdir(path)
    for i in range(len(videos)):
        vid_path = path + "/" + videos[i]
        sql = "INSERT INTO VIDEO(id, path) VALUES ('%d', '%s') " % (i, vid_path)
        c.execute(sql)
        conn.commit()
        keyframes, keyframePath = keyframeDetection(vid_path, 'Project', 0.5)
        for j in range(len(keyframes)):
            frame_path = os.path.join(keyframePath , 'keyframe'+ str(j+1) +'.jpg')
            avg_rgb = RGB_MEAN(keyframes[j])
            
            ### HISTOGRAM FUNCTION RETURNS ARRAY AND ENTERED IN HIST COLUMN ###
            
            sql = "INSERT INTO KEYFRAMES(id, vid_id, path, avg_rgb) VALUES ('%d','%d', '%s', '%s') " % (j, i, frame_path, avg_rgb)
            c.execute(sql)
            conn.commit()
            

path1 = 'DataSet/Images'
path2 = 'DataSet/Videos'

conn = create_db('multimedia.db')

insert_images(path1, conn)
insert_videos(path2, conn)
c = conn.cursor()

# c.execute('SELECT * FROM VIDEO') 
# table = c.fetchall()
# for row in table:
#     print(row)