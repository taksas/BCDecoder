import random
from barcode.writer import ImageWriter
from barcode.ean import JAN
from PIL import Image


num = 1     # 100000
dir = "./Researches/Resources"

while (num > 0):
    # ランダムな13桁の数字を生成
    random_number = "4567890123456"
    # JANコード画像の生成
    jan = JAN(random_number, writer=ImageWriter())
    # JANコード画像の保存
    jan.save(dir + random_number, {'format': 'JPEG'})
    
    num -= 1