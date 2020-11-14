import cv2
import acapture
import dlib
import pyglview
viewer = pyglview.Viewer()

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# read the image
cap = acapture.open(0)


def loop():
    check, frame = cap.read()
    # Convert image into grayscale
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

    # Use detector to find landmarks
    faces = detector(gray)

    for face in faces:
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        # Create landmark object
        landmarks = predictor(image=gray, box=face)

        # Loop through all the points
        for n in range(48, 60):
            x = landmarks.part(n).x
            y = landmarks.part(n).y

            # Draw a circle
            cv2.circle(img=frame, center=(x, y), radius=3,
                       color=(0, 255, 0), thickness=-1)

    # show the image
    # cv2.imshow(winname="Face", mat=frame)
    if check:
        viewer.set_image(frame)

    # Exit when escape is pressed
    if cv2.waitKey(delay=1) == 27:
        sys.exit()


viewer.set_loop(loop)
viewer.start()

# When everything done, release the video capture and video write objects
cap.release()
