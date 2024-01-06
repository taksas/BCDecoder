from PIL import Image
import cv2
import datetime

# 指定の色がどこにあるか数える
def find_color(image, target_color):

    # 画像の幅と高さを取得
    width, height = image.size

    # 右から数えて最初に見つかるピクセルの座標を初期化
    target_position_right, target_position_left = None, None

    # 画像を右から左にスキャンして指定の色ピクセルを探す
    for x in range(width - 1, -1, -1):
        pixel = image.getpixel((x, 0))

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



# 画像を2値化
def BCD_BarCode_Formatter(input_image_path):
    
    # まずは2値化
    threshold = 150 #二値化したい閾値
    binarized_img = image_binarization(input_image_path, threshold)
    binarized_img_raw = Image.fromarray(binarized_img)

    dt_now = datetime.datetime.now()
    binarized_img_raw.save('./Temp/'  + dt_now.strftime('%Y%m%d%H%M%S') + ".jpg")

    # 指定の色がどこにあるか数える
    target_color = (0, 0, 0)  # 黒色指定
    target_position_right, target_position_left = find_color(binarized_img, target_color)
    if target_position_right:
        print(f"指定の色ピクセルが最初に見つかる座標 (右から数える): {target_position_right}")
        print(f"指定の色ピクセルが最初に見つかる座標 (左から数える): {target_position_left}")
    else:
        print("指定の色ピクセルは画像中に見つかりませんでした。")



if __name__=="__main__":
    input_image_path = "C:\\Users\\TAKUMI\\git\\BCDecoder\\Researches\\Resources\\20231231102435.jpg"

    BCD_BarCode_Formatter(input_image_path)