import customtkinter as ctk
from backend.config import MAIN_FONT

class EnvironmentCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1, uniform="env")
        self.grid_columnconfigure(1, weight=1, uniform="env")
        
        self.lux_card = ctk.CTkFrame(self, corner_radius=corner_radius, border_width=1, fg_color=fg_color, border_color=border_color)
        self.lux_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        lbl_lux_title = ctk.CTkLabel(self.lux_card, text="💡 Ambient Lux", font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"))
        lbl_lux_title.pack(pady=(15, 0))
        self.controller.lbl_lux_val = ctk.CTkLabel(self.lux_card, text="Waiting...", font=ctk.CTkFont(family=MAIN_FONT, size=24, weight="bold"))
        self.controller.lbl_lux_val.pack(pady=(0, 15))
        
        self.time_card = ctk.CTkFrame(self, corner_radius=corner_radius, border_width=1, fg_color=fg_color, border_color=border_color)
        self.time_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        lbl_time_title = ctk.CTkLabel(self.time_card, text="🕒 Local Time", font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"))
        lbl_time_title.pack(pady=(15, 0))
        self.controller.lbl_time_val = ctk.CTkLabel(self.time_card, text="--:--", font=ctk.CTkFont(family=MAIN_FONT, size=24, weight="bold"))
        self.controller.lbl_time_val.pack(pady=(0, 15))
