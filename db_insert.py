import pymysql
from RGB_CBIR import *

try:
    # DATABASE ALREADY EXISTS
    db = pymysql.connect(
        host="localhost",
        user=input("Enter your MySQL Workbench username (try root): "),
        password=input("Enter password: "),
        database="schema",
    )
   
except:
    # DATABASE DOESN'T EXIST, CREATE A NEW ONE
    create_db_query = "CREATE DATABASE schema"
    db = pymysql.connect(
        host="localhost",
        user=input("Enter your MySQL Workbench username (try root): "),
        password=input("Enter password: "),
    ).cursor().execute(create_db_query)
    
cursor = db.cursor()

# DELETE TABLES IF THEY ALREADY EXIST, TO AVOID DUPLICATES
cursor.execute("DROP TABLE IF EXISTS CBIR")

# CREATE TABLE CBIR (ID, PATH, AVG_RGB)
sql = """CREATE TABLE CBIR (
    id  INT NOT NULL,
    path  CHAR(100),
    avg_rgb CHAR(200),
    PRIMARY KEY (id))"""

cursor.execute(sql)

# DATASET INSERTION
path = "DataSet"
images = os.listdir(path)
for i in range(1,len(images)):
    img_path = path + "/" + images[i]
    image = cv2.imread(img_path)
    avg = RGB_MEAN(image)
    
    # INSERT RECORDS INTO TABLE CBIR
    sql = "INSERT INTO CBIR(id, path, avg_rgb) VALUES ('%d', '%s', '%s') " % (i, img_path, avg)
    cursor.execute(sql)
    db.commit()
    

# disconnect from server
db.close()