import random
from barcode.writer import ImageWriter
from barcode.ean import JAN
from PIL import Image


num = 1     # 100000
dir = "./Temp/"

while (num > 0):
    # ランダムな13桁の数字を生成
    random_number = "4567890123456"
    # JANコード画像の生成
    jan = JAN(random_number, writer=ImageWriter())
    # JANコード画像の保存
    jan.save(dir + random_number, {'format': 'JPEG', 'quiet_zone': 50, "module_width" : 6, "module_height" : 200, "font_size" : 200, "text_distance" : 100})
    
    num -= 1