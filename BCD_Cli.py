import customtkinter
import keyboard
from PIL import Image
from pyzbar.pyzbar import decode
import time

import Modules.BCD_Decorder as BCD_Decorder
import Modules.BCD_BarCode_Formatter as BCD_BarCode_Formatter

# テキストから適宜生成用
import Modules.BCD_BarCode_Creater_from_Input as BCD_BarCode_Creater_from_Input
import Modules.BCD_BarCode_Generator_v0108_COPYED as BCD_BarCode_Generator_v0108_COPYED




# --- Global Static Variables ---
default_font = ("meiryo", 15)
default_font_45px = ("meiryo", 25)
default_font_65px = ("meiryo", 35)
default_font_72px = ("meiryo", 54)
model_info = "20240114114338_v10_240112_d1000000_n512_b512_e500_Adamax"
model_folder_path = "Training/TrainedModel/"
model_path = model_folder_path + model_info
model = BCD_Decorder.model_loader(model_path)
# ------------------------


# --- Global Variables ---
show_help = True
l1_image_area = ""
l2__frame_upper_1__squares = ""
l2__frame_upper_3__squares = ""
help_txt_raw_model_info = ""
l2__frame_upper_1__time = ""
l2__frame_upper_3__time = ""
r1__tab2_entry = ""
radio1_var = ""
# ------------------------


