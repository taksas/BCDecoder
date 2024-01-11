import random
from barcode.writer import ImageWriter
from barcode.ean import JAN
from PIL import Image


num = 10     # 100000
dir = "./Temp/"

while (num > 0):
    # ランダムな13桁の数字を生成
    random_number = str(4948019210392)
    # JANコード画像の生成
    jan = JAN(random_number, writer=ImageWriter())
    # JANコード画像の保存
    jan.save(dir + "normal_" + random_number, {'format': 'JPEG', 'quiet_zone': 20, "module_width" : 3, "module_height" : 100, "font_size" : 100, "text_distance" : 40})
    
    num -= 1