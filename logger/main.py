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
        # print ("getting: "+str(self.current_frame))
        return self.current_frame

class CurrentTime:
    current_time = 0
    def __init__(self):
        pass



    @classmethod
    def set_current_time(self, set_time):
        self.current_time = set_time



    def get_current_time(self):
        return self.current_time

    # current_time = property(get_current_time, set_current_time)



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

        self.btplay=tkinter.Button(window, text="Play / Pause", width=30, command=lambda: self.Play())
        self.btplay.place(x=100, y=450)

        self.btplay=tkinter.Button(window, text="Backwards / Pause", width=30, command=lambda: self.PlayBack())
        self.btplay.place(x=350, y=450)

        self.playing = False
        self.backwardsplaying = False

        self.frames_label = Label(self.window, text = "Frames")
        self.frames_label.place(x=600, y=500)
        self.frame_entry = tkinter.Entry(window,textvariable = "", font=('calibre',10,'normal'))
        self.frame_entry.place(x=650, y=500)



        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()




        self.window.mainloop()


# display selected frame
    def update(self):
        c = CurrentFrame()
        i = CurrentImage()
        t = CurrentTime()


        if self.playing is True:
            t.set_current_time(t.get_current_time() + 1)
            slider_pos = t.get_current_time()
            self.slider.set(slider_pos)
        if self.backwardsplaying is True:
            t.set_current_time(t.get_current_time() - 1)
            slider_pos = t.get_current_time()
            self.slider.set(slider_pos)
        else:
            t.set_current_time(self.slider.get())


        # if self.frame_entry is not None:
        # self.slider.set(self.frame_entry)


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

            self.FrameToProcess = frame
            #### COMMENT THIS TO UNPROCESSED VIDEO --->
            processed = self.Process(self.vid, self.FrameToProcess)
            i.set_current_image(processed)
            frame = i.get_current_image()

            self.label.config(text = c.get_current_frame())
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

            self.canvas.pack()
            self.window.after(self.delay, self.update)






    #play function

    def Play(self):
        self.playing^= True

    def PlayBack(self):
        self.backwardsplaying^= True







    def JumpTo(self, t):
        self.slider.set(t)

    def Process(self, video, FrameToProcess):

        i=CurrentImage()

        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence= 0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:


            # data = PIL.Image.fromarray(image)
            # print ("thing: " + str(data))
            # cv2.imshow("Face Landmarks2", image)
            # picture = cv2.imread(data)

            ret, frame = video.read()

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

                # cv2.imshow("Face Landmarks", frame)
                FrameToProcess = frame
                return FrameToProcess



            # print (i.get_current_image())























window_name = "Tkinter and OpenCV"
video_name =  "C:/Users/Andras/Desktop/test.mp4"

Display(tkinter.Tk(), window_name, video_name)