# -------- Texts ---------
text_raw_image = "入力されたバーコード画像を表示\n(これはヘルプ画面です)\n(F1キーで通常モードと切り替え)"
text_raw_compare = "機械学習版デコーダー\nと\nPythonライブラリのデコーダー  の結果を比較"
text_raw_model_info = "使用しているモデル情報"
text_raw_control = "操作エリア"
text_raw_frame_l2__frame_upper_2__desc = "↑pyzbar(ライブラリ)版     VS           機械学習版↓                          (ms)"
text_raw_waiting = "待機中..."
text_raw_file_select = "バーコードの\n画像ファイルを\n選択"
text_raw_tab1 = "画像を選択"
text_raw_tab2 = "数字から生成した画像を利用"
text_raw_r1_tab2_entry = "10桁の数字"
text_raw_create_from_input = "バーコード画像\nを\n生成"
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
            "1280x700"
        )  # Setting form size
        # self.attributes("-topmost", 1)   # Display at the front
        self.title("BarCodeDecorder Client")
        self.create_basic_frames()
        self.help_windows = self.create_help_frames()

    # ヘルプ関連のフレームを作り、後の操作用にフレームを返す
    def create_help_frames(self):
        self.helpframe = customtkinter.CTkFrame(master=self, border_width=0, width=1280, height=700)
        self.helpframe.place(x=0, y=0)
        # self_origin = self
        self = self.helpframe

        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=900, height=300)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)
        self.frame_l1.help_txt_image = customtkinter.CTkLabel(master=self.frame_l1, text=text_raw_image, font=default_font_65px)
        self.frame_l1.help_txt_image.place(x=10, y=1) # 各masterフレームからの相対座標

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1260, height=300)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=320)
        self.frame_l2.help_txt_compare = customtkinter.CTkLabel(master=self.frame_l2, text=text_raw_compare, font=default_font_65px)
        self.frame_l2.help_txt_compare.place(x=10, y=1)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1260, height=60)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=630)
        self.help_txt_raw_model_info = customtkinter.CTkLabel(master=self.frame_l3, text=text_raw_model_info, font=default_font_65px)
        self.help_txt_raw_model_info.place(x=10, y=1)
        

        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=350, height=300)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=920, y=10)
        self.help_txt_raw_log = customtkinter.CTkLabel(master=self.frame_r1, text=text_raw_control, font=default_font_65px)
        self.help_txt_raw_log.place(x=10, y=1)
        
        self.pack()
        return self # 返す
        

    
    # ベースフレーム
    def create_basic_frames(self):


        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=900, height=300)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)
        self.create_each_components_l1(self.frame_l1)

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1260, height=300)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=320)
        self.create_each_components_l2(self.frame_l2)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1260, height=60)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=630)
        self.help_txt_raw_model_info = customtkinter.CTkLabel(master=self.frame_l3, text=model_info, font=default_font_45px)
        self.help_txt_raw_model_info.place(x=10, y=1)
        global help_txt_raw_model_info
        help_txt_raw_model_info = self.help_txt_raw_model_info


        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=350, height=300)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=920, y=10)
        self.create_each_components_r1(self.frame_r1)
        

        
        

        

    

    # L1コンポーネントを作成（画像を表示するやつ）
    def create_each_components_l1(self, self_l1):
        img = resize_image_with_aspect_ratio("Resources/title.png", (890, 290))
        tk_image = customtkinter.CTkImage(light_image=img, size=(890, 290))
        self_l1.image_area = customtkinter.CTkLabel(master=self_l1, image=tk_image, text='')
        self_l1.image_area.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        global l1_image_area
        l1_image_area = self_l1.image_area
    
    # L1コンポーネントを「更新」
    def update_each_components_l1(self, file_name):
        img = resize_image_with_aspect_ratio(file_name, (890, 290))
        tk_image = customtkinter.CTkImage(light_image=img, size=(890, 290))
        l1_image_area.configure(image=tk_image)
    

    # L2コンポーネントを作成（pythonライブラリと機械学習版を比較するやつ）
    def create_each_components_l2(self, self_l2):

        # ライブラリ版部分
        self_l2.frame_upper_1 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=800, height=70)
        self_l2.frame_upper_1.place(x=10, y=10)
        self_l2.frame_upper_1.squares = []
        for i in range(13):
            temp_square = customtkinter.CTkFrame(master=self_l2.frame_upper_1, border_color="gray", border_width=1, width=84, height=84)
            temp_square.grid(row=0, column=i, padx=5, pady=5, sticky="s")

            temp_square.text_area = customtkinter.CTkLabel(master=temp_square, text="", font=default_font_72px, fg_color="transparent") # 各数字用label
            temp_square.text_area.place(x=30, y=1)
            self_l2.frame_upper_1.squares.append(temp_square)
        global l2__frame_upper_1__squares
        l2__frame_upper_1__squares = self_l2.frame_upper_1.squares
       
        # 説明部分のフレーム
        self_l2.frame_upper_2 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1240, height=90)
        self_l2.frame_upper_2.place(x=10, y=100)



        # 説明用ラベル
        customtkinter.CTkLabel(master=self_l2.frame_upper_2, text=text_raw_frame_l2__frame_upper_2__desc, font=default_font_65px).place(x=10, y=25)

         # 処理速度計測用(ライブラリ)
        self_l2.frame_upper_1.time = customtkinter.CTkLabel(master=self_l2.frame_upper_2, text="? ? ? ?", font=default_font_65px)
        self_l2.frame_upper_1.time.place(x=1000, y=0)
        global l2__frame_upper_1__time
        l2__frame_upper_1__time = self_l2.frame_upper_1.time



        


        # 機械学習版部分
        self_l2.frame_upper_3 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=800, height=100)
        self_l2.frame_upper_3.place(x=10, y=200)
        self_l2.frame_upper_3.squares = []
        for i in range(13):
            temp_square = customtkinter.CTkFrame(master=self_l2.frame_upper_3, border_color="gray", border_width=1, width=84, height=84)
            temp_square.grid(row=0, column=i, padx=5, pady=5, sticky="s")

            temp_square.text_area = customtkinter.CTkLabel(master=temp_square, text="", font=default_font_72px, fg_color="transparent") # 各数字用label
            temp_square.text_area.place(x=30, y=1)
            self_l2.frame_upper_3.squares.append(temp_square)
        global l2__frame_upper_3__squares
        l2__frame_upper_3__squares = self_l2.frame_upper_3.squares
        # 処理速度計測用
        self_l2.frame_upper_3.time = customtkinter.CTkLabel(master=self_l2.frame_upper_2, text="? ? ? ?", font=default_font_65px)
        self_l2.frame_upper_3.time.place(x=1000, y=50)
        global l2__frame_upper_3__time
        l2__frame_upper_3__time = self_l2.frame_upper_3.time



    # R1コンポーネントを作成（画像選択とかするやつ）
    def create_each_components_r1(self, self_r1):

        # バーコードを選択するファイルピッカを表示
        def button_event():
            file_name = customtkinter.filedialog.askopenfilename(filetypes=[("image file", "*.png;*.jpeg;*.jpg")])
            start_main_processes(file_name)
        
        # 入力されたコードからバーコードを生成し、それを用いて動作させる
        def button_create_from_input():
            global radio1_var
            entry = r1__tab2_entry.get()
            print("var:", radio1_var.get())
            print("entry:", entry)
            if(type(entry) != str): return
            text = ""
            if(radio1_var.get() == 1): text += "45"
            else: text += "49"
            text += entry
            print(text)
            barcode_path = BCD_BarCode_Creater_from_Input.create_barcode_from_input(text, BCD_BarCode_Generator_v0108_COPYED)
            start_main_processes(barcode_path)

        tabview = customtkinter.CTkTabview(master=self_r1, width=330, height=280)
        tabview.pack(padx=20, pady=20)
        tabview.place(x=10, y=10)

        tabview.add(text_raw_tab1)
        tabview.add(text_raw_tab2) 
        tabview.set(text_raw_tab1)  # デフォルトタブの指定

        # タブ1の設定
        self_r1.tab1_button = customtkinter.CTkButton(tabview.tab(text_raw_tab1), text=text_raw_file_select, font=default_font_45px, command=button_event)
        self_r1.tab1_button.place(x=10, y=10)

        # タブ2の設定
        global radio1_var
        radio1_var = customtkinter.IntVar(master=self, value=0)
        customtkinter.CTkRadioButton(master=tabview.tab(text_raw_tab2), text="45", font=default_font_45px, variable=radio1_var, value=1).place(x=10, y=0)
        customtkinter.CTkRadioButton(master=tabview.tab(text_raw_tab2), text="49", font=default_font_45px, variable=radio1_var, value=2).place(x=100, y=0)
        self_r1.tab2_entry = customtkinter.CTkEntry(master=tabview.tab(text_raw_tab2), placeholder_text=text_raw_r1_tab2_entry, font=default_font_45px, width=180, height = 45)
        self_r1.tab2_entry.place(x=10, y=40)
        global r1__tab2_entry
        r1__tab2_entry = self_r1.tab2_entry
        self_r1.tab2_button = customtkinter.CTkButton(tabview.tab(text_raw_tab2), text=text_raw_create_from_input, font=default_font_45px, command=button_create_from_input)
        self_r1.tab2_button.place(x=10, y=90)





    



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
    # decoded_data_ml, li_tim = ("4444444444444",  4444)  # テスト用！！！
    decoded_data_ml, li_tim = BCD_Decorder.BCD_Decorder(model, file_img, file_name, BCD_BarCode_Formatter)
    
    l2__frame_upper_3__time.configure(text=str(li_tim*1000)[0:7])

    # L2フレーム内機械学習版表示領域を更新
    for decoded_char_li, decoded_char_ml, square in zip(decoded_data_library, decoded_data_ml, l2__frame_upper_3__squares):
        square.text_area.configure(text=decoded_char_ml)
        color = "green"
        if(decoded_char_li != decoded_char_ml): color = "red"
        square.configure(fg_color=color)
    

    



if __name__ == "__main__":
    app.mainloop()
