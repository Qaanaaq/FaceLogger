from tkinter import *
import numpy as np
from PIL import Image, ImageTk
import cv2 as cv

#Create an instance of tkinter frame
win = Tk()
win.geometry("700x550")

#Load the image
img = cv.imread(r"C:\Users\Andras\Desktop\c.jpg")

#Rearrange colors
blue,green,red = cv.split(img)
img = cv.merge((red,green,blue))
im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)

#Create a Label to display the image
Label(win, image= imgtk).pack()
win.mainloop()



#
# cv.imshow ("Image", img)
# cv.waitKey(0)
#
# cv.destroyAllWindows()
