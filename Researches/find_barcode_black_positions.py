from PIL import Image

def find_color(image_path, target_color):
    # 画像を開く
    image = Image.open(image_path)

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

# 使用例
input_image_path = "./Training/Datasets/4511593873163.jpeg"
target_color = (0, 0, 0)  # 例: 赤色 (RGB)

target_position_right, target_position_left = find_color(input_image_path, target_color)

if target_position_right:
    print(f"指定の色ピクセルが最初に見つかる座標 (右から数える): {target_position_right}")
    print(f"指定の色ピクセルが最初に見つかる座標 (左から数える): {target_position_left}")
else:
    print("指定の色ピクセルは画像中に見つかりませんでした。")
