import sqlite3
import os
from RGB_CBIR import *


def create_db(name):
    conn = sqlite3.connect(name)  # You can create a new database by changing the name within the quotes
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
    
    c.execute("DROP TABLE IF EXISTS IMG")
    
    # Create table - IMG
    c.execute("""CREATE TABLE IMG (
        id  INT NOT NULL,
        path  CHAR(100),
        avg_rgb CHAR(200),
        hist CHAR(5000),
        PRIMARY KEY (id))""")
    return conn
    
          
def insert_images(path, conn):
    c = conn.cursor()
    images = os.listdir(path)
    for i in range(1,len(images)):
        img_path = path + "/" + images[i]
        image = cv2.imread(img_path)
        avg_rgb = RGB_MEAN(image)
        
        ### HISTOGRAM FUNCTION RETURNS ARRAY AND ENTERED IN HIST COLUMN ###
        
        # INSERT RECORDS INTO TABLE IMG
        sql = "INSERT INTO IMG(id, path, avg_rgb) VALUES ('%d', '%s', '%s') " % (i, img_path, avg)
        c.execute(sql)
        conn.commit()

path = 'DataSet'
conn = create_db('multimedia.db')
insert_images(path, conn)
c = conn.cursor()

# c.execute('SELECT * FROM IMG') 
# table = c.fetchall()
# for row in table:
#     print(row)