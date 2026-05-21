import customtkinter as ctk
from backend.config import MAIN_FONT

class DevicesCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        lbl_dev = ctk.CTkLabel(self, text="💻 Devices", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"))
        lbl_dev.grid(row=0, column=0, pady=(20, 10))
        
        self.grid_rowconfigure(1, weight=1)
        
        dev_list = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=fg_color, scrollbar_button_hover_color=("#CCC", "#444"))
        dev_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 15))
        dev_list.grid_columnconfigure(0, weight=1)
        self.controller.create_device_row(dev_list, "✨ Twinkle Tray", False, "#9370DB", "twinkle")
        self.controller.create_device_row(dev_list, "💻 OpenRGB", True, "#1E90FF", "openrgb")
        self.controller.create_device_row(dev_list, "🌐 WLED", self.controller.wled_state, "#FFA500", "wled")
        
        btn_add_dev = ctk.CTkButton(self, text="➕ Add Device", corner_radius=12, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                    fg_color="transparent", border_width=1, text_color=("#000", "#FFF"))
        btn_add_dev.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))
