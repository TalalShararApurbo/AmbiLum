import customtkinter as ctk
from backend.config import MAIN_FONT
from frontend.ui_components import ColorWheel

class ColorCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        lbl_color = ctk.CTkLabel(self, text="🎨 Color Wheel", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"))
        lbl_color.grid(row=0, column=0, pady=(20, 10))
        
        self.controller.wheel = ColorWheel(self, size=220, command=self.controller.on_wheel_change)
        self.controller.wheel.grid(row=1, column=0, pady=10)
        
        self.controller.entry_hex = ctk.CTkEntry(self, height=45, font=ctk.CTkFont(family=MAIN_FONT, size=16, weight="bold"), 
                                      fg_color=self.controller.current_color, border_width=0, justify="center", corner_radius=20, text_color="black")
        self.controller.entry_hex.insert(0, self.controller.current_color)
        self.controller.entry_hex.grid(row=2, column=0, sticky="ew", padx=40, pady=10)
        self.controller.entry_hex.bind("<Return>", self.controller.on_hex_enter)
        
        bri_header = ctk.CTkFrame(self, fg_color="transparent")
        bri_header.grid(row=3, column=0, sticky="ew", padx=40, pady=(10, 0))
        lbl_bri = ctk.CTkLabel(bri_header, text="Brightness", font=ctk.CTkFont(family=MAIN_FONT))
        lbl_bri.pack(side="left")
        self.controller.lbl_bri_pct = ctk.CTkLabel(bri_header, text="100%", font=ctk.CTkFont(family=MAIN_FONT, weight="bold"))
        self.controller.lbl_bri_pct.pack(side="right")
        
        bri_frame = ctk.CTkFrame(self, fg_color="transparent")
        bri_frame.grid(row=4, column=0, sticky="ew", padx=40, pady=(0, 10))
        
        self.controller.slider_bri = ctk.CTkSlider(bri_frame, button_color=("#555", "#888"), progress_color=("#333", "#CCC"), command=self.controller.on_brightness_change)
        self.controller.slider_bri.set(1.0)
        self.controller.slider_bri.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.controller.btn_auto_bri = ctk.CTkButton(bri_frame, text="Auto", width=50, corner_radius=12, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                          command=self.controller.set_auto_brightness)
        self.controller.btn_auto_bri.pack(side="right")
        
        preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        preset_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=20)
        self.controller.entry_preset = ctk.CTkEntry(preset_frame, placeholder_text="Preset Name...", corner_radius=12, font=ctk.CTkFont(family=MAIN_FONT))
        self.controller.entry_preset.pack(side="left", fill="x", expand=True, padx=(0,10))
        btn_save = ctk.CTkButton(preset_frame, text="💾 Save", width=70, corner_radius=12, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"), command=self.controller.save_new_preset)
        btn_save.pack(side="right")
