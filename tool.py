import customtkinter
import serial
from PIL import Image
from tkinter import messagebox
import os

class Tool:
    def __init__(self, _port, _baudrate):
        self.port = _port
        self.baudrate = _baudrate
        self.ser = None
        self.root = None
        self.menu_bar_frame = None
        self.toggle_menu_button = None
        self.main_frame = None

    def run(self):
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        except serial.SerialException as e:
            messagebox.showerror("Serial Port Error", f"Could not open port {self.port}: {e}")
            return
        
        # Load icons with error handling
        try:
            toggle_icon = self.load_image("images/toggle.png", (20, 20))
            toggle_home = self.load_image("images/home.png", (18, 18))
            toggle_monitor = self.load_image("images/monitor.png", (18, 18))
            toggle_service = self.load_image("images/service.png", (18, 18))
            toggle_settings = self.load_image("images/setting.png", (18, 18))
        except Exception as e:
            messagebox.showerror("Image Loading Error", f"Could not load one or more images: {e}")
            return

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.root = customtkinter.CTk()
        self.root.title("Tool")
        self.root.geometry("480x280")

        self.menu_bar_frame = customtkinter.CTkFrame(self.root, fg_color="#102A3D")
        self.menu_bar_frame.pack(side="left", fill="y")
        self.menu_bar_frame.configure(width=40)
        self.menu_bar_frame.pack_propagate(flag=False)

        self.toggle_menu_button = customtkinter.CTkButton(
            self.menu_bar_frame, image=toggle_icon, command=self.toggle_menu, anchor="center", text="", width=40, fg_color="#102A3D"
        )
        self.toggle_menu_button.place(x=0, y=5)

        self.create_toggle_button("home", toggle_home, 120)
        self.create_toggle_button("monitor", toggle_monitor, 160)
        self.create_toggle_button("service", toggle_service, 200)
        self.create_toggle_button("settings", toggle_settings, 240)

        self.main_frame = customtkinter.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.page_home()

        self.root.mainloop()

    def load_image(self, path, size):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image file not found: {path}")
        image = Image.open(path)
        return customtkinter.CTkImage(dark_image=image, size=size)

    def create_toggle_button(self, name, icon, y_pos):
        button = customtkinter.CTkButton(
            self.menu_bar_frame, image=icon, anchor="center", text="", width=40, fg_color="#102A3D",
            command=lambda: self.handle_indicator_label(name)
        )
        button.place(x=1, y=y_pos)
        if name == "home":
            indicator = customtkinter.CTkLabel(self.menu_bar_frame, fg_color="white", width=3, height=28, text="")
        else:
            indicator = customtkinter.CTkLabel(self.menu_bar_frame, fg_color="#102A3D", width=3, height=28, text="")
        indicator.place(x=1, y=y_pos)
        setattr(self, f"{name}_button", button)
        setattr(self, f"{name}_button_indicator", indicator)

    def handle_indicator_label(self, name):
        for child in self.menu_bar_frame.winfo_children():
            if isinstance(child, customtkinter.CTkLabel):
                child['fg_color'] = 'SystemButtonFace'  
        indicator = getattr(self, f"{name}_button_indicator")
        indicator['fg_color'] = 'white'
        
        page = getattr(self, f"page_{name}")
        page()

    def toggle_menu(self):
        new_width = 200 if self.menu_bar_frame.winfo_width() == 40 else 40
        self.menu_bar_frame.configure(width=new_width)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def page_home(self):
        self.clear_main_frame()
        label = customtkinter.CTkLabel(self.main_frame, text="Home Page", font=("Arial", 24))
        label.pack(pady=20)

    def page_monitor(self):
        self.clear_main_frame()
        label = customtkinter.CTkLabel(self.main_frame, text="Monitor Page", font=("Arial", 24))
        label.pack(pady=20)

    def page_service(self):
        self.clear_main_frame()
        label = customtkinter.CTkLabel(self.main_frame, text="Service Page", font=("Arial", 24))
        label.pack(pady=20)

    def page_settings(self):
        self.clear_main_frame()
        label = customtkinter.CTkLabel(self.main_frame, text="Settings Page", font=("Arial", 24))
        label.pack(pady=20)


if __name__ == "__main__":
    tool = Tool("COM13", 115200)
    tool.run()
