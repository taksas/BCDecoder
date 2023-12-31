import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import numpy as np
import datetime
from roboflow import Roboflow

import BCD_BarCode_Detector


# pip install roboflow opencv-python
ROBOFLOW_API_KEY = os.environ['ROBOFLOW_API_KEY']




def BCD_Realtime_Camera_For_Detector(model):

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        dt_now = datetime.datetime.now()
        output_path = './Temp/'  + dt_now.strftime('%Y%m%d%H%M%S') + ".jpg"

        BCD_BarCode_Detector.BCD_BarCode_Detector(model, frame, ROBOFLOW_API_KEY, output_path)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__=="__main__":
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project("yolov7-ocr")
    model = project.version(1).model
    
    BCD_Realtime_Camera_For_Detector(model)