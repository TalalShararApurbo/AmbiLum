import customtkinter as ctk
from backend.config import MAIN_FONT

class ScenesCard(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color, border_color, corner_radius, **kwargs):
        super().__init__(parent, fg_color=fg_color, border_color=border_color, border_width=1, corner_radius=corner_radius, **kwargs)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        lbl_scene = ctk.CTkLabel(self, text="🎬 Scenes", font=ctk.CTkFont(family=MAIN_FONT, size=20, weight="bold"))
        lbl_scene.grid(row=0, column=0, pady=(20, 10))
        
        self.controller.scene_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                                   scrollbar_button_color=fg_color, scrollbar_button_hover_color=("#CCC", "#444"))
        self.controller.scene_scroll.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.controller.scene_rows = {}
        self.controller.refresh_scenes_list()
            
        bottom_scene_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_scene_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
            
        self.controller.btn_add_scene = ctk.CTkButton(bottom_scene_frame, text="➕ Add Scene", corner_radius=12, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                           fg_color="transparent", border_width=1, text_color=("#000", "#FFF"),
                                           command=self.controller.show_add_scene_form)
        self.controller.btn_add_scene.pack(pady=10, padx=20, fill="x")
        
        self.controller.new_scene_frame = ctk.CTkFrame(bottom_scene_frame, fg_color="transparent")
        
        self.controller.entry_new_scene = ctk.CTkEntry(self.controller.new_scene_frame, placeholder_text="Scene Name...", corner_radius=12, font=ctk.CTkFont(family=MAIN_FONT))
        self.controller.entry_new_scene.pack(fill="x", pady=5, padx=20)
        
        btn_form_frame = ctk.CTkFrame(self.controller.new_scene_frame, fg_color="transparent")
        btn_form_frame.pack(fill="x", pady=5, padx=20)
        
        self.controller.new_scene_color = self.controller.current_color
        
        wheel_container = ctk.CTkFrame(btn_form_frame, fg_color="transparent")
        wheel_container.pack(side="left", expand=True, padx=(0,5))

        self.controller.btn_scene_set = ctk.CTkButton(wheel_container, text="🎨 Wheel", width=65, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT), 
                                           command=lambda: self.controller.enter_wheel_listen('new_scene', None, self.controller.btn_scene_set, self.controller.ns_listen_frame, self.controller.ns_set_btn))
        self.controller.btn_scene_set.pack(fill="both", expand=True)
        
        self.controller.ns_listen_frame = ctk.CTkFrame(wheel_container, fg_color="transparent")
        self.controller.ns_set_btn = ctk.CTkButton(self.controller.ns_listen_frame, text="SET", width=40, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                        command=self.controller.apply_wheel_listen)
        self.controller.ns_set_btn.pack(side="left", padx=(0, 5))
        ctk.CTkButton(self.controller.ns_listen_frame, text="✖", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10,
                      command=self.controller.cancel_wheel_listen).pack(side="left")
        
        preset_names = list(self.controller.presets.keys()) if self.controller.presets else ["Presets..."]
        self.controller.new_scene_opt_var = ctk.StringVar(value="Presets...")
        self.controller.new_scene_opt = ctk.CTkOptionMenu(btn_form_frame, values=preset_names, variable=self.controller.new_scene_opt_var, 
                                corner_radius=10, dynamic_resizing=False, font=ctk.CTkFont(family=MAIN_FONT), command=self.controller.set_new_scene_preset)
        self.controller.new_scene_opt.pack(side="left", expand=True, padx=5)
        

        
        btn_scene_save = ctk.CTkButton(btn_form_frame, text="💾 Save", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT), command=self.controller.save_new_scene)
        btn_scene_save.pack(side="right", expand=True, padx=(5,0))
