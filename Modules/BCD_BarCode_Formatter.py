from PIL import Image
import cv2
import datetime
import numpy as np
import math

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


# def image_arrayization(image):
#     # 画像のサイズ取得
#     image_width, image_height = image.size
#     arrayed_image = np.array(image)

#     smalled_arrayed_image = np.array([])
#     for i in range(0, image_width, math.ceil(image_width/337)):
#         smalled_arrayed_image = np.append(smalled_arrayed_image, arrayed_image[0][i])
#     # print(smalled_arrayed_image)
#     return smalled_arrayed_image


# 画像を2値化
def BCD_BarCode_Formatter(image, input_image_path):

    # 画像のサイズ取得
    image_width, image_height = image.size

    # 真ん中部分だけ画像を切り取る
    image = image.crop((0, image_height // 2, image_width, image_height // 2 + 1))
    binarized_img_path = './Outputs/'  + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
    image.save(binarized_img_path)

    # まずは2値化
    threshold = 150     #二値化したい閾値
    binarized_img_array = image_binarization(binarized_img_path, threshold)
    binarized_img = Image.fromarray(binarized_img_array)
    # # print(binarized_img_raw)
    # binarized_img_raw.save('./Outputs/'  + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg")


    # 指定の色がどこにあるか数える
    target_color = (0, 0, 0)  # 黒色指定
    target_position_right, target_position_left = find_color(binarized_img, target_color)
    print(target_position_right, target_position_left)
    # binarized_img_raw.save('./Outputs/'  + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg")

    # 画像を切り取る
    cropped_binarized_img = binarized_img.crop((target_position_left[0], 0, target_position_right[0] + 1, 1))
    # cropped_binarized_img.save("./Outputs/b.jpg")
    # print(np.array(cropped_binarized_img))


    resized_cropped_binarized_img = cropped_binarized_img.resize((337, 1), resample=Image.NEAREST) # (337, 1)、学習時のサイズにリサイズ
    resized_cropped_binarized_img.save('./Outputs/' + "resized_cropped_binarized_img" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg")
    arrayed_resized_cropped_binarized_img = np.array(resized_cropped_binarized_img)

    # arrayed_resized_cropped_binarized_img = image_arrayization(cropped_binarized_img)
    # print(len(arrayed_resized_cropped_binarized_img))


    # squeezed_arrayed_resized_cropped_binarized_img = np.squeeze(arrayed_resized_cropped_binarized_img)
    # # np.set_printoptions(threshold=np.inf) # numpy配列の出力を無限に
    # print(len(squeezed_arrayed_resized_cropped_binarized_img))
    # print(squeezed_arrayed_resized_cropped_binarized_img)
    print(arrayed_resized_cropped_binarized_img)
    return arrayed_resized_cropped_binarized_img

    




if __name__=="__main__":
    # input_image_path = "Researches/Resources_highres_4567890123456.jpeg"
    # input_image_path = "Training/Datasets1/4525491507698.jpeg"
    input_image_path = "Temp/4915356823998cropped.jpeg" # サイズ適正テスト用

    image = Image.open(input_image_path)
    # print(np.array(image))
    arrayed_resized_cropped_binarized_img = BCD_BarCode_Formatter(image, input_image_path)
    # print(arrayed_resized_cropped_binarized_img)