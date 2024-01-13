import random
from barcode.writer import ImageWriter
from barcode.ean import JAN
from PIL import Image
import cv2
import os

# チェックデジットの計算
def check_digit(code):
    odd_sum = 0
    even_sum = 0

    for i in range(0,12):
        if i % 2 == 0:
            odd_sum += int(code[i])
        else:
            even_sum += int(code[i])

    return str((10 - (3 * even_sum + odd_sum)) % 10)



# 指定の色がどこにあるか数える
def find_color(image, target_color):

    image = image.convert('RGB')
    # 画像の幅と高さを取得
    width, height = image.size

    # 右から数えて最初に見つかるピクセルの座標を初期化
    target_position_right, target_position_left = None, None

    # 画像を右から左にスキャンして指定の色ピクセルを探す
    for x in range(width - 1, -1, -1):
        pixel = image.getpixel((x, 0))
        # print(pixel)
        # RGBの色が一致した場合
        if pixel == target_color:
            target_position_right = (x, 0)
            break

    # 画像を右から左にスキャンして指定の色ピクセルを探す
    for x in range(width):
        pixel = image.getpixel((x, 0))

        # RGBの色が一致した場合
        if pixel == target_color:
            target_position_left = (x, 0)
            break

    return target_position_right, target_position_left




def image_binarization(input_image_path, threshold):
    grayscale_img = cv2.imread(input_image_path,cv2.IMREAD_GRAYSCALE) #カラー画像を白黒画像で読み出し
    ret, binarized_img = cv2.threshold(grayscale_img, threshold, 255, cv2.THRESH_BINARY) #二値化
    if not ret:
        return
    return binarized_img




def splitted_create(num, index, total):
    temp_dir = "./Temp/"
    dir = "./Training/Datasets_v0108/Dataset" + str(total) + "_Split/Dataset" + str(total) + "_Index" + str(index) + "/"
    os.makedirs(dir)


    # csvの読み込み
    while (num > 0):
        # ランダムな12桁の数字を生成
        digit = 10 # 桁数
        ten_number = str(random.randrange(10**(digit-1),10**digit))
        random_number = str(random.choice([45, 49])) + ten_number
        random_number += check_digit(random_number) # チェックデジットを付加
        # JANコード画像の生成
        jan = JAN(random_number, writer=ImageWriter())
        # JANコード画像の保存
        jan.save(temp_dir + random_number, {'format': 'JPEG', 'quiet_zone': 1, "module_width" : 0.3, "module_height" : 5, "font_size" : 7, "text_distance" : 3})
        
        # 画像を開く
        temp_image_path = temp_dir + random_number + ".jpeg"
        # 切り取った画像を保存
        original_image = Image.open(temp_image_path)

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
        cropped_image.save(temp_image_path)

        # まずは2値化
        threshold = 150     #二値化したい閾値
        binarized_img_array = image_binarization(temp_image_path, threshold)
        binarized_img = Image.fromarray(binarized_img_array)
        # # print(binarized_img_raw)
        # binarized_img_raw.save('./Outputs/'  + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg")


        # 指定の色がどこにあるか数える
        target_color = (0, 0, 0)  # 黒色指定
        target_position_right, target_position_left = find_color(binarized_img, target_color)
        # print(target_position_right, target_position_left)
        # binarized_img_raw.save('./Outputs/'  + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg")

        # 画像を切り取る
        cropped_binarized_img = binarized_img.crop((target_position_left[0], 0, target_position_right[0] + 1, 1))
        cropped_image_path = dir + random_number + ".jpeg"
        cropped_binarized_img.save(cropped_image_path)
        # print(np.array(cropped_binarized_img))

        os.remove(temp_dir + random_number + ".jpeg")


        

        num -= 1


if __name__=="__main__":
    batch_size = 10 # 1つ当たりに生成する画像数
    batch_num = 20 # 作成数
    # 合計の画像数 = batch_size * batch_num
    for i in range(batch_num):
        splitted_create(batch_size, i, batch_size * batch_num)