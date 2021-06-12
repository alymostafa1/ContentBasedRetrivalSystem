import sqlite3
import os
from CBIR_RGB import *
from CBVR import *
from CBIR_Hist import *
from CBIR_Layout import * # Histo Agent 007
from searching_method import *

def clear_db(conn):
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
    c.execute("DELETE FROM IMG")
    c.execute("DELETE FROM SLICES")
    c.execute("DELETE FROM VIDEO")
    c.execute("DELETE FROM KEYFRAMES")
    conn.commit()
    
    
def create_db(name):
    conn = sqlite3.connect(name)  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
    
    c.execute("DROP TABLE IF EXISTS IMG")
    c.execute("DROP TABLE IF EXISTS SLICES")
    c.execute("DROP TABLE IF EXISTS VIDEO")
    c.execute("DROP TABLE IF EXISTS KEYFRAMES")
    
    # Create table - IMG
    c.execute("""CREATE TABLE IMG (
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        path  CHAR(100) UNIQUE,
        avg_rgb CHAR(200),
        hist_bg CHAR(30000))""")
    
    # Create table - SLICES
    c.execute("""CREATE TABLE SLICES (
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        img_id INTEGER NOT NULL,
        hist CHAR(30000),
        FOREIGN KEY (img_id) REFERENCES IMG(id) ON UPDATE CASCADE ON DELETE CASCADE)""")
    
    # Create table - VIDEO
    c.execute("""CREATE TABLE VIDEO (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path CHAR(100) UNIQUE)""")
    
    # Create table - KEYFRAMES
    c.execute("""CREATE TABLE KEYFRAMES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vid_id INTEGER NOT NULL,
        avg_rgb CHAR(200),
        hist_bg CHAR(30000),
        FOREIGN KEY (vid_id) REFERENCES VIDEO(id) ON UPDATE CASCADE ON DELETE CASCADE)""")
    
    return conn
    
          
def insert_images(path, conn):
    c = conn.cursor()
    images = os.listdir(path)
    for i in range(len(images)):
        img_path = path + '/' + images[i]
        img = cv2.imread(img_path)
        image = cv2.resize(img, (200,200), interpolation = cv2.INTER_AREA)
        avg_rgb = RGB_MEAN(image)
        histo = hist_computation(image)
        str_hist = histo
        # INSERT RECORDS INTO TABLE IMG
        sql = "INSERT INTO IMG(path, avg_rgb, hist_bg) VALUES ('%s', '%s', '%s') " % (img_path, avg_rgb, str_hist)
        c.execute(sql)
        conn.commit()
        sql = "SELECT id FROM IMG WHERE path = '%s'" % img_path
        c.execute(sql)
        img_id = c.fetchall()
        histograms = Slicer_hist(image,16)
        for item in histograms:            
            hist = np.array(item)
            str_hist = hist
            sql = "INSERT INTO SLICES(img_id, hist) VALUES ('%s', '%s') " % (img_id, str_hist)
            c.execute(sql)
            conn.commit()

def insert_videos(path, conn):
    c = conn.cursor()
    videos = os.listdir(path)
    for i in range(len(videos)):
        vid_path = path + '/' + videos[i]
        sql = "INSERT INTO VIDEO(path) VALUES ('%s')" % vid_path
        c.execute(sql)
        conn.commit()
        sql = "SELECT id FROM VIDEO WHERE path = '%s'" % vid_path
        c.execute(sql)
        vid_id = c.fetchall()
        vid_id = vid_id[0][0]
        keyframes = keyframeDetection(vid_path, 0.5)
        for j in range(len(keyframes)):
            avg_rgb = RGB_MEAN(keyframes[j])
            histo = hist_computation(keyframes[j])
            str_hist = histo
            sql = "INSERT INTO KEYFRAMES(vid_id, avg_rgb, hist_bg) VALUES ('%d', '%s', '%s') " % (vid_id, avg_rgb, str_hist)
            c.execute(sql)
            conn.commit()

# path1 = 'DataSet/Images'
# path2 ='DataSet/Videos'

# conn = create_db('multimedia.db')

# insert_images(path1, conn)
# insert_videos(path2, conn)

# #conn=sqlite3.connect("multimedia.db")
# c = conn.cursor()
# c.execute('SELECT * FROM VIDEO') 
# table = c.fetchall()
# for row in table:
#     print(row)