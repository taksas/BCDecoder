import customtkinter
import keyboard
from PIL import Image
from pyzbar.pyzbar import decode
import time

import Modules.JankenJP_Kakeibo_Parser as JankenJP_Kakeibo_Parser
import Modules.BCD_Decorder as BCD_Decorder
import Modules.BCD_BarCode_Formatter as BCD_BarCode_Formatter

# --- Global Static Variables ---
default_font = ("meiryo", 15)
default_font_45px = ("meiryo", 45)
default_font_65px = ("meiryo", 65)
default_font_72px = ("meiryo", 72)
model_path = "Training/TrainedModel/20240108114046_v5_240107_d10000_n512_b1_e1_Adamax"
model = BCD_Decorder.model_loader(model_path)
# ------------------------


# --- Global Variables ---
show_help = True
l1_image_area = ""
l2__frame_upper_1__squares = ""
l2__frame_upper_3__squares = ""
help_txt_raw_merchandise_search = ""
l2__frame_upper_1__time = ""
l2__frame_upper_3__time = ""
# ------------------------


# -------- Texts ---------
text_raw_image = "入力されたバーコード画像を表示\n(これはヘルプ画面です)\n(F1キーで通常モードと切り替え)"
text_raw_compare = "機械学習版デコーダー\nと\nPythonライブラリのデコーダー  の結果を比較"
text_raw_merchandise_search = "特定したJANコードから商品検索(要ネット接続)"
text_raw_control = "操作エリア"
text_raw_frame_l2__frame_upper_2__desc = "↑pyzbar(ライブラリ)版     VS           機械学習版↓       (ms)"
text_raw_waiting = "待機中..."
text_raw_file_select = "バーコードの\n画像ファイルを\n選択"
# ------------------------




def resize_image_with_aspect_ratio(image_path, target_size):
    # 画像の読み込み
    img = Image.open(image_path)

    # 元のサイズ取得
    original_width, original_height = img.size

    # ターゲットサイズとのアスペクト比比較
    target_width, target_height = target_size
    aspect_ratio_target = target_width / target_height
    aspect_ratio_original = original_width / original_height

    # リサイズ後のサイズ計算
    if aspect_ratio_original > aspect_ratio_target:
        new_width = target_width
        new_height = int(target_width / aspect_ratio_original)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio_original)

    # 画像のリサイズ
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # 黒色の背景画像作成
    background = Image.new('RGB', target_size, (0, 0, 0))
    
    # 背景に画像を中央に貼り付け
    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2
    background.paste(img, (x, y, x + new_width, y + new_height))

    # 保存
    return background







