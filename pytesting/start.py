import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import StringVar

# create the root window
root = tk.Tk()
root.title('Face Logger OPENCV2FACS')
root.resizable(False, False)
root.geometry('600x200')
#this changes the favicon just coz
root.iconbitmap('C:/Users/Andras/github/FaceLogger/pytesting/face.ico')



#this only sets the background to grey
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

root.config(bg=rgb_hack((51, 51, 51)))


def tracking():{  }

def normalize():{  }

from open_files import *


# open model button
model_button = ttk.Button(
    root,
    text='Open tracking model',
    command= select_model,
    width = 30
)
model_button.place(x=20, y=20)


# video button
video_button = ttk.Button(
    root,
    text='Open video file',
    command=select_video_file,
    width = 30
)
video_button.place(x=20, y=50)


# track button
track_button = ttk.Button(
    root,
    text='Track video',
    command=tracking,
    width = 30
)
track_button.place(x=20, y=80)

# normalize button
normalize_button = ttk.Button(
    root,
    text='Normalize data',
    command=normalize,
    width = 30
)
normalize_button.place(x=20, y=110)

var = tk.StringVar()
model_label = Label(root, text = var)
model_label.place(x=250, y=20)



#video_label = Label(root, text = select_video_file.videoname)

#video_label.pack()

# run the application
root.mainloop()