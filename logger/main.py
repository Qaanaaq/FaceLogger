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

# get the frame with slider


class NeutralFrame:
    landmarkpositions = [None] * 478


class CurrentLandmark:
    Current_landmarks = [None] * 478

    @classmethod
    def set_Current_landmarks(self, set_landmarks):
        self.Current_landmarks = set_landmarks



    def get_Current_landmarks(self):
        return self.Current_landmarks



# get the video
class Video:
    allframes = 0
    def __init__(self):
        if Start().get_video_file():
            self.video = cv2.VideoCapture(Start().get_video_file())
            self.allframes = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        else:
            self.allframes = 0


    def get_max_frames(self):
        return self.allframes




# play it frame by framee

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
        if Start().get_video_file():
            ret, frame = cv2.VideoCapture(Start().get_video_file()).read()
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




        if Video().get_max_frames():
            self.frame_number = Video().get_max_frames()
        else:
            self.frame_number = 0
        print (self.frame_number)


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
        self.slider =Scale(self.window, from_=0, to=0, length=800, tickinterval=10, orient=HORIZONTAL)
        self.slider.place(x=10, y=heightInt-10)

        self.btplay=tkinter.Button(window, text="Play / Pause", width=10, command=lambda: self.Play())
        self.btplay.place(x=100, y=450)

        self.btBack=tkinter.Button(window, text="Backwards / Pause", width=15, command=lambda: self.PlayBack())
        self.btBack.place(x=180, y=450)

        self.btSelect=tkinter.Button(window, text="Select Video", width=30, command=lambda: Start().select_video_file())
        self.btSelect.place(x=295, y=450)

        self.btNeutral=tkinter.Button(window, text="Neutral Frame", width=12,  command=lambda: self.Neutral())
        self.btNeutral.place(x=515, y=450)

        self.btTracking=tkinter.Button(window, text="Track video", width=10, command=lambda: self.Track())
        self.btTracking.place(x=610, y=450)

        self.btNormalize=tkinter.Button(window, text="Normalize Results", width=14, command=lambda: self.Normalize())
        self.btNormalize.place(x=690, y=450)

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



        maxframes = v.get_max_frames()
        self.slider.config(to=maxframes)

        if self.playing is True:
            return
        ########### playbar

        print("updating....")
        if self.playing is True:
            if t.get_current_time()<(maxframes-1):
                t.set_current_time(t.get_current_time() + 1)
                slider_pos = t.get_current_time()
                self.slider.set(slider_pos)
        if self.backwardsplaying is True:
            if t.get_current_time()>0:
                t.set_current_time(t.get_current_time() - 1)
                slider_pos = t.get_current_time()
                self.slider.set(slider_pos)
        else:
            t.set_current_time(self.slider.get())


        #########################
        c.set_current_frame(self.slider.get())



        if Start().get_video_file():
            self.vid = cv2.VideoCapture(Start().get_video_file())
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, c.get_current_frame())
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


    def Neutral(self):
        t = CurrentTime()
        cl = CurrentLandmark()
        self.Neutralframe= t.get_current_time()
        print(self.Neutralframe)
        l = NeutralFrame()
        for n in range(0, 478):
            l.landmarkpositions[n] = cl.get_Current_landmarks()[n]

            # print (f"{n}" + " numer: "+ f"{l.landmarkpositions[n]}")
        print (cl.get_Current_landmarks())

    def Tracking(self, number):

        filename = Start().get_video_file()
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


            if Start().get_video_file():
                self.vid = cv2.VideoCapture(Start().get_video_file())
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
            MouthOpen = self.euclideanDistance(nf.landmarkpositions[13], cl.get_Current_landmarks()[13]) - self.euclideanDistance(nf.landmarkpositions[14], cl.get_Current_landmarks()[14])
            MouthWide = self.euclideanDistance(nf.landmarkpositions[61], cl.get_Current_landmarks()[61])
            JawOpen = self.euclideanDistance(nf.landmarkpositions[200], cl.get_Current_landmarks()[200])
            MouthCorner_Left = self.euclideanDistance(nf.landmarkpositions[186], cl.get_Current_landmarks()[186])
            MouthCorner_Right = self.euclideanDistance(nf.landmarkpositions[322], cl.get_Current_landmarks()[322])
            UpperLipRaiser = self.euclideanDistance(nf.landmarkpositions[0], cl.get_Current_landmarks()[0]) - self.euclideanDistance(nf.landmarkpositions[13], cl.get_Current_landmarks()[13])
            LowerLipRaiser = self.euclideanDistance(nf.landmarkpositions[17], cl.get_Current_landmarks()[17]) - self.euclideanDistance(nf.landmarkpositions[14], cl.get_Current_landmarks()[14])
            LipPresser = self.euclideanDistance(nf.landmarkpositions[17], cl.get_Current_landmarks()[17]) - self.euclideanDistance(nf.landmarkpositions[0], cl.get_Current_landmarks()[0])
            EyeBlink = self.euclideanDistance(nf.landmarkpositions[159], cl.get_Current_landmarks()[159]) - self.euclideanDistance(nf.landmarkpositions[145], cl.get_Current_landmarks()[145])
            InnerBrowRaiser = self.euclideanDistance(nf.landmarkpositions[107], cl.get_Current_landmarks()[107])
            OuterBrowRaiser = self.euclideanDistance(nf.landmarkpositions[63], cl.get_Current_landmarks()[63])
            BrowLowerer = -(self.euclideanDistance(nf.landmarkpositions[55], cl.get_Current_landmarks()[55]))
            list.append(MouthOpen)
            list.append(MouthWide)
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
            #list.append("{:.1f}".format(EyeVert))
            #list.append("{:.1f}".format(EyeHoriz))
            writer.writerow(list)


    def Track(self):
        self.playing= True

        c = CurrentFrame()
        t = CurrentTime()
        cl = CurrentLandmark()
        nf = NeutralFrame()
        v = Video()

        filename = Start().get_video_file()
        print (filename)
        filebasedir= os.path.dirname(filename)
        filenaming= os.path.basename(filename)
        filenaming= os. path. splitext(filenaming)[0]

        with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            title = ["Frame", "MouthOpen", "MouthWide", "JawOpen", "MouthCorner_Left", "MouthCorner_Right","UpperLipRaiser","LowerLipRaiser","LipPresser","EyeBlink", "InnerBrowRaiser", "OuterBrowRaiser","BrowLowerer", "EyeHoriz", "EyeVert"]
            writer.writerow(title)

        t.set_current_time(0)

        while t.get_current_time() < v.get_max_frames():
        # while t.get_current_time() < 10:


            self.Tracking(t.get_current_time())
            t.set_current_time(t.get_current_time() + 1 )






        # self.window.after(self.delay, self.Track)
        print("tracking done")



    def Normalize(self):

        filename = Start().get_video_file()
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
                landmarks = results.multi_face_landmarks[0]

                #joke test
                # point1 = [img_w*landmarks.landmark[0].x, img_h*landmarks.landmark[0].y]
                # point2 = [img_w*landmarks.landmark[17].x, img_h*landmarks.landmark[17].y]
                # distance = self.euclideanDistance(point1, point2)
                # self.distancelabel.config(text = distance)

                cl = CurrentLandmark()
                for n in range(0, 478):

                    x = img_w*landmarks.landmark[n].x
                    y = img_h*landmarks.landmark[n].y
                    cv2.circle(frame, (int(x), int(y)), 1, (255, 0, 0), 1)
                    cl.Current_landmarks[n] = [x,y]



                FrameToProcess = frame
                return FrameToProcess


window_name = "Tkinter and OpenCV"

class Start:
    videoname = None
    @classmethod
    def select_video_file(self):
        filetypes = (('Video files', '*.mp4'), ('All files', '*.*'))
        self.videoname = fd.askopenfilename(title='Select video to track',initialdir='//', filetypes=filetypes)



    def get_video_file(self):
        # print(self.videoname)
        return self.videoname



# Start().select_video_file()
# video_name =  "C:/Users/Andras/Desktop/test.mp4"


Display(tkinter.Tk(), window_name)
