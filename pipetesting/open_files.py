import cv2
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import Label
from tkinter import NW, Tk, Canvas, PhotoImage

import tkinter as tk

from PIL import Image, ImageTk

import cv2 as cv











def select_video_file(param):
    filetypes = (
        ('Video files', '*.mp4'),
        ('All files', '*.*')
    )

    videoname = fd.askopenfilename(
        title='Open tracking model',
        initialdir='//',
        filetypes=filetypes
    )
    global video_file_name
    video_file_name = videoname
    print(video_file_name)

    param.config(text = videoname)
