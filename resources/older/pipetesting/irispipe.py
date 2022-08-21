import cv2 as cv
import numpy as np
import mediapipe as mp

LEFT_EYE = [ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
LEFT_IRIS =[474,475, 476, 477]
RIGHT_IRIS= [469, 470, 471, 472]


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh




cap = cv.VideoCapture(0)



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

        if results.multi_face_landmarks:

            for face_landmarks in results.multi_face_landmarks:
                #all borders
                 mp_drawing.draw_landmarks(
                 image= frame,
                 landmark_list =  face_landmarks,
                 connections = mp_face_mesh.FACEMESH_CONTOURS,
                 landmark_drawing_spec= None,
                 connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_contours_style()
                 )



            for face_landmarks in results.multi_face_landmarks:
                #all borders
                 mp_drawing.draw_landmarks(
                 image= frame,
                 landmark_list =  face_landmarks,
                 connections = mp_face_mesh.FACEMESH_TESSELATION,
                 landmark_drawing_spec= None,
                 connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_tesselation_style()
                 )

            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            #
            # # cv.polylines(frame, [mesh_points[LEFT_EYE]], True, (0,255,0),1, cv.LINE_AA)
            # # cv.polylines(frame, [mesh_points[RIGHT_EYE]], True, (0,255,0),1, cv.LINE_AA)
            #
            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv.circle (frame, center_left, int(l_radius) , (0,255,255),1, cv.LINE_AA)
            cv.circle (frame, center_right, int(r_radius) , (0,255,255),1, cv.LINE_AA)

            points = results.multi_face_landmarks[0].landmark[138]
            print (points.y * img_h )


        cv.imshow('img', cv.flip(frame,  1))
        key = cv.waitKey(1)
        if key == ord('q'):
            break

cap.release ()
cv.destroyAllWindows()
