# import the necessary packages
from flask import Response
from flask import Flask
from flask import render_template
from camera import VideoCamera
import cv2

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



