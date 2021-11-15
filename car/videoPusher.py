import cv2
import requests
import base64
import json

cap = cv2.VideoCapture(2)

while True:

    retval, image = cap.read()
    image = cv2.resize(image, (320, 240))
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    result = requests.post("http://localhost:9000/image",
                           headers={"content-type": "application/json"},
                           data=json.dumps({"image": str(jpg_as_text)[1:-1]}))

cap.release()
