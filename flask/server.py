# Import the necessary packages
from asyncio.streams import start_server
from sanic_jinja2 import SanicJinja2
from sanic import response
from sanic.response import json
from sanic import Sanic
from sanic.websocket import WebSocketProtocol

import cv2
import asyncio
import json
from enum import Enum
import warnings

from websockets.protocol import State

# Basis for video streaming in flaskL=:
# https://medium.com/datadriveninvestor/video-streaming-using-flask-and-opencv-c464bf8473d6

# Initialize a flask object
app = Sanic(name="server")
jinja = SanicJinja2(app)
loop = asyncio.get_event_loop()

# Enumerated class for mask detection state
class States(Enum):
    NoFaceFound = 0
    NoMask = 1
    YesMask = 2


STATE = States.NoFaceFound
SOCKET = None
THRESHOLD = 3

DEBUG = []

# Defining face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier("script/haarcascade_nose.xml")
ds_factor = 0.6


################### begin ###################
class VideoCamera(object):
    frames_cap = 6
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
        # Extracting frames
        ret, img = self.video.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, None, fx=ds_factor, fy=ds_factor,
                         interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Draw rectangles on faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        noses = []
        closer = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            if w < 125:
                closer = 1
            # Draw noses
            noses = nose_cascade.detectMultiScale(img, 1.5, 5)
            #for (x, y, w, h) in noses:
            #    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

        await asyncio.sleep(.1)

        if len(faces) < 1:
            pass
        elif closer == 0:
            # Check if faces are in screen and are close enough
            if self.current_frame == 0:
                self.frame_list = [States.NoFaceFound] * self.frames_cap
                self.record = True

            if self.record == True:
                self.current_frame += 1
                if len(noses) > 0:
                    self.frame_list[self.current_frame] = States.NoMask
                else:
                    self.frame_list[self.current_frame] = States.YesMask

                if self.current_frame >= len(self.frame_list) - 1:
                    self.record = False
                    sendResultsToClient(self.frame_list)
                    self.current_frame = 0

        # Encode OpenCV raw frame to jpg and return
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


def sendResultsToClient(frames):
    global DEBUG
    count_yesmask_frames = 0
    count_nomask_frames = 0
    count_noperson_frames = 0
    for val in frames:
        if val == States.YesMask:
            count_yesmask_frames += 1
        if val == States.NoMask:
            count_nomask_frames += 1
        if val == States.NoFaceFound:
            count_noperson_frames += 1
    global STATE
    if count_yesmask_frames > THRESHOLD:
        STATE = States.YesMask
    else:
        STATE = States.NoMask

    DEBUG = frames

################### end ###################


@app.route("/")
def index(request):
    # await response.file('flask/templates/index.html')
    # return jinja.render("index.html", request)
    return jinja.render("template.html", request)
    # return await response.file("templates/template.html")


FPS = 29.97


async def gen(camera, response):
    """Video streaming generator function."""
    loop = asyncio.get_event_loop()
    # websockets.serve(websocketTest, "localhost", 8765)
    while True:

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

    data = {
        "type": "status",
        "value": value
        # "debug": DEBUG
    }
    print("VALUEEE", value)
    return data


def generateDataForClient():
    i = 0


@app.websocket('/websockets')
async def feed(request, ws):
    # print("connect")
    # asyncio.get_event_loop().stop()
    # sys.exit(0)
    while True:
        data = dataBuilder(1)
        # print("SOCKET")
        j = json.dumps(data)
        await ws.send(j)
        await asyncio.sleep(.1)


app.static('/static/', 'flask/static')


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        app.run(host='0.0.0.0',
                port=2204,
                debug=True,
                protocol=WebSocketProtocol
                )
