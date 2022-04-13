import cv2
import dlib
import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import Label












#open model file
def select_model(param):
    filetypes2 = (
        ('Model', '*.dat'),
        ('All files', '*.*')
    )

    model= fd.askopenfilename(
        title='Open a model',
        initialdir='//',
        filetypes=filetypes2
    )
    global model_file_name
    model_file_name = model
    print(model_file_name)

    param.config(text = model)


    #showinfo(
    #    title='Selected File',
    #    message=model
    #)


def select_video_file(param):
    filetypes = (
        ('Video files', '*.mp4'),
        ('All files', '*.*')
    )

    videoname = fd.askopenfilename(
        title='Open tracking model',
        initialdir='/',
        filetypes=filetypes
    )
    global video_file_name
    video_file_name = videoname
    print(video_file_name)

    param.config(text = videoname)


    #showinfo(
    #    title='Selected File',
    #    message=videoname
    #)
