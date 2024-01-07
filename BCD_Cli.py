import customtkinter
import keyboard
from PIL import Image


# --- Global Variables ---
default_font = ("meiryo", 15)
default_font_65px = ("meiryo", 65)
show_help = True
# ------------------------



# -------- Texts ---------
text_raw_image = "入力されたバーコード画像を表示"
text_raw_compare = "機械学習版デコーダー\nと\nPythonライブラリのデコーダー  の結果を比較"
text_raw_merchandise_search = "特定したJANコードから商品検索(要ネット接続)"
text_raw_log = "操作エリア"
text_raw_sanity_check = "F1キーで\n画面切替"
frame_l2__frame_upper_2__desc = "↑ライブラリ版      VS      機械学習版↓"
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
        self = self.helpframe

        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=470)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)
        self.frame_l1.help_txt_image = customtkinter.CTkLabel(master=self.frame_l1, text=text_raw_image, font=default_font_65px)
        self.frame_l1.help_txt_image.place(x=1, y=1) # 各masterフレームからの相対座標

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=350)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=490)
        self.frame_l2.help_txt_compare = customtkinter.CTkLabel(master=self.frame_l2, text=text_raw_compare, font=default_font_65px)
        self.frame_l2.help_txt_compare.place(x=1, y=1)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=140)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=850)
        self.help_txt_raw_merchandise_search = customtkinter.CTkLabel(master=self.frame_l3, text=text_raw_merchandise_search, font=default_font_65px)
        self.help_txt_raw_merchandise_search.place(x=1, y=1)

        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=770)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=1520, y=10)
        self.help_txt_raw_log = customtkinter.CTkLabel(master=self.frame_r1, text=text_raw_log, font=default_font_65px)
        self.help_txt_raw_log.place(x=1, y=1)
        
        self.frame_r2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=200)
        self.frame_r2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r2.place(x=1520, y=790)
        self.help_txt_sanity_check = customtkinter.CTkLabel(master=self.frame_r2, text=text_raw_sanity_check, font=default_font_65px)
        self.help_txt_sanity_check.place(x=1, y=1)

        self.pack()
        return self # 返す
        

    
    # ベースフレーム
    def create_basic_frames(self):
        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=470)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)
        self.create_each_components_l1(self.frame_l1)

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=350)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=490)
        self.create_each_components_l2(self.frame_l2)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=140)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=850)


        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=770)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=1520, y=10)
        
        self.frame_r2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=200)
        self.frame_r2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r2.place(x=1520, y=790)
        
    

    # L1コンポーネントを作成（画像を表示するやつ）
    def create_each_components_l1(self, self_l1):
        img = resize_image_with_aspect_ratio("Resources/icon.png", (1490, 470))
        tk_image = customtkinter.CTkImage(light_image=img, size=(1490, 470))
        self_l1.image_area = customtkinter.CTkLabel(master=self_l1, image=tk_image, text='')
        self_l1.image_area.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    

    # L2コンポーネントを作成（pythonライブラリと機械学習版を比較するやつ）
    def create_each_components_l2(self, self_l2):

        # ライブラリ版部分
        self_l2.frame_upper_1 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1480, height=100)
        self_l2.frame_upper_1.place(x=10, y=10)
        self_l2.frame_upper_1.squares = []
        for i in range(13):
            temp_square = customtkinter.CTkFrame(master=self_l2.frame_upper_1, border_color="gray", border_width=1, width=85, height=85)
            temp_square.grid(row=0, column=i, padx=5, pady=5, sticky="s")
            self_l2.frame_upper_1.squares.append(temp_square)
        customtkinter.CTkLabel(master=self_l2.frame_upper_1, text="? ? ? s", font=default_font_65px).grid(row=0, column=13, padx=5, pady=5, sticky="s") # 処理速度計測用

        # 説明部分
        self_l2.frame_upper_2 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1480, height=100)
        self_l2.frame_upper_2.place(x=10, y=120)
        customtkinter.CTkLabel(master=self_l2.frame_upper_2, text=frame_l2__frame_upper_2__desc, font=default_font_65px).place(x=10, y=10)

        # 機械学習版部分
        self_l2.frame_upper_3 = customtkinter.CTkFrame(master=self_l2, fg_color="transparent", border_width=0, width=1480, height=100)
        self_l2.frame_upper_3.place(x=10, y=240)
        self_l2.frame_upper_3.squares = []
        for i in range(13):
            temp_square = customtkinter.CTkFrame(master=self_l2.frame_upper_3, border_color="gray", border_width=1, width=85, height=85)
            temp_square.grid(row=0, column=i, padx=5, pady=5, sticky="s")
            self_l2.frame_upper_3.squares.append(temp_square)
            # print(temp_square)
        customtkinter.CTkLabel(master=self_l2.frame_upper_3, text="? ? ? s", font=default_font_65px).grid(row=0, column=13, padx=5, pady=5, sticky="s") # 処理速度計測用


        return




    



# --- Global Variables ---
app = App()
# ------------------------


def toggled_help_mode(key):
    global app
    global show_help

    show_help = not show_help
    if(show_help): app.help_windows.pack()
    else: app.help_windows.pack_forget()

    print("Help Mode Toggled:", show_help)




keyboard.on_press_key("f1", toggled_help_mode)




if __name__ == "__main__":
    app.mainloop()
