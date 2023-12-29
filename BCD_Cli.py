import customtkinter
import keyboard
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime



class App(customtkinter.CTk):  # CustomTKinter (GUI) Class
    def __init__(self):
        super().__init__()
        self.fonts = ("meiryo", 15)
        # self.iconbitmap("Assets/headandlock.ico")
        self.geometry(
            "1920x1000"
        )  # Setting form size
        # self.attributes("-topmost", 1)   # Display at the front
        self.title("Face Sentinel")
        self.create_basic_frames()
    
    def create_basic_frames(self):
        self.frame1 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1200, height=200)
        self.frame1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame1.place(x=10, y=10)

        self.frame2 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=690, height=200)
        self.frame2.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame2.place(x=1220, y=10)

        self.frame3 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=1200, height=770)
        self.frame3.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame3.place(x=10, y=220)
        
        self.frame4 = customtkinter.CTkFrame(master=self, border_color="gray", border_width=1, width=690, height=770)
        self.frame4.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.frame4.place(x=1220, y=220)
        self.frame4.browser = WebView2(self,500,500)


# --- Global Variables ---
app = App()
show_help = True
# ------------------------

def toggle_Helps():
    global show_help
    show_help = not show_help





keyboard.on_press_key("f1", toggle_Helps())


if __name__ == "__main__":
    app.mainloop()
