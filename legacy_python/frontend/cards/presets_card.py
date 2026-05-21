import customtkinter as ctk
from backend.config import MAIN_FONT

class PresetsCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        lbl_presets = ctk.CTkLabel(self, text="🔖 Saved Presets", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"))
        lbl_presets.grid(row=0, column=0, pady=(20, 10))
        
        self.controller.preset_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", 
                                                     scrollbar_button_color=fg_color, scrollbar_button_hover_color=("#CCC", "#444"))
        self.controller.preset_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.controller.refresh_presets_list()
