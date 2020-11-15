from enum import Enum
import cv2

# defining face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier("script/haarcascade_nose.xml")
ds_factor = 0.6


class States(Enum):
    NoFaceFound = 0
    NoMask = 1
    YesMask = 2


class VideoCamera(object):
    frames_cap = 20
    current_frame = 0
    # limit to 3 seconds so like 90 frames
    frame_list = [States.NoFaceFound] * frames_cap
    record = False

    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self):
        # extracting frames
        ret, img = self.video.read()
        # img = cv2.flip(img, 1)
        img = cv2.resize(img, None, fx=ds_factor, fy=ds_factor,
                         interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # draw rectangles
        # face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        noses = []
        closer = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            if w < 125:
                closer = 1
            # noses = nose_cascade.detectMultiScale(img, 1.5, 5)
            for (x, y, w, h) in noses:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

        # if len(faces) < 1:
        #     pass
        # elif closer == 0:
        #     # faces are in screen and are close enough
        #     if self.current_frame == 0:
        #         print("starting")
        #         self.record = True

        #     print(self.current_frame)
        #     if self.record == True:
        #         self.current_frame += 1
        #         if len(noses) > 0:
        #             self.frame_list[self.current_frame] = States.NoMask
        #         else:
        #             self.frame_list[self.current_frame] = States.YesMask

        #         if self.current_frame >= len(self.frame_list) - 1:
        #             self.record = False
        #             # sendResultsToClient(frame_list)
        #             print(self.frame_list)
        #             self.current_frame = 0

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