class App(customtkinter.CTk):  # CustomTKinter (GUI) Class
    def __init__(self):
        super().__init__()
        self.iconbitmap("Resources/icon.ico")
        self.geometry(
            "1920x1000"
        )  # Setting form size
        # self.attributes("-topmost", 1)   # Display at the front
        self.title("BarCodeDecorder Client")
        self.create_basic_frames()
        self.help_windows = self.create_help_frames()

    # ヘルプ関連のフレームを作り、後の操作用にフレームを返す
    def create_help_frames(self):
        self.helpframe = customtkinter.CTkFrame(master=self, border_width=0, width=1920, height=1000)
        self.helpframe.place(x=0, y=0)
        # self_origin = self
        self = self.helpframe

        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=470)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)
        self.frame_l1.help_txt_image = customtkinter.CTkLabel(master=self.frame_l1, text=text_raw_image, font=default_font_65px)
        self.frame_l1.help_txt_image.place(x=10, y=1) # 各masterフレームからの相対座標

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1900, height=390)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=490)
        self.frame_l2.help_txt_compare = customtkinter.CTkLabel(master=self.frame_l2, text=text_raw_compare, font=default_font_65px)
        self.frame_l2.help_txt_compare.place(x=10, y=1)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1900, height=100)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=890)
        self.help_txt_raw_merchandise_search = customtkinter.CTkLabel(master=self.frame_l3, text=text_raw_merchandise_search, font=default_font_65px)
        self.help_txt_raw_merchandise_search.place(x=10, y=1)
        

        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=470)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=1520, y=10)
        self.help_txt_raw_log = customtkinter.CTkLabel(master=self.frame_r1, text=text_raw_control, font=default_font_65px)
        self.help_txt_raw_log.place(x=10, y=1)
        
        self.pack()
        return self # 返す
        

    
    # ベースフレーム
    def create_basic_frames(self):

        def button_event():
            file_name = customtkinter.filedialog.askopenfilename(filetypes=[("image file", "*.png;*.jpeg;*.jpg")])
            start_main_processes(file_name)


        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=470)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)
        self.create_each_components_l1(self.frame_l1)

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1900, height=390)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=490)
        self.create_each_components_l2(self.frame_l2)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1900, height=100)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=890)
        self.help_txt_raw_merchandise_search = customtkinter.CTkLabel(master=self.frame_l3, text=text_raw_waiting, font=default_font_65px)
        self.help_txt_raw_merchandise_search.place(x=10, y=1)
        global help_txt_raw_merchandise_search
        help_txt_raw_merchandise_search = self.help_txt_raw_merchandise_search


        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=470)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=1520, y=10)
        self.frame_r1.button = customtkinter.CTkButton(self.frame_r1, text=text_raw_file_select, width=300, height=100, font=default_font_45px, command=button_event)
        self.frame_r1.button.place(x=10, y=10)

        
        

        

    

    # L1コンポーネントを作成（画像を表示するやつ）
    def create_each_components_l1(self, self_l1):
        img = resize_image_with_aspect_ratio("Resources/title.png", (1490, 460))
        tk_image = customtkinter.CTkImage(light_image=img, size=(1490, 460))
        self_l1.image_area = customtkinter.CTkLabel(master=self_l1, image=tk_image, text='')
        self_l1.image_area.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        global l1_image_area
        l1_image_area = self_l1.image_area
    
    # L1コンポーネントを「更新」
    def update_each_components_l1(self, file_name):
        img = resize_image_with_aspect_ratio(file_name, (1490, 460))
        tk_image = customtkinter.CTkImage(light_image=img, size=(1490, 460))
        l1_image_area.configure(image=tk_image)
    

    # L2コンポーネントを作成（pythonライブラリと機械学習版を比較するやつ）
    def create_each_components_l2(self, self_l2):

        # ライブラリ版部分
        self_l2.frame_upper_1 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1880, height=100)
        self_l2.frame_upper_1.place(x=10, y=10)
        self_l2.frame_upper_1.squares = []
        for i in range(13):
            temp_square = customtkinter.CTkFrame(master=self_l2.frame_upper_1, border_color="gray", border_width=1, width=110, height=110)
            temp_square.grid(row=0, column=i, padx=5, pady=5, sticky="s")

            temp_square.text_area = customtkinter.CTkLabel(master=temp_square, text="", font=default_font_72px, fg_color="transparent") # 各数字用label
            temp_square.text_area.place(x=30, y=1)
            self_l2.frame_upper_1.squares.append(temp_square)
        global l2__frame_upper_1__squares
        l2__frame_upper_1__squares = self_l2.frame_upper_1.squares
        # 処理速度計測用
        customtkinter.CTkLabel(master=self_l2.frame_upper_1, text=" ", font=default_font_65px).grid(row=0, column=13, padx=5, pady=5, sticky="s")
        self_l2.frame_upper_1.time = customtkinter.CTkLabel(master=self_l2.frame_upper_1, text="? ? ? ?", font=default_font_65px)
        self_l2.frame_upper_1.time.grid(row=0, column=14, padx=5, pady=5, sticky="s")
        global l2__frame_upper_1__time
        l2__frame_upper_1__time = self_l2.frame_upper_1.time

        # 説明部分
        self_l2.frame_upper_2 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1880, height=100)
        self_l2.frame_upper_2.place(x=10, y=140)
        customtkinter.CTkLabel(master=self_l2.frame_upper_2, text=text_raw_frame_l2__frame_upper_2__desc, font=default_font_65px).place(x=10, y=10)

        # 機械学習版部分
        self_l2.frame_upper_3 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1880, height=100)
        self_l2.frame_upper_3.place(x=10, y=260)
        self_l2.frame_upper_3.squares = []
        for i in range(13):
            temp_square = customtkinter.CTkFrame(master=self_l2.frame_upper_3, border_color="gray", border_width=1, width=110, height=110)
            temp_square.grid(row=0, column=i, padx=5, pady=5, sticky="s")

            temp_square.text_area = customtkinter.CTkLabel(master=temp_square, text="", font=default_font_72px, fg_color="transparent") # 各数字用label
            temp_square.text_area.place(x=30, y=1)
            self_l2.frame_upper_3.squares.append(temp_square)
        global l2__frame_upper_3__squares
        l2__frame_upper_3__squares = self_l2.frame_upper_3.squares
        # 処理速度計測用
        customtkinter.CTkLabel(master=self_l2.frame_upper_3, text=" ", font=default_font_65px).grid(row=0, column=13, padx=5, pady=5, sticky="s")
        self_l2.frame_upper_3.time = customtkinter.CTkLabel(master=self_l2.frame_upper_3, text="? ? ? ?", font=default_font_65px)
        self_l2.frame_upper_3.time.grid(row=0, column=14, padx=5, pady=5, sticky="s")
        global l2__frame_upper_3__time
        l2__frame_upper_3__time = self_l2.frame_upper_3.time

    




    



