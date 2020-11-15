# import the necessary packages
from sanic_jinja2 import SanicJinja2
from sanic import response
from sanic.response import json
from sanic import Sanic
from socket import socket
from flask import Response
from flask import Flask
from flask import render_template
# try:
# from camera import VideoCamera
# except ImportError:
# pass  # skip circular import second pass

import cv2
import websockets
import asyncio
import threading
import json
from multiprocessing import Pool
from enum import Enum

from concurrent.futures import ThreadPoolExecutor


_executor = ThreadPoolExecutor(1)


# https://medium.com/datadriveninvestor/video-streaming-using-flask-and-opencv-c464bf8473d6
# initialize a flask object

app = Sanic(name="server")
jinja = SanicJinja2(app)
loop = asyncio.get_event_loop()


class States(Enum):
    NoFaceFound = 0
    NoMask = 1
    YesMask = 2


STATE = States.NoFaceFound

THRESHOLD = 3

# defining face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier("script/haarcascade_nose.xml")
ds_factor = 0.6


################### begin ###################
class VideoCamera(object):
    frames_cap = 5
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

    async def get_frame(self):
        # extracting frames
        ret, img = self.video.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, None, fx=ds_factor, fy=ds_factor,
                         interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # draw rectangles
        # face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces = await face_cascade.detectMultiScale(gray, 1.1, 4)
        noses = []
        closer = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            if w < 125:
                closer = 1
            noses = await nose_cascade.detectMultiScale(img, 1.5, 5)
            for (x, y, w, h) in noses:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

        asyncio.sleep(1)

        if len(faces) < 1:
            pass
        elif closer == 0:
            # faces are in screen and are close enough
            if self.current_frame == 0:
                print("starting")
                self.record = True

            # print(self.current_frame)
            if self.record == True:
                self.current_frame += 1
                if len(noses) > 0:
                    self.frame_list[self.current_frame] = States.NoMask
                else:
                    self.frame_list[self.current_frame] = States.YesMask

                if self.current_frame >= len(self.frame_list) - 1:
                    self.record = False
                    sendResultsToClient(self.frame_list)
                    # print(self.frame_list)
                    self.current_frame = 0

        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


def sendResultsToClient(frames):
    count_mask_frames = 0
    for val in frames:
        if val == States.YesMask:
            count_mask_frames += 1
    if count_mask_frames > THRESHOLD:
        global STATE
        STATE = States.YesMask

################### end ###################


@app.route("/")
def index(request):
    # await response.file('flask/templates/index.html')
    return jinja.render("index.html", request)

    # return render_template("index.html")


# async def generator_async(camera):
#     frame = camera.get_frame()
#     return (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# `f()` is asynchronous iterator.
# Since we don't raise `StopAsyncIteration`
# it works "like" `while True`, until we manually break.
# class f:
#     # camera = None
#     async def __aiter__(self, cam):
#         self.camera = cam
#         return self

#     async def __anext__(self):
#         return await generator_async(self.camera)


# def gen(camera):
#     # loop = asyncio.get_event_loop()
#     # loop.run_forever()
#     while True:
#         # get camera frame
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# loop = asyncio.get_event_loop()


FPS = 29.97
# STREAM_RESPONSE = \
#     """
# --frame
# Content-Type: image/jpeg

# """


async def websocketTest(websocket, path):

    while True:
        print("result")
        # Evaluate "func(10)" asynchronously calling callback when finished.
        # result = pool.apply_async(dataBuilder, [10], ).get()
        result = dataBuilder(1)
        print("done")

        print(json.dumps(result))

        loop = asyncio.get_event_loop()
        await websocket.send(json.dumps(result))
        # await websocket.send(json.dumps(result))
        await asyncio.sleep(.5)


async def gen(camera, websocket, response):
    """Video streaming generator function."""
    loop = asyncio.get_event_loop()
    # websockets.serve(websocketTest, "localhost", 8765)
    while True:

        frame = await camera.get_frame()
        await response.write(b'--frame\r\n'
                             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        await asyncio.sleep(1.0/FPS)


@app.route('/video_feed')
async def video_feed(request):

    # start_server = websockets.serve(sendMessageToClient, "localhost", 8765)

    loop = asyncio.get_event_loop()
    test = websockets.serve(websocketTest, "localhost", 8765)
    # loop.run_until_complete(test)

    # loop.run_until_complete(start_server)
    # loop.run_forever()
    """Video streaming route. Put this in the src attribute of an img tag."""
    return response.stream(response.partial(gen, VideoCamera(), socket),
                           content_type='multipart/x-mixed-replace; boundary=frame')


# @app.route("/video_feed")
# async def video_feed(request):
#     # return Response(gen(VideoCamera()),
#     #                 mimetype='multipart/x-mixed-replace; boundary=frame')
#     # return response.stream(
#     #     gen(VideoCamera()),
#     #     content_type='multipart/x-mixed-replace; boundary=frame')
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     async def stream_camera(response):
#         camera = VideoCamera()
#         while True:
#             frame = camera.get_frame()
#             response.write(STREAM_RESPONSE + frame)
#             await asyncio.sleep(1.0 / FPS)

#     return response.stream(
#         stream_camera,
#         content_type='multipart/x-mixed-replace; boundary=frame'
#     )


def dataBuilder(n):
    value = "working"
    if STATE == States.NoMask:
        value = "failure"
    if STATE == States.YesMask:
        value = "success"
    if STATE == States.NoFaceFound:
        value = "inactive"

    print("VALUEEEEE", value)
    data = {
        "type": "status",
        "value": value
    }
    return data


def generateDataForClient():
    i = 0


async def sendMessageToClient(websocket, path):
    # name = await websocket.recv()
    # print(f"< {name}")

    # greeting = f"Hello {name}!"

    # Start a worker processes.
    while True:
        print("result")
        # Evaluate "func(10)" asynchronously calling callback when finished.
        # result = pool.apply_async(dataBuilder, [10], ).get()
        result = dataBuilder(1)
        print("done")

        print(json.dumps(result))

        await loop.run_in_executor(None, websocket.send, json.dumps(result))
        # await websocket.send(json.dumps(result))
        await asyncio.sleep(.5)

    # print(f"> {greeting}")


# async def app_runner():
#     app.run(host='0.0.0.0', port=2204,
#             threaded=False, debug=True)


app.static('/static/', 'flask/static')


if __name__ == "__main__":

    print("test a")
    # start_server = websockets.serve(sendMessageToClient, "localhost", 8765)

    app.run(host='0.0.0.0', port=2204,
            debug=True)
    print("test b")

    # # start sockets
    # loop.run_until_complete(start_server)
    # loop.run_forever()

    print("test c")
    # loop.run_until_complete(app_runner)
