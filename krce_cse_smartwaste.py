import numpy as np
import math
import cv2
import serial 
import cv2
import imutils
import numpy as np
import argparse
import time
import smtplib
import sys
import urllib.request
from keras.preprocessing.image import img_to_array
from keras.models import load_model

arduino = serial.Serial('COM8', 9600, timeout=.1)
time.sleep(2)
def arduino_rdata():
    data = arduino.readline()[:-2]
    data = data.decode("utf-8")
    data_v = str(data)
    data_v = data_v.split(" ")
    print(data_v)


def arduino_data(val):
    if val==1:
        arduino.write(b'1\r\n')
    elif val == 2:
        arduino.write(b'2\r\n')
    elif val == 3:
        arduino.write(b'3\r\n')
    return

cap = cv2.VideoCapture(0)
model=load_model('neural.model')
x = 1
while True:
    frameRate = cap.get(5) #frame rate
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    image = frame
    image = cv2.resize(image, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # classify the input image
    (nonbio, bio) = model.predict(image)[0]
    # build the label

    label = "Bio" if bio > nonbio else "Non-Bio"

    print(label)

    irr = arduino_rdata()
    y=label
    print(y)

    if y == "Bio":
        arduino_data(1)
    elif y == "Non-Bio":
        arduino_data(2)
    else:
        arduino_data(3)
    time.sleep(5)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
#vs.stop()
