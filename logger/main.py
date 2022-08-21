import tkinter
import cv2
import PIL.Image, PIL.ImageTk

from tkinter import Scale
from tkinter import HORIZONTAL
from tkinter import Label
from tkinter import filedialog as fd

import math

import time
import numpy as np
import mediapipe as mp

import os
import csv

import normalization

class Start:
    videoname = None
    @classmethod
    def select_video_file(self):
        filetypes = (('Video files', '*.mp4'), ('All files', '*.*'))
        self.videoname = fd.askopenfilename(title='Select video to track',initialdir='//', filetypes=filetypes)

    def get_video_file(self):
        # print(self.videoname)
        return self.videoname

class NeutralFrame:
    landmarkpositions = [[None, None]] * 478

class CurrentLandmark:
    Current_landmarks = [[None, None]] * 478

    @classmethod
    def set_Current_landmarks(self, set_landmarks):
        self.Current_landmarks = set_landmarks


    def get_Current_landmarks(self):
        return self.Current_landmarks

class Video:
    allframes = 0
    def __init__(self):
        if Start().videoname:
            self.video = cv2.VideoCapture(Start().videoname)
            self.allframes = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        else:
            self.allframes = 0

    def get_max_frames(self):
        return self.allframes

class CurrentFrame:
    def __init__(self):
        self.current_frame = 0


    def set_current_frame(self, set_frame):
        self.current_frame = set_frame


    def get_current_frame(self):
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

class CurrentImage:
    def __init__(self):
        if Start().videoname:
            ret, frame = cv2.VideoCapture(Start().videoname).read()
            if ret:
                scale_percent = 30 # percent of original size
                width = 800
                height = int(frame.shape[0] * (width / frame.shape[1]))
                dim = (width, height)
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.current_image = frame
                self.frame= frame
        else:
            self.current_image = 0

    def set_current_image(self, set_image):
        # cv2.imshow("Face Landmarks", self.frame )
        self.current_image = set_image

    def get_current_image(self):
        return self.current_image

