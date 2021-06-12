we implemented ContentBasedRetrievalSystem to let any user search automatically and faster than he searches by himself 
consisted of:
## GUI 
Content-based image retrieval system
Content-based video retrieval system
##  implementation
frontend: GUI, has to choose user or admin then if you are an admin you will insert the database and he can check if the database is inserted or not.
 if you are a user you will choose image or video
if image:
will insert the path of the image and choose the method (RGB- histogram -Sliced Histogram)
if video:
will insert the path of the video and choose the method (RGB- histogram )

## backend 

implementation of database insertion whether videos or images, comparison methods between database images and the input images & search methods to get the best match 

## Database
 in the database, we insert the id, the path of the images and if it's RGB we put the values whether it's RGB, Histogram, or sliced Histogram to compare the values of the input image with the values on the histogram 
if videos we insert two tables: 1- video id and path
2-video id, path & keyframes

## Sequence

1.open GUI
1.choose admin or user
1.if admin insert path of a folder of images or videos "calling database functions to insert the Infos"
1.if user insert the path of video or image and the method you want to search 
"take the image and if the user chose RGB will get the RGB values for the image and then call search function to search for this image in the database and get the best match for it"
1.the result will appear 

##Admin Screenshot
![Admin](C:\Users\My Lap\Desktop\New folder\screenshots\admin.PNG)


##user Screenshot
![User](C:\Users\My Lap\Desktop\New folder\screenshots\user.PNG)


