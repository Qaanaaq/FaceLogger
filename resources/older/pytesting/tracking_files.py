import cv2
import dlib
import os
import csv


def tracking_function(model, filename, param):
    print (model)
    print (filename)
    filebasedir= os.path.dirname(filename)
    filenaming= os.path.basename(filename)
    filenaming= os. path. splitext(filenaming)[0]


    #tracking


    framenumber = 1

    font = cv2.FONT_HERSHEY_SIMPLEX

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

    cap = cv2.VideoCapture(filename)

    hog_face_detector = dlib.get_frontal_face_detector()

    dlib_facelandmark = dlib.shape_predictor(model)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=1, fy=1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)




        faces = hog_face_detector(gray)
        for face in faces:

            face_landmarks = dlib_facelandmark(gray, face)

            for n in range(0, 68):
                xneutral = face_landmarks.part(n).x
                yneutral = face_landmarks.part(n).y
                xneutralList.append(xneutral)
                yneutralList.append(yneutral)

            xBase = face_landmarks.part(29).x
            yBase = face_landmarks.part(29).y
            #print (xneutralList)
            #print (xneutralList)

            MouthOpenNeutral = (face_landmarks.part(66).y - yneutralList[66]) - (face_landmarks.part(62).y - yneutralList[62])
            MouthWideNeutral = (face_landmarks.part(54).x - xneutralList[54]) - (face_landmarks.part(48).x - xneutralList[48])
            JawOpenNeutral = (face_landmarks.part(8).y - yneutralList[8]) - (face_landmarks.part(51).y - yneutralList[51])
            MouthCorner_LeftNeutral = face_landmarks.part(54).y - yneutralList[54]
            MouthCorner_RightNeutral = face_landmarks.part(48).y - yneutralList[48]
            UpperLipRaiserNeutral = (face_landmarks.part(51).y - yneutralList[51]) - (face_landmarks.part(29).y - yneutralList[29])
            LowerLipRaiserNeutral = (face_landmarks.part(29).y - yneutralList[29]) - (face_landmarks.part(57).y - yneutralList[57])
            LipPresserNeutral = (face_landmarks.part(51).y - yneutralList[51]) - (face_landmarks.part(57).y - yneutralList[57])
            EyeBlinkNeutral = (face_landmarks.part(37).y - yneutralList[37]) - (face_landmarks.part(40).y - yneutralList[40])
            InnerBrowRaiserNeutral = face_landmarks.part(21).y - yneutralList[21]
            OuterBrowRaiserNeutral = face_landmarks.part(17).y - yneutralList[17]
            BrowLowererNeutral = face_landmarks.part(21).x - xneutralList[21]



        break



    while True:
        _, frame = cap.read()
        print (framenumber)
        frame = cv2.resize(frame, None, fx=1, fy=1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)






        faces = hog_face_detector(gray)
        for face in faces:

            face_landmarks = dlib_facelandmark(gray, face)

            #gaze.refresh(frame)
            #frame = gaze.annotated_frame()

            with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                list = [framenumber]
                xBaseDelta = face_landmarks.part(29).x - xBase
                yBaseDelta = face_landmarks.part(29).y - yBase

                #version where direct AUs are called
                MouthOpen = (face_landmarks.part(66).y - yneutralList[66]- yBaseDelta) - (face_landmarks.part(62).y - yneutralList[62] - yBaseDelta)- MouthOpenNeutral
                MouthWide = (face_landmarks.part(54).x - xneutralList[54] - xBaseDelta) - (face_landmarks.part(48).x - xneutralList[48]- xBaseDelta) - MouthWideNeutral
                JawOpen = (face_landmarks.part(8).y - yneutralList[8]- yBaseDelta) - (face_landmarks.part(51).y - yneutralList[51]- yBaseDelta) - JawOpenNeutral
                MouthCorner_Left = face_landmarks.part(54).y - yneutralList[54] - yBaseDelta - MouthCorner_LeftNeutral
                MouthCorner_Right = face_landmarks.part(48).y - yneutralList[48] - yBaseDelta - MouthCorner_RightNeutral
                UpperLipRaiser = (face_landmarks.part(51).y - yneutralList[51]- yBaseDelta) - (face_landmarks.part(29).y - yneutralList[29]- yBaseDelta) - UpperLipRaiserNeutral
                LowerLipRaiser = (face_landmarks.part(29).y - yneutralList[29]- yBaseDelta) - (face_landmarks.part(57).y - yneutralList[57]- yBaseDelta) - LowerLipRaiserNeutral
                LipPresser = (face_landmarks.part(51).y - yneutralList[51]- yBaseDelta) - (face_landmarks.part(57).y - yneutralList[57]- yBaseDelta) - LipPresserNeutral
                EyeBlink = (face_landmarks.part(37).y - yneutralList[37]- yBaseDelta) - (face_landmarks.part(40).y - yneutralList[40]- yBaseDelta) - EyeBlinkNeutral
                InnerBrowRaiser = face_landmarks.part(21).y - yneutralList[21] - yBaseDelta - InnerBrowRaiserNeutral
                OuterBrowRaiser = face_landmarks.part(17).y - yneutralList[17] - yBaseDelta - OuterBrowRaiserNeutral
                BrowLowerer = face_landmarks.part(21).x - xneutralList[21] - xBaseDelta - BrowLowererNeutral

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
                #list.append("{:.1f}".format(EyeVert))
                #list.append("{:.1f}".format(EyeHoriz))
                writer.writerow(list)

            myString = filename
            cv2.putText(frame, myString ,(1, 15),font, 0.5,(255,0,0),1,cv2.LINE_AA)

            myString = "XDelta: " + str(xBaseDelta)
            cv2.putText(frame, myString ,(1, 30),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            myString = "YDelta: " + str(yBaseDelta)
            cv2.putText(frame, myString ,(1, 45),font, 0.4,(0,0,255),1,cv2.LINE_AA)


            myString = "JawDrop: " + str(JawOpen)
            cv2.putText(frame, myString ,(1, 60),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (100, 45), (100 + (3 * JawOpen), 60), (0,255,255), -1)
            myString = "MouthOpen: " + str(MouthOpen)
            cv2.putText(frame, myString ,(1, 75),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (100, 60), (100 + (3 * MouthOpen), 75), (0,255,255), -1)
            myString = "MouthWide: " + str(MouthWide)
            cv2.putText(frame, myString ,(1, 90),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (100, 75), (100 + (3 * MouthWide), 90), (0,255,255), -1)

            myString = "BrowsOut: " + str(OuterBrowRaiser)
            cv2.putText(frame, myString ,(1, 105),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (100, 90), (100 + (3 * OuterBrowRaiser), 105), (0,255,255), -1)
            myString = "BrowsIn: " + str(InnerBrowRaiser)
            cv2.putText(frame, myString ,(1, 120),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (100, 105), (100 + (3 * InnerBrowRaiser), 120), (0,255,255), -1)

            myString = "Blink: " + str(EyeBlink)
            cv2.putText(frame, myString ,(1, 135),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame, (100, 120), (100 + (3 * EyeBlink), 135), (0,255,255), -1)

            #myString = "EyeHoriz: " + str(int_EyeHoriz)
            #cv2.putText(frame, myString ,(1, 150),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            #cv2.rectangle(frame, (100, 135), (100 + int_EyeHoriz, 150), (0,255,255), -1)

            #myString = "EyeVert: " + str(int_EyeVert)
            #cv2.putText(frame, myString ,(1, 165),font, 0.4,(0,0,255),1,cv2.LINE_AA)
            #cv2.rectangle(frame, (100, 150), (100 + int_EyeVert, 165), (0,255,255), -1)

            myString = "Frame: " + str(framenumber)
            cv2.putText(frame, myString ,(1, 180),font, 0.4,(0,255,255),1,cv2.LINE_AA)

            x = face_landmarks.part(8).x
            y = face_landmarks.part(8).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)


            x = face_landmarks.part(17).x
            y = face_landmarks.part(17).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)


            x = face_landmarks.part(22).x
            y = face_landmarks.part(22).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)


            x = face_landmarks.part(21).x
            y = face_landmarks.part(21).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)


            x = face_landmarks.part(26).x
            y = face_landmarks.part(26).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(29).x
            y = face_landmarks.part(29).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), 1)

            #x = face_landmarks.part(31).x
            #y = face_landmarks.part(31).y
            #cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            #x = face_landmarks.part(35).x
            #y = face_landmarks.part(35).y
            #cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            #x = face_landmarks.part(40).x
            #y = face_landmarks.part(40).y
            #cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(43).x
            y = face_landmarks.part(43).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            #x = face_landmarks.part(47).x
            #y = face_landmarks.part(47).y
            #cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(37).x
            y = face_landmarks.part(37).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)


            x = face_landmarks.part(48).x
            y = face_landmarks.part(48).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(51).x
            y = face_landmarks.part(51).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(54).x
            y = face_landmarks.part(54).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(57).x
            y = face_landmarks.part(57).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(62).x
            y = face_landmarks.part(62).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = face_landmarks.part(66).x
            y = face_landmarks.part(66).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            framenumber = framenumber + 1


        if not os.path.exists(filebasedir +  "/TrackedVideo_" + filenaming):
                os.makedirs(filebasedir + "/TrackedVideo_" + filenaming)
        cv2.imshow("Face Landmarks", frame)
        cv2. imwrite(filebasedir + '/TrackedVideo_' + filenaming + '/TrackedVideo_' + filenaming + '_' + str(framenumber-1)+'.jpg',frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

        param.config(text = "Tracking done!")

    cap.release()
    cv2.destroyAllWindows()
