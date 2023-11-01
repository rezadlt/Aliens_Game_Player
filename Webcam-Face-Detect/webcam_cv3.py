import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import requests

#requests.post('http://localhost:5000/instructions', json={'direction': 'left'})
cascPath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

counter_l = counter_r = 0

COUNTER_TRESHOLD = 3
LEFT_TRHESHOLD = 350
RIGHT_TRHESHOLD = 600

sleep(2)

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        try:
            # print(counter_l, counter_r)
            if x < LEFT_TRHESHOLD:
                counter_r = (counter_r + 1) % COUNTER_TRESHOLD
                if counter_r == 0:
                    counter_l = 0
                    print("right")
                    requests.post('http://localhost:5000/instructions', json={'direction': 'right'})
            elif x > RIGHT_TRHESHOLD:
                counter_l = (counter_l + 1) % COUNTER_TRESHOLD
                if counter_l == 0:
                    counter_r = 0
                    print("left")
                    requests.post('http://localhost:5000/instructions', json={'direction': 'left'})
        except requests.exceptions.ConnectionError:
            pass
        # print(x, y, w, h)

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

    # # Display the resulting frame
    # cv2.imshow('Video', frame)


    # # Display the resulting frame
    # cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
