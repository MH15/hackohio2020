# import the necessary packages
from asyncio.streams import start_server
from sanic_jinja2 import SanicJinja2
from sanic import response
from sanic.response import json
from sanic import Sanic
from socket import socket
from flask import Response
from flask import Flask
from flask import render_template
from sanic.websocket import WebSocketProtocol
# try:
# from camera import VideoCamera
# except ImportError:
# pass  # skip circular import second pass

import cv2
import websockets
import asyncio
import threading
import json
import sys
from multiprocessing import Pool
from enum import Enum
import warnings

from concurrent.futures import ThreadPoolExecutor


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
SOCKET = None
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
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        noses = []
        closer = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            if w < 125:
                closer = 1
            noses = nose_cascade.detectMultiScale(img, 1.5, 5)
            for (x, y, w, h) in noses:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

        await asyncio.sleep(.1)

        if len(faces) < 1:
            pass
        elif closer == 0:
            # faces are in screen and are close enough
            if self.current_frame == 0:
                print("starting")
                self.record = True

            print(self.current_frame)
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


# def whole_ass_app(websocket, path):
    # print("launched")

@app.route("/")
def index(request):
    # await response.file('flask/templates/index.html')
    return jinja.render("index.html", request)
    # return jinja.render("template.html", request)

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

# async def websocketTest(websocket, path):

#     while True:
#         print("result")
#         # Evaluate "func(10)" asynchronously calling callback when finished.
#         # result = pool.apply_async(dataBuilder, [10], ).get()
#         result = dataBuilder(1)
#         print("done")

#         print(json.dumps(result))

#         loop = asyncio.get_event_loop()
#         await websocket.send(json.dumps(result))
#         # await websocket.send(json.dumps(result))
#         await asyncio.sleep(.5)


async def gen(camera, response):
    """Video streaming generator function."""
    loop = asyncio.get_event_loop()
    # websockets.serve(websocketTest, "localhost", 8765)
    while True:
        # print("socket", SOCKET)
        # send the websocket
        # if SOCKET is not None:
        #     result = dataBuilder(1)
        #     await SOCKET.send(json.dumps(result))

        # process video frame
        frame = await camera.get_frame()
        # stream video frame
        await response.write(b'--frame\r\n'
                             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        await asyncio.sleep(1.0/FPS)


@app.route('/video_feed')
async def video_feed(request):

    # start_server = websockets.serve(sendMessageToClient, "localhost", 8765)

    # loop = asyncio.get_event_loop()
    # test = websockets.serve(websocketTest, "localhost", 8765)
    # loop.run_until_complete(test)

    # loop.run_until_complete(start_server)
    # loop.run_forever()
    """Video streaming route. Put this in the src attribute of an img tag."""
    return response.stream(response.partial(gen, VideoCamera()),
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


@app.websocket('/websockets')
async def feed(request, ws):
    print("SOCKET")
    # asyncio.get_event_loop().stop()
    # sys.exit(0)
    while True:
        data = dataBuilder(1)
        j = json.dumps(data)
        await ws.send(j)
        await asyncio.sleep(1)


def setup_sockets(websocket, path):
    print("loading websockets")
    SOCKET = websocket
    # sys.exit()

    while True:
        print("test")

#     # print(f"> {greeting}")

# async def app_runner():
#     app.run(host='0.0.0.0', port=2204,
#             threaded=False, debug=True)


app.static('/static/', 'flask/static')

# app.run(host='0.0.0.0', port=2204,
# debug=True)


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        app.run(host='0.0.0.0',
                port=2204,
                debug=True,
                protocol=WebSocketProtocol
                )

    # print("test a")
    # start_server = websockets.serve(setup_sockets, "localhost", 8765)
    # start_server = websockets.serve(setup_sockets, "localhost", 8756)
    # # print("test b")
    # # # start sockets
    # # sys.exit()
    # loop.run_until_complete(start_server)
    # loop.run_forever()

    # loop = asyncio.get_event_loop()
    # srv_coro = app.create_server(
    #     return_asyncio_server=True,
    #     asyncio_server_kwargs=dict(
    #         start_serving=False
    #     ),
    #     port=2205,
    #     protocol=WebSocketProtocol
    # )
    # srv = loop.run_until_complete(srv_coro)
    # try:
    #     assert srv.is_serving() is False
    #     loop.run_until_complete(srv.start_serving())
    #     assert srv.is_serving() is True
    #     loop.run_until_complete(srv.serve_forever())
    # except KeyboardInterrupt:
    #     srv.close()
    #     loop.close()

    # print("test c")
    # loop.run_until_complete(app_runner)
