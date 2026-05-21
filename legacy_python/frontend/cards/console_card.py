import customtkinter as ctk
from backend.config import MAIN_FONT

class ConsoleCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        lbl_data = ctk.CTkLabel(self, text="🖥️ Console", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"))
        lbl_data.grid(row=0, column=0, pady=(20, 5))
        
        self.controller.console_textbox = ctk.CTkTextbox(self, fg_color=("#F5F5F5", "#181D1A"), border_width=1, border_color=("#E5E5E5", "#222"), corner_radius=15, font=ctk.CTkFont(family="Consolas", size=12))
        self.controller.console_textbox.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.controller.console_textbox.insert("end", "System Initialized.\nWaiting for commands...\n")
        self.controller.console_textbox.configure(state="disabled")
