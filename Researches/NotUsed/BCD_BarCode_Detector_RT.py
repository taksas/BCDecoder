import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from roboflow import Roboflow
import json
from PIL import Image
import numpy as np
import datetime

# pip install roboflow opencv-python
# $env:ROBOFLOW_API_KEY = ""

rf = Roboflow(api_key=os.environ['ROBOFLOW_API_KEY'])
project = rf.workspace().project("barcode_detection_one")
model = project.version(1).model

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame)
    for result in results:
        prediction_json = result.json()
        print(prediction_json)
        x = prediction_json["x"]
        y = prediction_json["y"]
        w = prediction_json["width"]
        h = prediction_json["height"]
        image = prediction_json["image_path"]

        dt_now = datetime.datetime.now()
        pil_img = Image.fromarray(image)
        pil_img = pil_img.crop((y, x, y+w, x+h))
        pil_img.save('./Temp/'  + dt_now.strftime('%Y%m%d%H%M%S') + ".jpg")
        

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
