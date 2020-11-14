# hackohio2020

## `vision` module
Install OpenCV with `pip3 install opencv-python`.
Run `python3 vision/opencv_test.py` in the Terminal. The integrated console in vscode doesn't work.

# Setup Virtual Environment
## Setup Virtual Environment for Mac
1. Get to same level directory as the project you would like to create the virtual environment. 
2. Type 'python3 -m venv env' in your terminal. This creates the virtual environment.
3. Type 'source env/bin activate'. This will activate your virtual environment.
4. Only install packages when the right virtual environment is activated.
5. Type 'deactivate' to deactivate the virtual environment.

## Setup Virtual Environment for Windows
1. Get to same level directory as the project you would like to create the virtual environment. 
2. Type 'py -m pip install --user virtualenv' in your terminal. This installs the virtual environment creator.
3. Type 'py -m venv env' in your terminal. This creates the virtual environment.
4. Type '.\env\Scripts\activate' in your terminal. This will activate your virtual environment.
    - If it asks 'Do you want to run software from this untrusted publisher?' type 'A' to always run. This should be safe since you installed the virtual environment through pip.
5. Only install packages when the right virtual environment is activated.
6. Type 'deactivate' to deactivate the virtual environment.

# how to use dlib mouth detection
0. `brew install cmake` if on MacOS
1. install dlib and opencv (pip install opencv-python and pip install dlib)
2. go to hackohio2020/vision directory and run "python dlib_test.py"


# Dependencies
- `acapture` a faster webcam reader for OpenCV
- `pyglview` for drawing output to screen
- `opencv-python` for image manipulation
- `dlib` for face landmark detection


# UI
1. `export FLASK_APP=flask/server.py`
2. `flask run`