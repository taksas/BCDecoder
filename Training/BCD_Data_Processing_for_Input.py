#%%
# 機械学習のライブラリ関連をインポート
import numpy as np

# ファイル操作
import os

# 画像操作
from PIL import Image



#%%
# DIRS
DATASET_NUM = 1
DIRS_DATASET = "../Training/Datasets_v0108/Dataset" + str(DATASET_NUM) + "/"
SAVING_DIR = "../Training/Datasets_v0108_AfterProcessing/" + str(DATASET_NUM) + ".npz" # 処理後のnumpyエクスポート保存先



#%%
# ファイルを取得, 配列に格納, Pythonリスト型をnumpy.ndarray型に変換
file_names = []
    
# フォルダ内のファイルを取得
files = os.listdir(DIRS_DATASET)

# ファイル名を配列に格納
for file in files:
    file_names.append(file)

# Pythonリスト型をnumpy.ndarray型に変換
file_names = np.array(file_names)




#%%
file_names



#%%

def convert_to_grayscale(numpy_array):
    # グレーと言わず2値化
    grayscale_array = np.where(numpy_array <= 128, 0, 255)
    # plt.imshow(grayscale_array) # こいつらのせいで処理が重かった。出力系は要注意
    # print(grayscale_array)
    return grayscale_array





#%%
### 画像を配列にしてよしなに
X, y = [], []



#%%
for file_name in file_names:
    numpy_array = np.array(Image.open(DIRS_DATASET + file_name)) # 画像をnumpy配列にする
    # print(numpy_array)
    grayscale_array = convert_to_grayscale(numpy_array)
    # print(grayscale_array)
    for i in range(13):
        # grayscale_array1 = np.where(np.all(grayscale_array == 0, axis=-1), 0, 255)
        # print(grayscale_array1)
        grayscale_array2 = np.where(grayscale_array == 255, i+1, 0)
        # print(grayscale_array2)
        X.append(grayscale_array2)
        y.append(file_name[i])



#%%
# X, yをPythonリスト型をnumpy.ndarray型に変換
X = np.array(X)
X = X.squeeze()
y = np.array(y, dtype=int)

#%%
X
#%%
y
#%%
# ラベルデータをone-hotベクトルに直す
def one_hot_vector(y):
    labels = {
        0: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        1: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
        2: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
        3: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
        4: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
        5: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
        6: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
        7: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
        8: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
        9: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    }

    y = np.array(list(map(lambda v : labels[v] , y)))
    return y

#%%
y = one_hot_vector(y)

#%%
# 完成
# np.set_printoptions(threshold=np.inf) # numpy配列の出力を無限に
#%%
print(type(X))
X
#%%
print(type(y))
y

#%%
# 保存
np.savez_compressed(SAVING_DIR, X, y)
