import random
from barcode.writer import ImageWriter
from barcode.ean import JAN
from PIL import Image
import cv2
import os



def create_barcode_from_input(text, BCD_BarCode_Generator_v0108):

    temp_dir = "./Temp/"
    random_number = text
    random_number += BCD_BarCode_Generator_v0108.check_digit(random_number) # チェックデジットを付加
    # JANコード画像の生成
    jan = JAN(random_number, writer=ImageWriter())
    # JANコード画像の保存
    jan.save(temp_dir + random_number, {'format': 'JPEG', 'quiet_zone': 1, "module_width" : 0.3, "module_height" : 5, "font_size" : 1, "text_distance" : 5})
    
    # 画像のパス
    temp_image_path = temp_dir + random_number + ".jpeg"

    # 数字部分以外切り取り
    temp_image = Image.open(temp_image_path)
    width, height = temp_image.size
    temp_image.crop((0, 0, width, 85)).save(temp_image_path)

    # 2値化
    threshold = 150     #二値化したい閾値
    binarized_img_array = BCD_BarCode_Generator_v0108.image_binarization(temp_image_path, threshold)
    binarized_img_raw = Image.fromarray(binarized_img_array)
    # # print(binarized_img_raw)
    binarized_img_raw.save(temp_image_path)



    return temp_image_path



if __name__=="__main__":
    import BCD_BarCode_Generator_v0108_COPYED

    text = "491234567890"


    print(create_barcode_from_input(text, BCD_BarCode_Generator_v0108_COPYED))