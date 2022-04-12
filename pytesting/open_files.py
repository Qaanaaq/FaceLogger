import cv2
import dlib
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import Label



#open model file
def select_model():
    filetypes2 = (
        ('Model', '*.dat'),
        ('All files', '*.*')
    )

    model= fd.askopenfilename(
        title='Open a model',
        initialdir='//',
        filetypes=filetypes2
    )

    showinfo(
        title='Selected File',
        message=model
    )

    model=var



def select_video_file():
    filetypes = (
        ('Video files', '*.mp4'),
        ('All files', '*.*')
    )

    videoname = fd.askopenfilename(
        title='Open tracking model',
        initialdir='/',
        filetypes=filetypes
    )

    showinfo(
        title='Selected File',
        message=videoname
    )
