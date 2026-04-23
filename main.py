import customtkinter as ctk

# Set global appearance and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AmbiLumUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AMBILUM - Dashboard")
        self.geometry("1000x700")
        
        # Enforce pure black background for the main window
        self.configure(fg_color="#000000")

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#0A0A0A", corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        # Brand title
        self.title_label = ctk.CTkLabel(self.header_frame, text="AMBILUM", font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        self.title_label.pack(side="left", padx=20, pady=15)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(self.header_frame, text="System Status: Simulated", text_color="#00FA9A", font=ctk.CTkFont(size=14, weight="bold"))
        self.status_label.pack(side="right", padx=20, pady=15)

        # --- Main Tabview ---
        # The tabview background and frame colors should blend with the black theme
        self.tabview = ctk.CTkTabview(self, 
                                      fg_color="#000000", 
                                      bg_color="#000000", 
                                      segmented_button_fg_color="#121212", 
                                      segmented_button_selected_color="#242424",
                                      segmented_button_selected_hover_color="#333333",
                                      segmented_button_unselected_color="#000000",
                                      segmented_button_unselected_hover_color="#111111",
                                      text_color="#FFFFFF")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_dashboard = self.tabview.add("Dashboard")
        self.tab_dataset = self.tabview.add("Dataset Preview")
        
        # Configure tab backgrounds
        self.tab_dashboard.configure(fg_color="#000000")
        self.tab_dataset.configure(fg_color="#000000")

        self.setup_dashboard_tab()
        self.setup_dataset_tab()

    def setup_dashboard_tab(self):
        # --- Real-time Monitoring Cards ---
        self.monitoring_frame = ctk.CTkFrame(self.tab_dashboard, fg_color="#000000")
        self.monitoring_frame.pack(fill="x", pady=(10, 20))
        self.monitoring_frame.grid_columnconfigure((0, 1, 2), weight=1)

        def create_card(parent, title, value, col):
            # Pure black cards with a very subtle grey border look
            card = ctk.CTkFrame(parent, fg_color="#0F0F0F", border_color="#1F1F1F", border_width=1, corner_radius=12)
            card.grid(row=0, column=col, padx=10, sticky="ew")
            
            lbl_title = ctk.CTkLabel(card, text=title.upper(), font=ctk.CTkFont(size=12, weight="bold"), text_color="#888888")
            lbl_title.pack(pady=(15, 5))
            
            lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFFFFF")
            lbl_val.pack(pady=(0, 20))
            
            return lbl_val

        self.val_lux = create_card(self.monitoring_frame, "Ambient Lux", "320 lx", 0)
        self.val_monitor = create_card(self.monitoring_frame, "Monitor Brightness", "75%", 1)
        self.val_profile = create_card(self.monitoring_frame, "Active Profile", "Coding Focus", 2)

        # --- Layout for Controls and Scenes ---
        self.middle_frame = ctk.CTkFrame(self.tab_dashboard, fg_color="#000000")
        self.middle_frame.pack(fill="both", expand=True)
        self.middle_frame.grid_columnconfigure(0, weight=2)
        self.middle_frame.grid_columnconfigure(1, weight=1)

        # Device Control Section
        self.device_frame = ctk.CTkFrame(self.middle_frame, fg_color="#0F0F0F", border_color="#1F1F1F", border_width=1, corner_radius=12)
        self.device_frame.grid(row=0, column=0, padx=(10, 10), sticky="nsew")

        lbl_dev = ctk.CTkLabel(self.device_frame, text="Device Controls", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_dev.pack(anchor="w", padx=20, pady=(20, 15))

        def create_device_control(parent, name, val, color):
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=12)
            
            lbl = ctk.CTkLabel(row_frame, text=name, width=120, anchor="w", font=ctk.CTkFont(size=14))
            lbl.pack(side="left")
            
            toggle = ctk.CTkSwitch(row_frame, text="", progress_color=color, button_color="#FFFFFF")
            toggle.select()
            toggle.pack(side="left", padx=(0, 20))
            
            slider = ctk.CTkSlider(row_frame, progress_color=color, button_color="#FFFFFF", button_hover_color="#DDDDDD")
            slider.set(val)
            slider.pack(side="left", fill="x", expand=True)
        
        # Give each control a distinct accent color for flair
        create_device_control(self.device_frame, "WLED (WiFi)", 0.8, "#FFA500")    # Orange
        create_device_control(self.device_frame, "OpenRGB (PC)", 0.6, "#1E90FF")   # Blue
        create_device_control(self.device_frame, "Twinkle Tray", 0.75, "#9370DB")  # Purple

        # Scene Selector Section
        self.scene_frame = ctk.CTkFrame(self.middle_frame, fg_color="#0F0F0F", border_color="#1F1F1F", border_width=1, corner_radius=12)
        self.scene_frame.grid(row=0, column=1, padx=(10, 10), sticky="nsew")

        lbl_scene = ctk.CTkLabel(self.scene_frame, text="Scenes", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_scene.pack(anchor="w", padx=20, pady=(20, 15))

        scenes = [("Study", "#3498DB"), ("Gaming", "#E74C3C"), ("Movie", "#9B59B6"), ("Night", "#E67E22")]
        for scene_name, color in scenes:
            btn = ctk.CTkButton(self.scene_frame, 
                                text=scene_name, 
                                height=45, 
                                font=ctk.CTkFont(size=14, weight="bold"), 
                                fg_color="#1A1A1A", 
                                hover_color=color,
                                border_color="#2A2A2A",
                                border_width=1)
            btn.pack(fill="x", padx=20, pady=8)

    def setup_dataset_tab(self):
        lbl_info = ctk.CTkLabel(self.tab_dataset, text="Recent System Decisions (Demo Data)", font=ctk.CTkFont(size=18, weight="bold"), text_color="#FFFFFF")
        lbl_info.pack(anchor="w", pady=(10, 15), padx=10)

        # Table Header
        header_frame = ctk.CTkFrame(self.tab_dataset, fg_color="#151515", height=40, corner_radius=8)
        header_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        cols = ["Timestamp", "Lux", "Profile", "Decision Source"]
        weights = [2, 1, 2, 2]
        for i, (col, w) in enumerate(zip(cols, weights)):
            header_frame.grid_columnconfigure(i, weight=w)
            lbl = ctk.CTkLabel(header_frame, text=col.upper(), font=ctk.CTkFont(size=12, weight="bold"), text_color="#888888")
            lbl.grid(row=0, column=i, pady=10, sticky="w", padx=15)

        # Scrollable rows
        self.table_frame = ctk.CTkScrollableFrame(self.tab_dataset, fg_color="#050505", corner_radius=8)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for i, w in enumerate(weights):
            self.table_frame.grid_columnconfigure(i, weight=w)

        # Hardcoded sample data
        sample_data = [
            ("2026-04-23 10:00:00", "320 lx", "Coding Focus", "Rule Engine"),
            ("2026-04-23 11:30:15", "450 lx", "Daylight Auto", "Rule Engine"),
            ("2026-04-23 14:10:00", "280 lx", "Gaming Mode", "User Override"),
            ("2026-04-23 18:00:00", "150 lx", "Warm Evening", "Rule Engine"),
            ("2026-04-23 21:00:00", "50 lx",  "Night Mode", "Rule Engine"),
            ("2026-04-23 23:45:00", "15 lx",  "Ultra Low", "Rule Engine")
        ]

        for row_idx, row_data in enumerate(sample_data):
            # Row container for background styling on hover or just simple alternating colors
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="#0F0F0F" if row_idx % 2 == 0 else "#080808", corner_radius=0)
            row_frame.grid(row=row_idx, column=0, columnspan=len(cols), sticky="ew", pady=1)
            
            for i, w in enumerate(weights):
                row_frame.grid_columnconfigure(i, weight=w)

            for col_idx, text in enumerate(row_data):
                color = "#FFFFFF"
                if col_idx == 3: # Colorize Decision Source
                    color = "#E74C3C" if "User Override" in text else "#2ECC71"
                    
                lbl = ctk.CTkLabel(row_frame, text=text, font=ctk.CTkFont(size=13), text_color=color)
                lbl.grid(row=0, column=col_idx, pady=12, sticky="w", padx=15)

if __name__ == "__main__":
    app = AmbiLumUI()
    app.mainloop()
