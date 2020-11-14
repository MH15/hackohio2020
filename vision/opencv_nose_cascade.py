import cv2
import sys

# cascPath = sys.argv[1]
cascPath = "vision/Nariz.xml"
# Create the haar cascade
noseCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
# sys.exit()

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # roi_gray = gray[y:y+h, x:x+w]
    # roi_color = frame[y:y+h, x:x+w]

    # faces = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=5,
    #     minSize=(30, 30),
    #     flags=cv2.CASCADE_SCALE_IMAGE
    # )

    # Draw a rectangle around the faces
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    nose = noseCascade.detectMultiScale(gray)
    for (ex, ey, ew, eh) in nose:
        cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
