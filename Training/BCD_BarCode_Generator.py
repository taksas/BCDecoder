import random
from barcode.writer import ImageWriter
from barcode.ean import JAN
from PIL import Image


num = 10000     # 100000
dir = "./Training/Datasets10000/"


# csvの読み込み
while (num > 0):
    # ランダムな13桁の数字を生成
    random_number = str(random.choice([45, 49])) + str(random.randint(10**10, 10**11 - 1))
    # JANコード画像の生成
    jan = JAN(random_number, writer=ImageWriter())
    # JANコード画像の保存
    jan.save(dir + random_number, {'format': 'JPEG', 'quiet_zone': 0, "module_width" : 0.1, "module_height" : 0.1, "font_size" : 1, "text_distance" : 0.4})
    
    # 画像を開く
    original_image = Image.open(dir + random_number + ".jpeg")

    # 画像の幅と高さを取得
    width, height = original_image.size

    # 中央部分を切り取る範囲を計算
    left = 0
    top = 11
    right = width
    bottom = 11 + 1  # 縦1ピクセル

    # 中央部分を切り取る
    cropped_image = original_image.crop((left, top, right, bottom))

    # 切り取った画像を保存
    cropped_image.save(dir + random_number + ".jpeg")

    num -= 1