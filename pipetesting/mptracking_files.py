import cv2 as cv
import os
import csv
import numpy as np
import mediapipe as mp

def tracking_function(filename, param):
    print (filename)
    filebasedir= os.path.dirname(filename)
    filenaming= os.path.basename(filename)
    filenaming= os. path. splitext(filenaming)[0]


    #tracking with mediapipe

    mp_face_mesh = mp.solutions.face_mesh


    framenumber = 1
    font = cv.FONT_HERSHEY_SIMPLEX

    #creating variables for the face track
    global xneutralList
    global yneutralList
    xneutralList = []
    yneutralList = []

    global xBase
    global yBase
    xBase = 0
    yBase = 0

    global yBaseDelta
    global yBaseDelta
    xBaseDelta = 0
    yBaseDelta = 0

    global MouthOpenNeutral
    global MouthWideNeutral
    global JawOpenNeutral
    global MouthCorner_LeftNeutral
    global MouthCorner_RightNeutral
    global UpperLipRaiserNeutral
    global LowerLipRaiserNeutral
    global LipPresserNeutral
    global EyeBlinkNeutral
    global InnerBrowRaiserNeutral
    global OuterBrowRaiserNeutral
    global BrowLowererNeutral

    MouthOpenNeutral = 0
    MouthWideNeutral = 0
    JawOpenNeutral = 0
    MouthCorner_LeftNeutral = 0
    MouthCorner_RightNeutral = 0
    UpperLipRaiserNeutral = 0
    LowerLipRaiserNeutral = 0
    LipPresserNeutral = 0
    EyeBlinkNeutral = 0
    InnerBrowRaiserNeutral = 0
    OuterBrowRaiserNeutral = 0
    BrowLowererNeutral = 0

    global EyeHoriz
    global EyeVert
    EyeHoriz = 0
    EyeVert = 0

    #Create A new file for FACS

    with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        title = ["Frame", "MouthOpen", "MouthWide", "JawOpen", "MouthCorner_Left", "MouthCorner_Right","UpperLipRaiser","LowerLipRaiser","LipPresser","EyeBlink", "InnerBrowRaiser", "OuterBrowRaiser","BrowLowerer", "EyeHoriz", "EyeVert"]
        writer.writerow(title)



        #write facs data into table

    cap = cv.VideoCapture(filename)

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence= 0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:


        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            landmarks = results.multi_face_landmarks[0]

            for n in range(0, 478):
                xneutral = img_w*landmarks.landmark[n].x
                yneutral = img_h*landmarks.landmark[n].y
                xneutralList.append(xneutral)
                yneutralList.append(yneutral)

            xBase = img_w*landmarks.landmark[197].x
            yBase = img_h*landmarks.landmark[197].y
            print (framenumber)
            #print ("xNeutralList= " + str(xneutralList))
            #print ("yNeutralList= " + str(yneutralList))


            print ("xBase= " + str(xBase))

            MouthOpenNeutral = (img_h*landmarks.landmark[66].y - yneutralList[66]) - (img_h*landmarks.landmark[62].y - yneutralList[62])
            MouthWideNeutral = (img_w*landmarks.landmark[54].x - xneutralList[54]) - (img_w*landmarks.landmark[48].x - xneutralList[48])
            JawOpenNeutral = (img_h*landmarks.landmark[8].y - yneutralList[8]) - (img_h*landmarks.landmark[51].y - yneutralList[51])
            MouthCorner_LeftNeutral = img_h*landmarks.landmark[54].y - yneutralList[54]
            MouthCorner_RightNeutral = img_h*landmarks.landmark[48].y - yneutralList[48]
            UpperLipRaiserNeutral = (img_h*landmarks.landmark[51].y - yneutralList[51]) - (img_h*landmarks.landmark[29].y - yneutralList[29])
            LowerLipRaiserNeutral = (img_h*landmarks.landmark[29].y - yneutralList[29]) - (img_h*landmarks.landmark[57].y - yneutralList[57])
            LipPresserNeutral = (img_h*landmarks.landmark[51].y - yneutralList[51]) - (img_h*landmarks.landmark[57].y - yneutralList[57])
            EyeBlinkNeutral = (img_h*landmarks.landmark[37].y - yneutralList[37]) - (img_h*landmarks.landmark[40].y - yneutralList[40])
            InnerBrowRaiserNeutral = img_h*landmarks.landmark[21].y - yneutralList[21]
            OuterBrowRaiserNeutral = img_h*landmarks.landmark[17].y - yneutralList[17]
            BrowLowererNeutral = img_w*landmarks.landmark[21].x - xneutralList[21]

            break

            #####break
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence= 0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:


        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            landmarks = results.multi_face_landmarks[0]




            with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                list = [framenumber]
                xBaseDelta = img_w*landmarks.landmark[197].x - xBase
                yBaseDelta = img_h*landmarks.landmark[197].y - yBase

                #version where direct AUs are called
                MouthOpen = (img_h*landmarks.landmark[66].y - yneutralList[66]- yBaseDelta) - (img_h*landmarks.landmark[62].y - yneutralList[62] - yBaseDelta)- MouthOpenNeutral
                MouthWide = (img_w*landmarks.landmark[54].x - xneutralList[54] - xBaseDelta) - (img_w*landmarks.landmark[48].x - xneutralList[48]- xBaseDelta) - MouthWideNeutral
                JawOpen = (img_h*landmarks.landmark[8].y - yneutralList[8]- yBaseDelta) - (img_h*landmarks.landmark[51].y - yneutralList[51]- yBaseDelta) - JawOpenNeutral
                MouthCorner_Left = img_h*landmarks.landmark[54].y - yneutralList[54] - yBaseDelta - MouthCorner_LeftNeutral
                MouthCorner_Right = img_h*landmarks.landmark[48].y - yneutralList[48] - yBaseDelta - MouthCorner_RightNeutral
                UpperLipRaiser = (img_h*landmarks.landmark[51].y - yneutralList[51]- yBaseDelta) - (img_h*landmarks.landmark[29].y - yneutralList[29]- yBaseDelta) - UpperLipRaiserNeutral
                LowerLipRaiser = (img_h*landmarks.landmark[29].y - yneutralList[29]- yBaseDelta) - (img_h*landmarks.landmark[57].y - yneutralList[57]- yBaseDelta) - LowerLipRaiserNeutral
                LipPresser = (img_h*landmarks.landmark[51].y - yneutralList[51]- yBaseDelta) - (img_h*landmarks.landmark[57].y - yneutralList[57]- yBaseDelta) - LipPresserNeutral
                EyeBlink = (img_h*landmarks.landmark[37].y - yneutralList[37]- yBaseDelta) - (img_h*landmarks.landmark[40].y - yneutralList[40]- yBaseDelta) - EyeBlinkNeutral
                InnerBrowRaiser = img_h*landmarks.landmark[21].y - yneutralList[21] - yBaseDelta - InnerBrowRaiserNeutral
                OuterBrowRaiser = img_h*landmarks.landmark[17].y - yneutralList[17] - yBaseDelta - OuterBrowRaiserNeutral
                BrowLowerer = img_w*landmarks.landmark[21].x - xneutralList[21] - xBaseDelta - BrowLowererNeutral

                #if (MouthOpen > 0.2 or MouthOpen < -0.2 ):
                    #MouthOpen = MouthOpen
                #else: MouthOpen = 0
                #if (MouthWide > 0.5 or MouthWide < -0.5 ):
                    #MouthWide = MouthWide
                #else: MouthWide = 0



                #if (gaze.horizontal_ratio()== None):
                #    EyeHoriz = EyeHoriz
                #else: EyeHoriz = gaze.horizontal_ratio()



                #if (gaze.vertical_ratio()== None):
                #    EyeVert = EyeVert
                #else: EyeVert = gaze.vertical_ratio()


                #format_EyeVert = "{:.0f}".format(EyeVert*10)
                #int_EyeVert = int(format_EyeVert)

                #format_EyeHoriz = "{:.0f}".format(EyeHoriz*10)
                #int_EyeHoriz = int(format_EyeHoriz)

                list.append(MouthOpen/10)
                list.append(MouthWide/10)
                list.append(JawOpen/10)
                list.append(MouthCorner_Left/10)
                list.append(MouthCorner_Right/10)
                list.append(UpperLipRaiser /10)
                list.append(LowerLipRaiser/10)
                list.append(LipPresser/10)
                list.append(EyeBlink/10)
                list.append(InnerBrowRaiser/10)
                list.append(OuterBrowRaiser/10)
                list.append(BrowLowerer/10)
            #     #list.append("{:.1f}".format(EyeVert))
            #     #list.append("{:.1f}".format(EyeHoriz))
                writer.writerow(list)

            myString = filename
            cv.putText(frame, myString ,(1, 15),font, 0.5,(255,0,0),1,cv.LINE_AA)

            myString = "XDelta: " + str(xBaseDelta)
            cv.putText(frame, myString ,(1, 30),font, 0.4,(0,0,255),1,cv.LINE_AA)
            myString = "YDelta: " + str(yBaseDelta)
            cv.putText(frame, myString ,(1, 45),font, 0.4,(0,0,255),1,cv.LINE_AA)
            #
            #
            # myString = "JawDrop: " + str(JawOpen)
            # cv2.putText(frame, myString ,(1, 60),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            # cv2.rectangle(frame, (100, 45), (100 + (3 * JawOpen), 60), (0,255,255), -1)
            # myString = "MouthOpen: " + str(MouthOpen)
            # cv2.putText(frame, myString ,(1, 75),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            # cv2.rectangle(frame, (100, 60), (100 + (3 * MouthOpen), 75), (0,255,255), -1)
            # myString = "MouthWide: " + str(MouthWide)
            # cv2.putText(frame, myString ,(1, 90),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            # cv2.rectangle(frame, (100, 75), (100 + (3 * MouthWide), 90), (0,255,255), -1)
            #
            # myString = "BrowsOut: " + str(OuterBrowRaiser)
            # cv2.putText(frame, myString ,(1, 105),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            # cv2.rectangle(frame, (100, 90), (100 + (3 * OuterBrowRaiser), 105), (0,255,255), -1)
            # myString = "BrowsIn: " + str(InnerBrowRaiser)
            # cv2.putText(frame, myString ,(1, 120),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            # cv2.rectangle(frame, (100, 105), (100 + (3 * InnerBrowRaiser), 120), (0,255,255), -1)
            #
            # myString = "Blink: " + str(EyeBlink)
            # cv2.putText(frame, myString ,(1, 135),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            # cv2.rectangle(frame, (100, 120), (100 + (3 * EyeBlink), 135), (0,255,255), -1)

            #myString = "EyeHoriz: " + str(int_EyeHoriz)
            #cv2.putText(frame, myString ,(1, 150),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            #cv2.rectangle(frame, (100, 135), (100 + int_EyeHoriz, 150), (0,255,255), -1)

            #myString = "EyeVert: " + str(int_EyeVert)
            #cv2.putText(frame, myString ,(1, 165),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            #cv2.rectangle(frame, (100, 150), (100 + int_EyeVert, 165), (0,255,255), -1)

            myString = "Frame: " + str(framenumber)
            cv.putText(frame, myString ,(1, 180),font, 0.4,(0,255,255),1,cv.LINE_AA)

            x = img_w*landmarks.landmark[8].x
            #print ("x: " + str(x))
            #print ("x integer: " + str(int(x)))
            y = img_h*landmarks.landmark[8].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)


            x = img_w*landmarks.landmark[17].x

            y = img_h*landmarks.landmark[17].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)


            x = img_w*landmarks.landmark[22].x
            y = img_h*landmarks.landmark[22].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)


            x = img_w*landmarks.landmark[21].x
            y = img_h*landmarks.landmark[21].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)


            x = img_w*landmarks.landmark[26].x
            y = img_h*landmarks.landmark[26].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[29].x
            y = img_h*landmarks.landmark[29].y
            cv.circle(frame, (int(x), int(y)), 2, (0, 255, 0), 1)

            x = img_w*landmarks.landmark[31].x
            y = img_h*landmarks.landmark[31].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[35].x
            y = img_h*landmarks.landmark[35].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[40].x
            y = img_h*landmarks.landmark[40].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[43].x
            y = img_h*landmarks.landmark[43].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[47].x
            y = img_h*landmarks.landmark[47].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[37].x
            y = img_h*landmarks.landmark[37].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)


            x = img_w*landmarks.landmark[48].x
            y = img_h*landmarks.landmark[48].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[51].x
            y = img_h*landmarks.landmark[51].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[54].x
            y = img_h*landmarks.landmark[54].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[57].x
            y = img_h*landmarks.landmark[57].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[62].x
            y = img_h*landmarks.landmark[62].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            x = img_w*landmarks.landmark[66].x
            y = img_h*landmarks.landmark[66].y
            cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)

            framenumber = framenumber + 1


            if not os.path.exists(filebasedir +  "/TrackedVideo_" + filenaming):
                    os.makedirs(filebasedir + "/TrackedVideo_" + filenaming)
            img1 = cv.imshow("Face Landmarks", frame)
            cv.imwrite(filebasedir + '/TrackedVideo_' + filenaming + '/TrackedVideo_' + filenaming + '_' + str(framenumber-1)+'.jpg',frame)

            key = cv.waitKey(1)
            if key == ord('q'):
                break

            param.config(text = "Tracking done!")
        return img1

    cap.release()
    cv.destroyAllWindows()
