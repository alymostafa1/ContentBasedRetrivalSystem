from os import path
import tkinter as tk
from tkinter import *
from tkinter import ttk
import cv2
from numpy.lib.arraypad import pad
from db_insert import insert_images, insert_videos, create_db
import sqlite3
from searching_method import *
from video_search import *


class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Content-Based Multi-media Retrival System')
        master.geometry('500x500+100+100')
        self.lable = Label(
            master, text='Choose Your Identity', width=25, fg='red', font=32)
        self.lable.pack(pady=10)
        self.button = Button(master, text='Admin', width=30,
                             height=2, bg='grey', fg='black', command=self.AdminopenNewWindow)
        self.button.pack(pady=30)
        self.button = Button(master, text='User', width=30,
                             height=2, bg='grey', fg='black', command=self.UseropenNewWindow)
        self.button.pack(pady=30)
        Button(text='Quit', bg='black', fg='white', width=15,
               command=lambda: quit()).pack(pady=10)
        self.conn = create_db('multimedia.db')
        c = self.conn.cursor()
        self.n = StringVar()
        self.L = StringVar()
        self.Isearch = StringVar()
        self.Vsearch = StringVar()
        self.InsertsearchImage = StringVar()
        self.InsertImgs = StringVar()
        self.InsertVideos = StringVar()

    def VgetPath(self):
        m = self.InsertVideos.get()
        return m

    def InsertVideo(self):
        path = self.VgetPath()
        insert_videos(path, self.conn)

    def IgetPath(self):
        m = self.InsertImgs.get()
        return m

    def InsertImg(self):
        path = self.IgetPath()
        insert_images(path, self.conn)

    def IsearchgetPath(self):
        m = self.InsertsearchImage.get()
        return m

    def InsertsearchImg(self):
        path = self.IgetPath()
        insert_images(path, self.conn)

    def VView(self):
        newWindow = Toplevel()
        newWindow.title("My Data")
        newWindow.geometry("500x500")
        tree_frame = Frame(newWindow)
        tree_frame.pack(pady=20)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                                 column=("c1", "c2"), show='headings')
        tree_scroll.config(command=self.tree.yview)
        xscroll = ttk.Scrollbar(
            tree_frame, orient='horizontal', command=self.tree.xview)
        xscroll.pack(side=BOTTOM, fill=X)
        self.tree.column("#1", anchor=tk.CENTER, width=350)
        self.tree.heading("#1", text="id")
        self.tree.column("#2", anchor=tk.CENTER, width=350)
        self.tree.heading("#2", text="path")

        self.tree.pack()
        cur1 = self.conn.execute("SELECT * FROM VIDEO")
        rows = cur1.fetchall()
        for row in rows:
            print(row)
            self.tree.insert("", tk.END, values=row)
        self.c.close()

    def IView(self):
        newWindow = Toplevel()
        newWindow.title("My Data")
        newWindow.geometry("500x500")
        tree_frame = Frame(newWindow)
        tree_frame.pack(pady=20)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                                 column=("c1", "c2", "c3", "c4"), show='headings')
        tree_scroll.config(command=self.tree.yview)
        xscroll = ttk.Scrollbar(
            tree_frame, orient='horizontal', command=self.tree.xview)
        xscroll.pack(side=BOTTOM, fill=X)
        self.tree.column("#1", anchor=tk.CENTER, width=350)
        self.tree.heading("#1", text="id")
        self.tree.column("#2", anchor=tk.CENTER, width=350)
        self.tree.heading("#2", text="path")
        self.tree.column("#3", anchor=tk.CENTER, width=350)
        self.tree.heading("#3", text="avg_rgb")
        self.tree.column("#4", anchor=tk.CENTER, width=350)
        self.tree.heading("#4", text="hist_bg")

        self.tree.pack()
        cur1 = self.conn.execute("SELECT * FROM IMG")
        rows = cur1.fetchall()
        for row in rows:
            print(row)
            self.tree.insert("", tk.END, values=row)
        self.c.close()

    def AdminopenNewWindow(self):

        newWindow = Toplevel(self.master)
        newWindow.title("Admin")
        newWindow.geometry("500x500")
        Label(newWindow,
              text="Insert the directory of the dataset of Images to be inserted",
              width=50, fg='red').pack()
        Entry(newWindow, width=50, textvariable=self.InsertImgs).pack()
        Button(newWindow, text='Done', width=20,
               bg='grey', fg='red', command=self.InsertImg).pack(pady=10)
        Label(newWindow,
              text="Insert the directory of the dataset of Videos to be inserted",
              width=50, fg='purple').pack()
        Entry(newWindow, width=50, textvariable=self.InsertVideos).pack()
        Button(newWindow, text='Done', width=20,
               bg='grey', fg='purple', command=self.InsertVideo).pack(pady=10)
        Button(newWindow, text="Display videos data",
               command=self.VView).pack(pady=10)
        Button(newWindow, text="Display Imgs data",
               command=self.IView).pack(pady=10)

    def ImageAlgorithms(self):
        newWindow = Toplevel()
        newWindow.title("Result")
        newWindow.geometry("500x500")
        m = self.Isearch.get()
        N = self.n.get()
        img = ImageSearch(m, self.conn, N)
        Label(newWindow, text="The Searching Results", font=2,
              bg='black', fg='white').pack(pady=20)
        Label(newWindow, text=img).pack(pady=10)
        Img = cv2.imread(img)
        cv2.imshow('image', Img)
        cv2.waitKey(0)

    def VideoAlgorithms(self):
        newWindow = Toplevel()
        newWindow.title("Result")
        newWindow.geometry("500x500")
        m = self.Vsearch.get()
        l = self.L.get()
        video = video_search(m, self.conn, l)
        Label(newWindow, text="The Searching Results", font=2,
              bg='black', fg='white').pack(pady=20)
        Label(newWindow, text=video).pack(pady=10)
        cv2.VideoCapture(video)
        cap = cv2.VideoCapture(video)
        mirror = False
        cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, frame = cap.read()
            if mirror:
                frame = cv2.flip(frame, 1)
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break  # esc to quit

    def UseropenNewWindow(self):
        newWindow = Toplevel(self.master)
        newWindow.title("User")
        newWindow.geometry("500x500")
        Label(newWindow,
              text="Insert the directory of the Image searching for",
              width=50, font=20, fg='red').pack()
        Entry(newWindow, width=50, textvariable=self.Isearch).pack(pady=10)
        Label(newWindow,
              text="Choose the Algorithm of Searching",
              width=30, font=18, fg='red').pack()

        alorithmchoosen = ttk.Combobox(
            newWindow, width=27, textvariable=self.n)
        alorithmchoosen['values'] = ('RGB_MEAN',
                                     'Histogram',
                                     'SLiced-Histogram',
                                     )

        alorithmchoosen.pack(pady=20)
        alorithmchoosen.current()
        Button(newWindow, text='Done', width=20,
               bg='grey', fg='red', command=self.ImageAlgorithms).pack(pady=10)
        Label(newWindow,
              text="Insert the directory of the Video searching for",
              width=50, font=20, fg='purple').pack(pady=30)
        Entry(newWindow, width=50, textvariable=self.Vsearch).pack(pady=10)
        Label(newWindow,
              text="Choose the Algorithm of Searching",
              width=30, font=18, fg='purple').pack()
        n = tk.StringVar()
        alorithmchoosen = ttk.Combobox(
            newWindow, width=27, textvariable=self.L)
        alorithmchoosen['values'] = ('RGB_MEAN',
                                     'HIST'
                                     )

        alorithmchoosen.pack(pady=20)
        alorithmchoosen.current()

        Button(newWindow, text='Done', width=20,
               bg='grey', fg='purple', command=self.VideoAlgorithms).pack(pady=10)


root = Tk()
mygui = GUI(root)
root.mainloop()
