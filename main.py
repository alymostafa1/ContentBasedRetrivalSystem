import tkinter as tk
from tkinter import *
from tkinter import ttk


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

    def AdminopenNewWindow(self):

        newWindow = Toplevel(self.master)
        newWindow.title("Admin")
        newWindow.geometry("500x500")
        Label(newWindow,
              text="Insert the directory of the dataset of Images to be inserted",
              width=50, fg='red').pack()
        Entry(newWindow, width=50).pack()
        Button(newWindow, text='Done', width=20,
               bg='grey', fg='red').pack(pady=10)
        Label(newWindow,
              text="Insert the directory of the dataset of Videos to be inserted",
              width=50, fg='purple').pack()
        Entry(newWindow, width=50).pack()
        Button(newWindow, text='Done', width=20,
               bg='grey', fg='purple').pack(pady=10)

    def UseropenNewWindow(self):
        newWindow = Toplevel(self.master)
        newWindow.title("User")
        newWindow.geometry("500x500")
        Label(newWindow,
              text="Insert the directory of the Image searching for",
              width=50, font=20, fg='red').pack()
        Entry(newWindow, width=50).pack(pady=10)
        Label(newWindow,
              text="Choose the Algorithm of Searching",
              width=30, font=18, fg='red').pack()

        n = tk.StringVar()
        alorithmchoosen = ttk.Combobox(
            newWindow, width=27, textvariable=n)
        alorithmchoosen['values'] = ('Mean Color',
                                     ' Histograme',
                                     ' Object Detection',
                                     )

        alorithmchoosen.pack(pady=20)
        alorithmchoosen.current()
        Button(newWindow, text='Done', width=20,
               bg='grey', fg='red').pack(pady=10)
        Label(newWindow,
              text="Insert the directory of the Video searching for",
              width=50, font=20, fg='purple').pack(pady=30)
        Entry(newWindow, width=50).pack(pady=10)
        Label(newWindow,
              text="Choose the Algorithm of Searching",
              width=30, font=18, fg='purple').pack()
        n = tk.StringVar()
        alorithmchoosen = ttk.Combobox(
            newWindow, width=27, textvariable=n)
        alorithmchoosen['values'] = ('Video Naive Similarity',)

        alorithmchoosen.pack(pady=20)
        alorithmchoosen.current()

        Button(newWindow, text='Done', width=20,
               bg='grey', fg='purple').pack(pady=10)


root = Tk()
mygui = GUI(root)
root.mainloop()
