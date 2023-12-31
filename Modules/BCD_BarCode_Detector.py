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


def BCD_BarCode_Detector(model_name, image_array, ROBOFLOW_API_KEY, output_path):

    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project(model_name)
    model = project.version(1).model

    result = model.predict(image_array).json()
    print(result)
    if(result["predictions"] == []): return
    result = result["predictions"][0]
    x = result["x"]
    y = result["y"]
    w = result["width"]
    h = result["height"]
    image = result["image_path"]

        
    pil_img = Image.fromarray(image)
    pil_img = pil_img.crop((x-w/2, y-w/2, x+w/2, y+h/2))
    pil_img.save(output_path)




if __name__=="__main__":
    model_name = "yolov7-ocr"
    image_array = np.array(Image.open("C:\\Users\\TAKUMI\\Videos\\iVCam\\20231231095434.jpg"))
    ROBOFLOW_API_KEY = os.environ['ROBOFLOW_API_KEY']
    dt_now = datetime.datetime.now()
    output_path = './Temp/'  + dt_now.strftime('%Y%m%d%H%M%S') + ".jpg"

    BCD_BarCode_Detector(model_name, image_array, ROBOFLOW_API_KEY, output_path)