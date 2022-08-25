import mediapipe as mp

print(mp.__file__)
import cv2 as cv
import numpy as np
mp_face_mesh = mp.solutions.face_mesh

cap=cv.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv.cvtColor (frame, cv.COLOR_BGR2RGB)

        results = face_mesh.process(rgb_frame)
        img_h, img_w = frame.shape[:2]
        landmarks = results.multi_face_landmarks[0]
        x = img_w*landmarks.landmark[472].x
        y = img_h*landmarks.landmark[472].y
        cv.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 1)
        cv.imshow('img', frame)
        key= cv.waitKey(1)
        if key == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
