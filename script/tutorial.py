





import numpy as np
import cv2
from enum import Enum




face_cascade = cv2.CascadeClassifier('vision/haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier('vision/haarcascade_nose.xml')


# Read video
cap = cv2.VideoCapture(0)

class States(Enum):
    NoFaceFound = 0
    NoMask = 1
    YesMask = 2


frames_cap = 20
current_frame = 0
frame_list = [States.NoFaceFound] * frames_cap # limit to 3 seconds so like 90 frames
record = False


while 1:
    # Get individual frame
    ret, img = cap.read()
    img = cv2.flip(img,1)

    
    faces = face_cascade.detectMultiScale(img, 1.1, 4)


    closer = 0  
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        if w < 125:
            closer = 1
        noses = nose_cascade.detectMultiScale(img, 1.5, 5)
        for (x,y,w,h) in noses:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 1)
 
            
    if len(faces) < 1:
        pass
    elif closer == 0:
        # faces are in screen and are close enough
        if current_frame == 0:
            print("starting")
            record = True

        print(current_frame)
        if record == True:
            current_frame += 1
            if len(noses) > 0:
                frame_list[current_frame] = States.NoMask 
            else:
                frame_list[current_frame] = States.YesMask

            if current_frame >= len(frame_list) - 1:
                record = False
                # sendResultsToClient(frame_list)
                print(frame_list)
                current_frame = 0
            


    # Show frame with results
    cv2.imshow('Mask Detection', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   

# Release video
cap.release()
cv2.destroyAllWindows()