# --- Global Variables ---
app = App()
# ------------------------


# ヘルプモード切替
def toggle_help_mode(key):
    global app
    global show_help

    show_help = not show_help
    if(show_help): app.help_windows.pack()
    else: app.help_windows.pack_forget()

    print("Help Mode Toggled:", show_help)




keyboard.on_press_key("f1", toggle_help_mode) # ヘルプモード用F1キー登録


# メイン機能
def start_main_processes(file_name):
    file_img = Image.open(file_name)
    app.update_each_components_l1(file_name) # 画像プレビューを更新


    # ライブラリ版(pyzbar)
    time_sta = time.perf_counter() # 時間計測開始
    decoded_list = decode(file_img)
    time_end = time.perf_counter() # 時間計測終了
    li_tim = time_end- time_sta
    l2__frame_upper_1__time.configure(text=str(li_tim*1000)[0:7])
    try:
        decoded_data_library = decoded_list[0].data
    except:
        decoded_data_library = "?????????????"
    decoded_data_library = str(decoded_data_library).replace('b', '').replace("'", '')
    print("Decoded by pyzbar:", decoded_data_library)
    

    # L2フレーム内ライブラリ版表示領域を更新
    for decoded_char, square in zip(decoded_data_library, l2__frame_upper_1__squares):
        square.text_area.configure(text=decoded_char)


    # 機械学習版
    # decoded_data_ml, li_tim = "4902750910454", 1234 # テスト用！！！
    decoded_data_ml, li_tim = BCD_Decorder.BCD_Decorder(model, file_img, file_name, BCD_BarCode_Formatter)
    
    l2__frame_upper_3__time.configure(text=str(li_tim*1000)[0:7])

    # L2フレーム内機械学習版表示領域を更新
    for decoded_char_li, decoded_char_ml, square in zip(decoded_data_library, decoded_data_ml, l2__frame_upper_3__squares):
        square.text_area.configure(text=decoded_char_ml)
        color = "green"
        if(decoded_char_li != decoded_char_ml): color = "red"
        square.configure(fg_color=color)
    

    search_result = JankenJP_Kakeibo_Parser.JankenJP_Kakeibo_Parser(decoded_data_ml) # じゃんけんJP家計簿で商品検索
    try:
        search_result = search_result[0] + ", " + search_result[3] + ", " + search_result[4]
    except:
        search_result = "特定できませんでした（JANコードエラー/未登録）"
    help_txt_raw_merchandise_search.configure(text=search_result) # L3コンポーネント（商品検索表示するやつ）を更新




if __name__ == "__main__":
    app.mainloop()