class Display:

    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        if Video().allframes:
            self.frame_number = Video().allframes
        else:
            self.frame_number = 0
        # print (self.frame_number)

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
        # self.label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

        # display the slider
        self.slider =Scale(self.window, from_=0, to=0, length=800, tickinterval=10, orient=HORIZONTAL)
        self.slider.place(x=10, y=heightInt-10)

        # back button
        self.btBack=tkinter.Button(window, text="<<", width=3, command=lambda: self.JumpTo(0))
        self.btBack.place(x=80, y=450)

        # select video dialog
        self.btSelect=tkinter.Button(window, text="Select Video", width=20, command=lambda: Start().select_video_file())
        self.btSelect.place(x=130, y=450)

        # select neutral frame button
        self.btNeutral=tkinter.Button(window, text="Neutral Frame", width=20,  command=lambda: self.Neutral())
        self.btNeutral.place(x=300, y=450)

        # track whole video button
        self.btTracking=tkinter.Button(window, text="Track video", width=20, command=lambda: self.Track())
        self.btTracking.place(x=470, y=450)

        # open created file and normalize results from 0-1 for each column
        self.btNormalize=tkinter.Button(window, text="Normalize Results", width=20, command=lambda: self.Normalize())
        self.btNormalize.place(x=640, y=450)

        self.tracking = False
        self.playing = False
        self.backwardsplaying = False

        # self.distancelabel = Label(self.window, text = 0)
        # self.distancelabel.place(x=10, y=10)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    # display selected frame
    def update(self):

        c = CurrentFrame()
        i = CurrentImage()
        t = CurrentTime()
        v = Video()

        maxframes = v.allframes
        self.slider.config(to=maxframes)

        c.set_current_frame(self.slider.get())

        if Start().videoname:
            self.vid = cv2.VideoCapture(Start().videoname)
            self.vid.set(38,1) # set buffer size parameter to 1.0
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, c.get_current_frame())
        else:
            # imag = PIL.Image.open("C:/Users/Andras/Desktop/a.jpg")
            # self.photo = PIL.ImageTk.PhotoImage(image = imag)
            self.window.after(self.delay, self.update)
            return
        ret, frame = self.vid.read()

        if ret:

            scale_percent = 10 # percent of original size
            width = 800
            height = int(frame.shape[0] * (width / frame.shape[1]))
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.FrameToProcess = frame

            self.label.config(text = c.get_current_frame())
            # cv2.imshow("Face Landmarks", frame )
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

            self.canvas.pack()
            self.window.after(self.delay, self.update)

    def Neutral(self):
        t = CurrentTime()
        cl = CurrentLandmark()
        self.Neutralframe= t.get_current_time()
        print(self.Neutralframe)
        l = NeutralFrame()

        if Start().videoname:
            self.vid = cv2.VideoCapture(Start().videoname)
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, t.get_current_time())
        else:
            self.window.after(self.delay, self.update)
            return

        ret, frame = self.vid.read()

        if ret:

            scale_percent = 30 # percent of original size
            width = 800
            height = int(frame.shape[0] * (width / frame.shape[1]))
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.FrameToProcess = frame
            processed = self.Process(self.vid, self.FrameToProcess)


        for n in range(0, 478):
            l.landmarkpositions[n] = cl.get_Current_landmarks()[n]

            # print (f"{n}" + " numer: "+ f"{l.landmarkpositions[n]}")
        print (cl.get_Current_landmarks())

    def Tracking(self, number):

        filename = Start().videoname
        filebasedir= os.path.dirname(filename)
        filenaming= os.path.basename(filename)
        filenaming= os. path. splitext(filenaming)[0]

        t = CurrentTime()
        c = CurrentFrame()
        cl = CurrentLandmark()
        nf = NeutralFrame()

        self.currentframenumber = number

        with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            list = [self.currentframenumber]

            if Start().videoname:
                self.vid = cv2.VideoCapture(Start().videoname)
                self.vid.set(38,1) # set buffer siye parameter to 1.0
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.currentframenumber)
            else:
                self.window.after(self.delay, self.update)
                return

            ret, frame = self.vid.read()

            if ret:

                scale_percent = 30 # percent of original size
                width = 800
                height = int(frame.shape[0] * (width / frame.shape[1]))
                dim = (width, height)
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.FrameToProcess = frame
                processed = self.Process(self.vid, self.FrameToProcess)

            print (self.currentframenumber)

            #version where direct AUs are called
            # MouthOpen = -((nf.landmarkpositions[14][1]- nf.landmarkpositions[13][1]) - (cl.get_Current_landmarks()[14][1]- cl.get_Current_landmarks()[13][1]))
            # MouthWide = nf.landmarkpositions[61][0] - cl.get_Current_landmarks()[61][0]
            # MouthOpen = self.euclideanDistance(nf.landmarkpositions[14], nf.landmarkpositions[13]) - self.euclideanDistance(cl.get_Current_landmarks()[14], cl.get_Current_landmarks()[13])
            MouthWide = self.euclideanDistance(nf.landmarkpositions[61], nf.landmarkpositions[291]) - self.euclideanDistance(cl.get_Current_landmarks()[61], cl.get_Current_landmarks()[291])
            MouthPucker = self.euclideanDistance(nf.landmarkpositions[181], nf.landmarkpositions[405]) - self.euclideanDistance(cl.get_Current_landmarks()[181], cl.get_Current_landmarks()[405])
            JawOpen = self.euclideanDistance(nf.landmarkpositions[200], nf.landmarkpositions[0]) - self.euclideanDistance(cl.get_Current_landmarks()[200], cl.get_Current_landmarks()[0])
            # makes an open jaw and a closed mouth
            MouthOpen = JawOpen - (self.euclideanDistance(nf.landmarkpositions[14], nf.landmarkpositions[13]) - self.euclideanDistance(cl.get_Current_landmarks()[14], cl.get_Current_landmarks()[13]))

            MouthCorner_Left = self.euclideanDistance(nf.landmarkpositions[186], nf.landmarkpositions[6]) - self.euclideanDistance(cl.get_Current_landmarks()[186], cl.get_Current_landmarks()[6])
            MouthCorner_Right = self.euclideanDistance(nf.landmarkpositions[410], nf.landmarkpositions[6]) - self.euclideanDistance(cl.get_Current_landmarks()[410], cl.get_Current_landmarks()[6])
            UpperLipRaiser = self.euclideanDistance(nf.landmarkpositions[13], nf.landmarkpositions[0]) - self.euclideanDistance(cl.get_Current_landmarks()[13], cl.get_Current_landmarks()[0])
            LowerLipRaiser = self.euclideanDistance(nf.landmarkpositions[17], nf.landmarkpositions[14]) - self.euclideanDistance(cl.get_Current_landmarks()[17], cl.get_Current_landmarks()[14])
            LipPresser = self.euclideanDistance(nf.landmarkpositions[17], nf.landmarkpositions[0]) - self.euclideanDistance(cl.get_Current_landmarks()[17], cl.get_Current_landmarks()[0])
            EyeBlink = self.euclideanDistance(nf.landmarkpositions[159], nf.landmarkpositions[145]) - self.euclideanDistance(cl.get_Current_landmarks()[159], cl.get_Current_landmarks()[145])
            InnerBrowRaiser = self.euclideanDistance(nf.landmarkpositions[107], nf.landmarkpositions[6]) - self.euclideanDistance(cl.get_Current_landmarks()[107], cl.get_Current_landmarks()[6])
            OuterBrowRaiser = self.euclideanDistance(nf.landmarkpositions[63], nf.landmarkpositions[6]) - self.euclideanDistance(cl.get_Current_landmarks()[63], cl.get_Current_landmarks()[6])
            BrowLowerer = self.euclideanDistance(nf.landmarkpositions[55], nf.landmarkpositions[6]) - self.euclideanDistance(cl.get_Current_landmarks()[55], cl.get_Current_landmarks()[6])
            #### LEFT_IRIS = [474,475, 476, 477]
            #### RIGHT_IRIS = [469, 470, 471, 472]
            EyeHoriz = self.euclideanDistance(nf.landmarkpositions[474], nf.landmarkpositions[263]) - self.euclideanDistance(cl.get_Current_landmarks()[474], cl.get_Current_landmarks()[263])
            EyeVert =  self.euclideanDistance(nf.landmarkpositions[472], nf.landmarkpositions[159]) - self.euclideanDistance(cl.get_Current_landmarks()[472], cl.get_Current_landmarks()[159])

            used_vert_set = [0, 6, 13, 14, 17, 55, 61, 63, 107, 145, 159, 181, 186, 200, 263, 291, 405, 410, 472, 474]
            list.append(MouthOpen)
            list.append(MouthWide)
            list.append(MouthPucker)
            list.append(JawOpen)
            list.append(MouthCorner_Left)
            list.append(MouthCorner_Right)
            list.append(UpperLipRaiser)
            list.append(LowerLipRaiser)
            list.append(LipPresser)
            list.append(EyeBlink)
            list.append(InnerBrowRaiser)
            list.append(OuterBrowRaiser)
            list.append(BrowLowerer)
            list.append(EyeVert)
            list.append(EyeHoriz)
            writer.writerow(list)

    def Track(self):
        self.playing= True

        c = CurrentFrame()
        t = CurrentTime()
        cl = CurrentLandmark()
        nf = NeutralFrame()
        v = Video()

        filename = Start().videoname
        print (filename)
        filebasedir= os.path.dirname(filename)
        filenaming= os.path.basename(filename)
        filenaming= os.path.splitext(filenaming)[0]

        with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            title = ["Frame", "MouthOpen", "MouthWide","mouthPucker", "JawOpen", "MouthCorner_Left", "MouthCorner_Right","UpperLipRaiser","LowerLipRaiser","LipPresser","EyeBlink", "InnerBrowRaiser", "OuterBrowRaiser","BrowLowerer", "EyeHoriz", "EyeVert"]
            writer.writerow(title)

        t.set_current_time(0)

        while t.get_current_time() < v.allframes:

            self.slider.set(t.get_current_time())
            self.Tracking(t.get_current_time())
            t.set_current_time(t.get_current_time() + 1 )



        # self.window.after(self.delay, self.Track)
        print("tracking done")

    def Normalize(self):

        filename = Start().videoname
        normalization.normalize(filename)

    def JumpTo(self, t):
        self.slider.set(t)

    def euclideanDistance(self, point1, point2):
        x, y = point1
        x1, y1 = point2
        distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
        return distance

    def Process(self, video, FrameToProcess):

        i=CurrentImage()

        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence= 0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:


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
                cl = CurrentLandmark()
                nf = NeutralFrame()

                used_vert_set = [0, 6, 13, 14, 17, 55, 61, 63, 107, 145, 159, 181, 186, 200, 263, 291, 405, 410, 472, 474]
                u = len(used_vert_set)
                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0]




                #     for n in range(0, 478):
                #
                #         x = img_w*landmarks.landmark[n].x
                #         y = img_h*landmarks.landmark[n].y
                #         # cv2.circle(frame, (int(x), int(y)), 1, (255, 0, 0), 1)
                #         cl.Current_landmarks[n] = [x,y]
                # else:
                #     for n in range(0, 478):
                #         cl.Current_landmarks[n] = nf.landmarkpositions[n]

                    for n in range(0, u):

                        x = img_w*landmarks.landmark[used_vert_set[n]].x
                        y = img_h*landmarks.landmark[used_vert_set[n]].y
                        cv2.circle(frame, (int(x), int(y)), 1, (255, 0, 0), 1)
                        cl.Current_landmarks[used_vert_set[n]] = [x,y]
                        # cv2.imshow("Face Landmarks", frame )
                else:
                    for n in range(0, u):
                        cl.Current_landmarks[used_vert_set[n]] = nf.landmarkpositions[used_vert_set[n]]


                FrameToProcess = frame
                return FrameToProcess



window_name = "Tkinter and OpenCV"

Display(tkinter.Tk(), window_name)
