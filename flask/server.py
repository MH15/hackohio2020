# import the necessary packages
import websockets
import asyncio
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import json
import time
from multiprocessing import Pool
import time


# https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


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

start_server = websockets.serve(sendMessageToClient, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
