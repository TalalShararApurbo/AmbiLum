import customtkinter as ctk
from backend.config import MAIN_FONT

class QuickActionsCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        btn_ping_wled = ctk.CTkButton(self, text="📡\n\nPing WLED", height=90, corner_radius=18, fg_color="#3498DB", hover_color="#2980B9", font=ctk.CTkFont(family=MAIN_FONT, weight="bold", size=15), command=self.controller.ping_wled)
        btn_ping_wled.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        btn_ping_sensor = ctk.CTkButton(self, text="📡\n\nPing Sensor", height=90, corner_radius=18, fg_color="#1ABC9C", hover_color="#16A085", font=ctk.CTkFont(family=MAIN_FONT, weight="bold", size=15), command=self.controller.ping_sensor)
        btn_ping_sensor.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
