from PIL import Image
from tensorflow.keras.models import load_model as tf
import time
import numpy as np





def model_loader(path):
    # モデルのロード
    model = tf(path)
    return model


def one_hot_vector_decoder(array):
    labels = {
        0: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        1: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
        2: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
        3: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
        4: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
        5: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
        6: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
        7: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
        8: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
        9: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    }

    # one-hotベクトルを元の数字に変換
    original_number = int(np.argmax(array))
    return original_number

def array_pluralize(array):
    arrays = []
    for i in range(13):
        pluralized_array = np.where(array == 255, i+1, 0)
        arrays.append(pluralized_array)
    return arrays




def BCD_Decorder(model, image, input_image_path, BCD_BarCode_Formatter):
    result = ""
    arrayed_image = BCD_BarCode_Formatter.BCD_BarCode_Formatter(image, input_image_path)
    arrays = array_pluralize(arrayed_image)
    # np.set_printoptions(threshold=np.inf) # numpy配列の出力を無限に
    # print(arrays)
    # print(arrayed_image)

    time_sta = time.perf_counter() # 時間計測開始
    
    for array in arrays:
        predictions = model.predict(array)
        result += str(one_hot_vector_decoder(predictions[0]))

    time_end = time.perf_counter() # 時間計測終了
    li_tim = time_end- time_sta

    return result, li_tim



if __name__=="__main__":
    import BCD_BarCode_Formatter
    # input_image_path = "Researches/Resources4567890123456.jpeg"
    input_image_path = "Training/Datasets10/4971964585943.jpeg"
    model_path = "Training/TrainedModel/20240108114046_v5_240107_d10000_n512_b1_e1_Adamax"
    model = model_loader(model_path)
    image = Image.open(input_image_path)
    result = BCD_Decorder(model, image, input_image_path, BCD_BarCode_Formatter)
    print(result)

