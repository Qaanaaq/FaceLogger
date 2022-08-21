import tkinter as tk

from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import StringVar
from tkinter import Label
from tkinter import NW, Tk, Canvas, PhotoImage
from PIL import Image, ImageTk
import cv2 as cv

import open_files
import mptracking_files


# import normalization

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
global root
root = tk.Tk()
root.title('Face Logger MEDIAPIPE2FACS')
root.resizable(False, False)
root.geometry('800x600')
#this changes the favicon just coz
root.iconbitmap(os.path.join(current_dir, 'face.ico'))




#this only sets the background to grey
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

root.config(bg=rgb_hack((51, 51, 51)))

#creating labels


video_label_name= StringVar()
video_label_name.set("")
video_label = Label(root, text = video_label_name.get())
video_label.place(x=250, y=20)
video_label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

track_label_name= StringVar()
track_label_name.set("")
track_label = Label(root, text = track_label_name.get())
track_label.place(x=250, y=50)
track_label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')


##### variables for from the selected files
open_files.video_file_name = "0"



#video and refreshing
img = cv.imread(r"C:\Users\Andras\Desktop\a.jpg")
width = 760
height = int((width / img.shape[1] ) *img.shape[0])
dim = (width, height)
img2= cv.resize(img, dim)
blue,green,red = cv.split(img2)
img2 = cv.merge((red,green,blue))
im = Image.fromarray(img2)
CATCH = ImageTk.PhotoImage(image=im)


# image_label = tk.Label(root, image=CATCH)
# image_label.place(x=20, y=80)
# secret = image_label

# # Canvas to display the rectangle
win = tk.Canvas(root, width=760, height=400)
win.place(x=20, y=80)
win.create_image(0, 0, image=CATCH, anchor=NW)
win.image= CATCH






def update():
    mptracking_files.redrawing_function(win)
    # 40ms , calling the same function again and again.
    root.after(40, update)



update()


# video button
video_button = ttk.Button(
    root,
    text='Open video file',
    command= lambda: open_files.select_video_file(video_label),
    width = 20
)
video_button.place(x=20, y=20)


# track button
track_button = ttk.Button(
    root,
    text='Track video',
    command= lambda: mptracking_files.tracking_function(open_files.video_file_name, track_label),
    width = 20
)

track_button.place(x=20, y=50)



# cap = cv.VideoCapture("C:\Users\Andras\Desktop\a.jpg")
#
# img = cap.read()
# img1 = cv.cvtColor (img, cv.COLOR_BGR2RGB)
# mg = ImageTk.PhotoImage (Image.fromarray(img1))



# run the application
root.mainloop()
