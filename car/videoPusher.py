import cv2
import requests
import base64
import json

cap = cv2.VideoCapture(0)

while True:

    retval, image = cap.read()
    image = cv2.resize(image, (320, 240))
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    result = requests.post("http://ttm41-bfflo-17c606og763lz-1083556350.eu-west-1.elb.amazonaws.com/image/",
                           headers={"content-type": "application/json"},
                           data=json.dumps({"image": str(jpg_as_text)[1:-1]}))

cap.release()
