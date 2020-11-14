# import the necessary packages
from flask import Response
from flask import Flask
from flask import render_template
from camera import VideoCamera
import cv2
import websockets
import asyncio
import threading
import json
from multiprocessing import Pool

# https://medium.com/datadriveninvestor/video-streaming-using-flask-and-opencv-c464bf8473d6
# initialize a flask object
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def gen(camera):
    while True:
        # get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)


def dataBuilder(n):
    data = {
        "type": "status",
        "value": "failure"
    }
    return data


def generateDataForClient():
    i = 0


async def sendMessageToClient(websocket, path):
    # name = await websocket.recv()
    # print(f"< {name}")

    # greeting = f"Hello {name}!"

    # Start a worker processes.
    pool = Pool(processes=1)
    while True:
        print("result")
        # Evaluate "func(10)" asynchronously calling callback when finished.
        # result = pool.apply_async(dataBuilder, [10], ).get()
        result = dataBuilder(1)
        print("done")

        await websocket.send(json.dumps(result))
        await asyncio.sleep(2)

    # print(f"> {greeting}")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2204, threaded=True, debug=True)


start_server = websockets.serve(sendMessageToClient, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
