from PIL import Image
import tensorflow as tf
import 


def BCD_Decorder(image):
    # モデルのロード
    model = tf.keras.models.load_model("Training/TrainedModel/20240108114046_v5_240107_d10000_n512_b1_e1_Adamax")
    predictions = model.predict(image)

    return predictions



if __name__=="__main__":
    image = Image.open("Researches/Resources4567890123456.jpeg")
    output = BCD_Decorder(image)
    print(output)

