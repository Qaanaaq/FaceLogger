import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import Scale
from tkinter import HORIZONTAL
from tkinter import Label
from tkinter import filedialog
import time
import numpy as np
import mediapipe as mp

# get the frame with slider

# get the video and
class Video:
    def __init__(self, video_name):
        self.video = cv2.VideoCapture(video_name)
        self.allframes = self.video.get(cv2.CAP_PROP_FRAME_COUNT)

# play it frame by framee

class CurrentFrame:
    def __init__(self):
        self.current_frame = 0


    def set_current_frame(self, set_frame):
        self.current_frame = set_frame

    def get_current_frame(self):
        return self.current_frame

class CurrentImage:
    def __init__(self):
        ret, frame = Video(video_name).video.read()
        scale_percent = 30 # percent of original size
        width = 800
        height = int(frame.shape[0] * (width / frame.shape[1]))
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_image = frame
        self.frame= frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)




    def set_current_image(self, set_image):
        # cv2.imshow("Face Landmarks", self.frame )
        self.current_image = set_image


    def get_current_image(self):
        return self.current_image


class Display:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)


        self.video_source = video_source

        frame_number = Video(video_source).allframes

        # open video source
        self.vid = Video(video_source).video

        wideInt= 820
        heightInt= 520
        self.window.geometry(f'{wideInt+20}x{heightInt+80}')

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width =820, height = 420)
        self.canvas.pack()

        #labelstrack_label_name.set("")
        self.label = Label(self.window, text = 0)
        self.label.place(x=50, y=450)
        # self.label.pack()
        #label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

        # display the slider
        self.slider =Scale(self.window, from_=0, to=frame_number-1, length=800,tickinterval=10, orient=HORIZONTAL)
        self.slider.place(x=10, y=heightInt-10)

        self.btplay=tkinter.Button(window, text="Play", width=50, command=lambda: self.JumpTo(30))
        self.btplay.place(x=100, y=450)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()




        self.window.mainloop()


# display selected frame
    def update(self):
        c=CurrentFrame()
        i=CurrentImage()

        c.set_current_frame(self.slider.get())

        self.vid.set(cv2.CAP_PROP_POS_FRAMES, c.get_current_frame())
        ret, frame = self.vid.read()

        if ret:

            scale_percent = 30 # percent of original size
            width = 800
            height = int(frame.shape[0] * (width / frame.shape[1]))
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.Process(self.vid)
            # frame = i.get_current_image()

            self.label.config(text = c.get_current_frame())
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            # self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(i.get_current_image()))
            # self.canvas.create_image(5, 5, image = self.photo2, anchor = tkinter.NW)
            self.canvas.pack()
            self.window.after(self.delay, self.update)




    # define the countdown func.
    def countdown(self, t, max):


        while t<max:
            secs = t
            timer = '{:02d}'.format( secs)
            print(timer, end="\r")
            self.update()
            time.sleep(0.1)

            t += 1
            CurrentFrame().set_current_frame(t)

    def JumpTo(self, t):
        self.slider.set(t)

    def Process(self, image):

        i=CurrentImage()

        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence= 0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            ret, frame = image.read()

            if ret:

                scale_percent = 30
                # percent of original size
                width = 800
                height = int(frame.shape[0] * (width / frame.shape[1]))
                dim = (width, height)
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_h, img_w = frame.shape[:2]
                results = face_mesh.process(rgb_frame)
                landmarks = results.multi_face_landmarks[0]

                for n in range(0, 478):
                    x = img_w*landmarks.landmark[n].x
                    y = img_h*landmarks.landmark[n].y
                    cv2.circle(frame, (int(x), int(y)), 1, (45, 245, 55), 1)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow("Face Landmarks", frame)
                i.set_current_image(frame)


                # print (i.get_current_image())























window_name = "Tkinter and OpenCV"
video_name =  "C:/Users/Andras/Desktop/test.mp4"

Display(tkinter.Tk(), window_name, video_name)
