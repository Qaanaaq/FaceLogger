import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from tkinter import Scale
from tkinter import HORIZONTAL
from tkinter import Label

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        wideInt= int(self.vid.width)
        heightInt=int(self.vid.height)
        self.window.geometry(f'{wideInt+20}x{heightInt+80}')

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        #labelstrack_label_name.set("")
        self.label = Label(self.window, text = 0)
        self.label.place(x=50, y=50)
        #label.config(bg=rgb_hack((51, 51, 51)), fg='#fff')

        self.slider =Scale(self.window, from_=0, to=allframes, length=self.vid.width,tickinterval=10, orient=HORIZONTAL)
        self.slider.place(x=10, y=heightInt+10)



        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()




        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, current, frame = self.vid.get_frame()
        print (current)
        self.label.config(text = current)
        self.slider.set(int(current))
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

            self.window.after(self.delay, self.update)

        else:
            print ("ende")

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                self.current = self.vid.get(cv2.CAP_PROP_POS_FRAMES)
                if allframes==self.current:
                    return (ret, "",cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                return (ret, self.current,cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, "0",None)
        else:
            return (ret,"0" ,None)

 # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class GetNumberOfFrames:
    def AllFramer(self, frames):
        print ("This is the thing: " + str(frames))
        return frames


    def __init__(self):
        ####do something else entireliy
        videoPath=r"C:\Users\Andras\Desktop\test.mp4"
        #  Convert the video file path to a standard path
        #videoPath=videoPath.replace("\\","/").replace('"','').replace("'","").strip()
        #  Video acquisition
        videoCapture=cv2.VideoCapture(videoPath)
        #  Frame rate (frames per second)
        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        #  The total number of frames (frames)
        self.frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        print(" frames : "+str(fps))
        print(" The total number of frames: "+str(self.frames))
        print(" Total video duration: "+"{0:.2f}".format(self.frames/fps)+" second ")
        self.AllFramer(self.frames)



GetNumberOfFrames()
allframes = GetNumberOfFrames().frames

# # Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV", "C:/Users/Andras/Desktop/test.mp4")
