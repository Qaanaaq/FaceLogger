import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import StringVar
from tkinter import Label

import open_files
import tracking_files
import normalization

from pathlib import *


current_dir = Path.cwd()
home_dir = Path.home()
#print(current_dir)
#print(home_dir)



import os
#from config.definitions import ROOT_DIR
#ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
#print(os.path.join(ROOT_DIR, 'face.ico'))

# create the root window
root = tk.Tk()
root.title('Face Logger OPENCV2FACS')
root.resizable(False, False)
root.geometry('800x200')
#this changes the favicon just coz
root.iconbitmap(os.path.join(current_dir, 'face.ico'))




#this only sets the background to grey
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

root.config(bg=rgb_hack((51, 51, 51)))

#creating labels

model_label_name= StringVar()
model_label_name.set("")
model_label = Label(root, text = model_label_name.get())
model_label.place(x=250, y=20)
model_label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

video_label_name= StringVar()
video_label_name.set("")
video_label = Label(root, text = video_label_name.get())
video_label.place(x=250, y=50)
video_label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

track_label_name= StringVar()
track_label_name.set("")
track_label = Label(root, text = track_label_name.get())
track_label.place(x=250, y=80)
track_label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

norm_label_name= StringVar()
norm_label_name.set("")
norm_label = Label(root, text = norm_label_name.get())
norm_label.place(x=250, y=110)
norm_label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

##### variables for from the selected files
open_files.video_file_name = "0"
open_files.model_file_name = "0"



# open model button
model_button = ttk.Button(
    root,
    text='Open tracking model',
    command= lambda: open_files.select_model(model_label),
    width = 30
)
model_button.place(x=20, y=20)


# video button
video_button = ttk.Button(
    root,
    text='Open video file',
    command= lambda: open_files.select_video_file(video_label),
    width = 30
)
video_button.place(x=20, y=50)


# track button
track_button = ttk.Button(
    root,
    text='Track video',
    command= lambda: tracking_files.tracking_function(open_files.model_file_name, open_files.video_file_name, track_label),
    width = 30
)
track_button.place(x=20, y=80)

# normalize button
normalize_button = ttk.Button(
    root,
    text='Normalize data',
    command=lambda: normalization.normalize(open_files.video_file_name, norm_label),
    width = 30
)
normalize_button.place(x=20, y=110)






# run the application
root.mainloop()
