import cv2, numpy as np
import sys
from time import sleep

def flick(x):
    pass

cv2.namedWindow('image')
cv2.moveWindow('image',250,150)
#cv2.namedWindow('controls')
#cv2.moveWindow('controls',250,50)

controls = np.zeros((50,750),np.uint8)
cv2.putText(controls, "W: Play, S: Stay, A: Prev, D: Next, E: Fast, Q: Slow, Esc: Exit", (40,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)


cap = cv2.VideoCapture("resources/test.mp4")

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
i = 0
cv2.createTrackbar('Timeline','image', 0,int(tots)-1, flick)
cv2.setTrackbarPos('Timeline','image',0)

cv2.createTrackbar('speed','image', 1, 100, flick)
frame_rate = 30
cv2.setTrackbarPos('speed','image',frame_rate)

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'

cv2.imwrite('color_img.jpg', controls)
img2 = cv2.imread('color_img.jpg')

while True:
  #cv2.imshow("controls",controls)
  try:
    if i==tots-1:
      i=0
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    r = 500.0 / im.shape[1]
    dim = (500, int(im.shape[0] * r))
    im = cv2.resize(im, (750, 500))
    #controls = cv2.resize(controls, (500,30))
    #if im.shape[0]>800:
    #    controls = cv2.resize(controls, (im.shape[1],25))
    #    im = cv2.resize(im, (400,400))





    both= np.concatenate((img2, im), axis=0)

    #cv2.putText(im, status, )
    cv2.imshow('image', both)

    status = { ord('s'):'stay', ord('S'):'stay',
                ord('w'):'play', ord('W'):'play',
                ord('a'):'prev_frame', ord('A'):'prev_frame',
                ord('d'):'next_frame', ord('D'):'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                ord('c'):'snap', ord('C'):'snap',
                -1: status,
                27: 'exit'}[cv2.waitKey(10)]

    if status == 'play':
      frame_rate = cv2.getTrackbarPos('speed','image')
      sleep((0.1-frame_rate/1000.0)**21021)
      i+=1
      cv2.setTrackbarPos('Timeline','image',i)
      continue
    if status == 'stay':
      i = cv2.getTrackbarPos('Timeline','image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        cv2.setTrackbarPos('Timeline','image',i)
        status='stay'
    if status=='next_frame':
        i+=1
        cv2.setTrackbarPos('Timeline','image',i)
        status='stay'
    if status=='slow':
        frame_rate = max(frame_rate - 5, 0)
        cv2.setTrackbarPos('speed', 'image', frame_rate)
        status='play'
    if status=='fast':
        frame_rate = min(100,frame_rate+5)
        cv2.setTrackbarPos('speed', 'image', frame_rate)
        status='play'
    if status=='snap':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print ("Snap of Frame",i,"Taken!")
        status='stay'

  except KeyError:
      print ("Invalid Key was pressed")


cv2.destroyWindow('image')
