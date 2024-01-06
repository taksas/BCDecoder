import customtkinter
import keyboard


# --- Global Variables ---
default_font = ("meiryo", 15)
default_font_65px = ("meiryo", 65)
show_help = True
# ------------------------



# -------- Texts ---------
text_raw_image = "(これはヘルプ画面です。F1キー押下で表示切替)\n入力されたバーコード画像"
text_raw_compare = "機械学習版デコーダーと\nPythonライブラリのデコーダーの結果を比較"
text_raw_merchandise_search = "特定したJANコードから商品検索。要ネット接続"
text_raw_log = "各種設定"
text_raw_sanity_check = "構成\nチェック"
# ------------------------



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
        return self # 返す☆彡

    
    # ベースフレーム
    def create_basic_frames(self):
        self.frame_l1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=470)
        self.frame_l1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l1.place(x=10, y=10)

        self.frame_l2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=350)
        self.frame_l2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l2.place(x=10, y=490)

        self.frame_l3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1500, height=140)
        self.frame_l3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_l3.place(x=10, y=850)


        self.frame_r1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=770)
        self.frame_r1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r1.place(x=1520, y=10)
        
        self.frame_r2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=390, height=200)
        self.frame_r2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame_r2.place(x=1520, y=790)
        



    



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
