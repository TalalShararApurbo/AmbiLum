import customtkinter as ctk
from backend.config import MAIN_FONT

class CalibrationCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        lbl_calib = ctk.CTkLabel(self, text="📐 Calibration", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"))
        lbl_calib.grid(row=0, column=0, pady=(20, 10))
        
        lbl_tba = ctk.CTkLabel(self, text="TBA", font=ctk.CTkFont(family=MAIN_FONT, size=16, weight="bold"), text_color="#777")
        lbl_tba.grid(row=1, column=0, pady=(40, 40))
