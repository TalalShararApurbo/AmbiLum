import customtkinter as ctk
import json
import time
from backend.config import *
from backend.utils import get_contrasting_text_color
from backend.mqtt_client import AmbiLumMQTTClient
from backend.wled_client import WLEDClient

from frontend.cards.color_card import ColorCard
from frontend.cards.presets_card import PresetsCard
from frontend.cards.environment_card import EnvironmentCard
from frontend.cards.scenes_card import ScenesCard
from frontend.cards.calibration_card import CalibrationCard
from frontend.cards.devices_card import DevicesCard
from frontend.cards.quick_actions_card import QuickActionsCard
from frontend.cards.console_card import ConsoleCard

class AmbiLumUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AMBILUM - Dashboard")
        self.geometry("1300x850")
        
        self.configure(fg_color=("#F0F2F5", "#0A0A0A"))
        
        self.presets = {}
        self.load_presets()
        
        self.scenes_data = {}
        self.load_scenes()
        
        self.load_app_state()
        
        self.wled = WLEDClient(WLED_IP)
        
        self.active_wheel_listener = None
        self.current_color = "#FFA500"
        self.current_theme = "dark"
        ctk.set_appearance_mode(self.current_theme)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.setup_header()
        
        self.home_frame = None
        self.settings_frame = None
        
        self.build_home_frame()
        self.build_settings_frame()
        
        self.show_home()
        self.update_time()
        self.mqtt_client = AmbiLumMQTTClient(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_LUX, self.on_lux_update)
        self.mqtt_client.start()
        self.wled.toggle_power(self.wled_state)
        
        dev_state = self.app_state.get("devices", {}).get("wled", {})
        boot_color = self.current_color
        if dev_state.get("scene") and dev_state["scene"] != "Scenes..." and dev_state["scene"] in self.scenes_data:
            boot_color = self.scenes_data[dev_state["scene"]]["color"]
        elif dev_state.get("preset") and dev_state["preset"] != "Presets..." and dev_state["preset"] in self.presets:
            boot_color = self.presets[dev_state["preset"]]
        elif dev_state.get("color"):
            boot_color = dev_state["color"]
            
        self.wled.set_color(boot_color)

    def on_lux_update(self, lux_value):
        """Callback for when new lux data arrives via MQTT."""
        self.after(0, self._update_lux_ui, lux_value)

    def _update_lux_ui(self, lux_value):
        if hasattr(self, 'lbl_lux_val'):
            self.lbl_lux_val.configure(text=f"{lux_value:.1f} lx")
        if hasattr(self, 'console_textbox'):
            self.log_to_console(f"Sensor Update: {lux_value:.1f} lx")

    def update_time(self):
        if hasattr(self, 'lbl_time_val'):
            current_time = time.strftime("%I:%M %p")
            self.lbl_time_val.configure(text=current_time)
        self.after(1000, self.update_time)

    def load_presets(self):
        if os.path.exists(PRESETS_FILE):
            try:
                with open(PRESETS_FILE, 'r') as f:
                    self.presets = json.load(f)
            except:
                self.presets = {}
        else:
            self.presets = {"Warm White": "#FFAA55", "Cool Blue": "#55AAFF"}

    def save_presets(self):
        with open(PRESETS_FILE, 'w') as f:
            json.dump(self.presets, f)
            
    def load_scenes(self):
        if os.path.exists(SCENES_FILE):
            try:
                with open(SCENES_FILE, 'r') as f:
                    self.scenes_data = json.load(f)
            except:
                self.scenes_data = {}
        else:
            self.scenes_data = {
                "Study": {"color": "#3498DB"},
                "Gaming": {"color": "#E74C3C"},
                "Movie": {"color": "#9B59B6"},
                "Night": {"color": "#E67E22"}
            }

    def save_scenes(self):
        with open(SCENES_FILE, 'w') as f:
            json.dump(self.scenes_data, f)

    def load_app_state(self):
        if os.path.exists(APP_STATE_FILE):
            try:
                with open(APP_STATE_FILE, 'r') as f:
                    self.app_state = json.load(f)
            except:
                self.app_state = {"scenes": {}, "devices": {}, "wled_state": True}
        else:
            self.app_state = {"scenes": {}, "devices": {}, "wled_state": True}
            
        self.wled_state = self.app_state.get("wled_state", True)

    def save_app_state(self):
        self.app_state["wled_state"] = self.wled_state
        with open(APP_STATE_FILE, 'w') as f:
            json.dump(self.app_state, f, indent=4)

    def setup_header(self):
        self.header_frame = ctk.CTkFrame(self.container, corner_radius=20, fg_color=("#FFFFFF", "#141414"), border_color=("#E5E5E5", "#1E1E1E"), border_width=1)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.header_frame, 
            text="Detected Scene: None", 
            text_color=("#00B36B", "#00FA9A"), 
            font=ctk.CTkFont(family=MAIN_FONT, size=15, weight="bold")
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=30, pady=15)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="AMBILUM", 
            font=ctk.CTkFont(family=MAIN_FONT, size=28, weight="bold"),
            text_color=("#111111", "#EEEEEE")
        )
        self.title_label.grid(row=0, column=1, pady=15)
        
        right_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_frame.grid(row=0, column=2, sticky="e", padx=20)
        
        self.btn_settings = ctk.CTkButton(
            right_frame, text="⚙️", width=40, height=40, 
            font=ctk.CTkFont(size=20), command=self.toggle_view,
            corner_radius=20, fg_color="transparent", hover_color=("#E0E0E0", "#2A2A2A"), text_color=("#000", "#FFF")
        )
        self.btn_settings.pack(side="right", padx=0)
        
        self.btn_theme = ctk.CTkButton(
            right_frame, text="☀️" if self.current_theme=="dark" else "🌙", 
            width=40, height=40, font=ctk.CTkFont(size=20), command=self.toggle_theme,
            corner_radius=20, fg_color="transparent", hover_color=("#E0E0E0", "#2A2A2A"), text_color=("#000", "#FFF")
        )
        self.btn_theme.pack(side="right", padx=10)

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.btn_theme.configure(text="🌙")
        else:
            self.current_theme = "dark"
            self.btn_theme.configure(text="☀️")
        ctk.set_appearance_mode(self.current_theme)
        
    def toggle_view(self):
        if self.home_frame.winfo_ismapped():
            self.show_settings()
        else:
            self.show_home()

    def show_home(self):
        if self.settings_frame:
            self.settings_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)
        self.btn_settings.configure(text="⚙️")

    def show_settings(self):
        if self.home_frame:
            self.home_frame.pack_forget()
        self.settings_frame.pack(fill="both", expand=True)
        self.btn_settings.configure(text="🏠")

    def build_home_frame(self):
        self.home_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1, uniform="cols")
        self.home_frame.grid_columnconfigure(1, weight=1, uniform="cols")
        self.home_frame.grid_columnconfigure(2, weight=1, uniform="cols")
        self.home_frame.grid_rowconfigure(0, weight=1)
        
        col1_fg = ("#E8F0FE", "#121820") 
        col2_fg = ("#F3E8FE", "#181220") 
        col3_fg = ("#E8FCEF", "#122018") 
        
        card_border = ("#D0D0D0", "#222222")
        corner_rad = 25
        
        col1_container = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        col1_container.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        col1_container.grid_columnconfigure(0, weight=1)
        col1_container.grid_rowconfigure(1, weight=1) 
        
        self.color_card = ColorCard(col1_container, self, fg_color=col1_fg, border_color=card_border, corner_radius=corner_rad)
        self.color_card.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.presets_card = PresetsCard(col1_container, self, fg_color=col1_fg, border_color=card_border, corner_radius=corner_rad)
        self.presets_card.grid(row=1, column=0, sticky="nsew")
        
        col2_container = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        col2_container.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=10)
        col2_container.grid_columnconfigure(0, weight=1)
        col2_container.grid_rowconfigure(1, weight=1)
        col2_container.grid_rowconfigure(2, weight=1)
        
        self.env_card = EnvironmentCard(col2_container, self, fg_color=col2_fg, border_color=card_border, corner_radius=corner_rad)
        self.env_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.scene_card = ScenesCard(col2_container, self, fg_color=col2_fg, border_color=card_border, corner_radius=corner_rad)
        self.scene_card.grid(row=1, column=0, sticky="nsew")
        
        self.calib_card = CalibrationCard(col2_container, self, fg_color=col2_fg, border_color=card_border, corner_radius=corner_rad)
        self.calib_card.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
            
        col3_container = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        col3_container.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=10)
        col3_container.grid_columnconfigure(0, weight=1)
        col3_container.grid_rowconfigure(2, weight=1)
        
        self.device_card = DevicesCard(col3_container, self, fg_color=col3_fg, border_color=card_border, corner_radius=corner_rad)
        self.device_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.quick_card = QuickActionsCard(col3_container, self, fg_color=col3_fg, border_color=card_border, corner_radius=corner_rad)
        self.quick_card.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.analytics_card = ConsoleCard(col3_container, self, fg_color=col3_fg, border_color=card_border, corner_radius=corner_rad)
        self.analytics_card.grid(row=2, column=0, sticky="nsew")

    def log_to_console(self, msg):
        self.console_textbox.configure(state="normal")
        ts = time.strftime("%H:%M:%S")
        self.console_textbox.insert("end", f"[{ts}] {msg}\n")
        self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")

    def ping_wled(self):
        self.log_to_console("Pinging WLED at " + WLED_IP + "...")
        import requests
        try:
            resp = requests.get(f"http://{WLED_IP}/json/state", timeout=2)
            if resp.status_code == 200:
                self.log_to_console("WLED Responded: OK (200)")
            else:
                self.log_to_console(f"WLED Responded: HTTP {resp.status_code}")
        except Exception as e:
            self.log_to_console(f"WLED Ping Failed: {e}")

    def ping_sensor(self):
        self.log_to_console("Pinging Sensor MQTT Broker...")
        if self.mqtt_client.is_connected:
            self.log_to_console("MQTT Connected. Waiting for BH1750 data...")
        else:
            self.log_to_console("MQTT Not Connected.")

    def toggle_device_brightness(self, dev_id):
        controls = self.device_controls[dev_id]
        if "bri_slider_frame" not in controls:
            frame = ctk.CTkFrame(controls["row"], fg_color="transparent")
            
            btn_close = ctk.CTkButton(frame, text="✖", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT),
                                      command=lambda d=dev_id: self.close_device_brightness(d))
            btn_close.pack(side="right", padx=(10, 0))
            
            btn_auto = ctk.CTkButton(frame, text="Auto", width=45, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                     command=lambda d=dev_id: self.set_device_auto_brightness(d))
            btn_auto.pack(side="right", padx=(10, 0))
            
            slider = ctk.CTkSlider(frame, button_color=("#555", "#888"), progress_color=("#333", "#CCC"), 
                                   command=lambda v, d=dev_id: self.on_device_brightness_change(d, v))
            slider.set(1.0)
            slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            lbl_pct = ctk.CTkLabel(frame, text="100%", font=ctk.CTkFont(family=MAIN_FONT, weight="bold"))
            lbl_pct.pack(side="left", padx=(0, 10))
            controls["bri_lbl_pct"] = lbl_pct
            
            controls["bri_slider_frame"] = frame
            controls["bri_slider"] = slider
            
        if "scene_opt" in controls: controls["scene_opt"].pack_forget()
        if "preset_opt" in controls: controls["preset_opt"].pack_forget()
        if "wheel_container" in controls: controls["wheel_container"].pack_forget()
        controls["bri_btn"].pack_forget()
        
        controls["bri_slider_frame"].pack(side="right", fill="x", expand=True, padx=(5, 15), pady=12)

    def close_device_brightness(self, dev_id):
        controls = self.device_controls[dev_id]
        controls["bri_slider_frame"].pack_forget()
        
        controls["bri_btn"].pack(side="right", padx=(5, 5), pady=12)
        if "wheel_container" in controls: controls["wheel_container"].pack(side="right", padx=(5, 5), pady=12)
        if "preset_opt" in controls: controls["preset_opt"].pack(side="right", padx=(5, 5), pady=12)
        if "scene_opt" in controls: controls["scene_opt"].pack(side="right", padx=(0, 5), pady=12)
        
    def set_device_auto_brightness(self, dev_id):
        controls = self.device_controls[dev_id]
        controls["bri_slider"].set(0.5)
        self.on_device_brightness_change(dev_id, 0.5)
        self.log_to_console(f"{dev_id} auto brightness enabled (50%)")

    def on_device_brightness_change(self, dev_id, value):
        pct = int(value * 100)
        self.device_controls[dev_id]["bri_btn"].configure(text=f"{pct}% 🔅")
        if "bri_lbl_pct" in self.device_controls[dev_id]:
            self.device_controls[dev_id]["bri_lbl_pct"].configure(text=f"{pct}%")
        bri = int(value * 255)
        if dev_id == "wled" and self.wled_state:
            self.wled.set_brightness(bri)

    def assign_scene_to_device(self, dev_id, scene_name):
        if scene_name in self.scenes_data:
            color = self.scenes_data[scene_name]["color"]
            self.log_to_console(f"Setting {dev_id} to scene {scene_name} ({color})")
            if dev_id == "wled" and self.wled_state:
                self.wled.set_color(color)
            if hasattr(self, 'device_rows') and dev_id in self.device_rows:
                self.device_rows[dev_id]["opt"].set("Presets...")
            
            if "devices" not in self.app_state: self.app_state["devices"] = {}
            if dev_id not in self.app_state["devices"]: self.app_state["devices"][dev_id] = {}
            self.app_state["devices"][dev_id]["scene"] = scene_name
            self.app_state["devices"][dev_id]["preset"] = "Presets..."
            self.save_app_state()

    def set_auto_brightness(self):
        self.slider_bri.set(0.5)
        self.log_to_console("Auto brightness enabled (50%)")
        self.on_brightness_change(0.5)

    def assign_preset_to_device(self, dev_id, preset_name):
        if preset_name in self.presets:
            color = self.presets[preset_name]
            self.log_to_console(f"Setting {dev_id} to preset {preset_name} ({color})")
            if dev_id == "wled" and self.wled_state:
                self.wled.set_color(color)
            if hasattr(self, 'device_rows') and dev_id in self.device_rows:
                if "scene_opt" in self.device_rows[dev_id]:
                    self.device_rows[dev_id]["scene_opt"].set("Scenes...")
            
            if "devices" not in self.app_state: self.app_state["devices"] = {}
            if dev_id not in self.app_state["devices"]: self.app_state["devices"][dev_id] = {}
            self.app_state["devices"][dev_id]["preset"] = preset_name
            self.app_state["devices"][dev_id]["scene"] = "Scenes..."
            self.save_app_state()

    def show_confirm(self, btn_del, btn_confirm, btn_cancel):
        btn_del.pack_forget()
        btn_cancel.pack(side="right", padx=(5, 0))
        btn_confirm.pack(side="right", padx=(5, 0))
        
    def hide_confirm(self, btn_del, btn_confirm, btn_cancel):
        btn_confirm.pack_forget()
        btn_cancel.pack_forget()
        btn_del.pack(side="right")

    def show_add_scene_form(self):
        if not self.new_scene_frame.winfo_ismapped():
            self.new_scene_frame.pack(fill="x", before=self.btn_add_scene)
            self.btn_add_scene.configure(text="❌ Cancel")
        else:
            self.new_scene_frame.pack_forget()
            self.btn_add_scene.configure(text="➕ Add Scene")
            
    def set_new_scene_preset(self, preset_name):
        if preset_name in self.presets:
            self.new_scene_color = self.presets[preset_name]
            text_color = get_contrasting_text_color(self.new_scene_color)
            self.btn_scene_set.configure(fg_color=self.new_scene_color, hover_color=self.new_scene_color, text_color=text_color)
        
    def save_new_scene(self):
        name = self.entry_new_scene.get().strip()
        if name and name not in self.scenes_data:
            mon_bri = self.new_scene_mon_var.get()
            self.scenes_data[name] = {"color": self.new_scene_color, "monitor": mon_bri}
            self.save_scenes()
            self.refresh_scenes_list()
            self.refresh_scene_dropdowns()
            self.entry_new_scene.delete(0, "end")
            self.show_add_scene_form() 
            
    def delete_scene(self, name):
        if name in self.scenes_data:
            del self.scenes_data[name]
            self.save_scenes()
            self.refresh_scenes_list()
            self.refresh_scene_dropdowns()
            
    def refresh_scenes_list(self):
        for widget in self.scene_scroll.winfo_children():
            widget.destroy()
        self.scene_rows.clear()
        for scene in self.scenes_data:
            self.create_scene_row(self.scene_scroll, scene)

    def create_scene_row(self, parent, scene_name):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=8)
        
        color = self.scenes_data[scene_name]["color"]
        
        indicator = ctk.CTkFrame(row, width=20, height=20, corner_radius=10, fg_color=color)
        indicator.pack(side="left", padx=(0, 10))
        
        lbl = ctk.CTkLabel(row, text=scene_name, font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"), width=70, anchor="w")
        lbl.pack(side="left")
        
        action_frame = ctk.CTkFrame(row, fg_color="transparent")
        action_frame.pack(side="right", padx=(5, 0))
        
        btn_del = ctk.CTkButton(action_frame, text="🗑", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
        btn_confirm = ctk.CTkButton(action_frame, text="✔", width=30, fg_color="#00C851", hover_color="#007E33", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
        btn_cancel = ctk.CTkButton(action_frame, text="✖", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
        
        btn_del.configure(command=lambda d=btn_del, c=btn_confirm, x=btn_cancel: self.show_confirm(d, c, x))
        btn_cancel.configure(command=lambda d=btn_del, c=btn_confirm, x=btn_cancel: self.hide_confirm(d, c, x))
        btn_confirm.configure(command=lambda n=scene_name: self.delete_scene(n))
        
        btn_del.pack(side="right")
        
        wheel_container = ctk.CTkFrame(row, fg_color="transparent")
        wheel_container.pack(side="right", padx=(5, 0))
        
        btn_apply = ctk.CTkButton(wheel_container, text="🎨 Wheel", width=65, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
        
        frame_listen = ctk.CTkFrame(wheel_container, fg_color="transparent")
        btn_set = ctk.CTkButton(frame_listen, text="SET", width=40, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                command=self.apply_wheel_listen)
        btn_set.pack(side="left", padx=(0, 5))
        ctk.CTkButton(frame_listen, text="✖", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10,
                      command=self.cancel_wheel_listen).pack(side="left")
                      
        btn_apply.configure(command=lambda s=scene_name, b=btn_apply, f=frame_listen, st=btn_set: self.enter_wheel_listen('scene', s, b, f, st))
        btn_apply.pack(fill="both", expand=True)

        preset_names = list(self.presets.keys()) if self.presets else ["Presets..."]
        init_val = self.app_state.get("scenes", {}).get(scene_name, "Presets...")
        opt_var = ctk.StringVar(value=init_val)
        opt = ctk.CTkOptionMenu(row, values=preset_names, variable=opt_var, 
                                command=lambda v, s=scene_name: self.assign_preset_to_scene(s, v),
                                corner_radius=10, dynamic_resizing=False, width=105, font=ctk.CTkFont(family=MAIN_FONT))
        opt.pack(side="right", padx=(0, 0))
        
        self.scene_rows[scene_name] = {"indicator": indicator, "opt": opt_var, "opt_widget": opt}

    def device_toggle_callback(self, dev_id, state):
        if dev_id == "wled":
            self.wled_state = state
            self.save_app_state()
            self.wled.toggle_power(state)

    def create_device_row(self, parent, name, state, accent_color, dev_id=None):
        if not hasattr(self, 'device_controls'):
            self.device_controls = {}
        row = ctk.CTkFrame(parent, fg_color=("#F5F5F5", "#181D1A"), corner_radius=15, border_width=1, border_color=("#E5E5E5", "#222"))
        row.pack(fill="x", padx=15, pady=6)
        
        lbl = ctk.CTkLabel(row, text=name, font=ctk.CTkFont(family=MAIN_FONT, size=14, weight="bold"))
        lbl.pack(side="left", padx=15, pady=12)
        
        sw = ctk.CTkSwitch(row, text="", progress_color=accent_color, width=40, button_color=("#FFFFFF", "#E0E0E0"), button_hover_color=("#EEEEEE", "#CCCCCC"))
        if state: sw.select()
        if dev_id:
            sw.configure(command=lambda: self.device_toggle_callback(dev_id, sw.get()))
        sw.pack(side="right", padx=15, pady=12)
        
        if dev_id:
            self.device_controls[dev_id] = {"row": row}
            
            bri_btn = ctk.CTkButton(row, text="100% 🔅", width=70, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT),
                                    command=lambda d=dev_id: self.toggle_device_brightness(d))
            bri_btn.pack(side="right", padx=(5, 5), pady=12)
            self.device_controls[dev_id]["bri_btn"] = bri_btn
            
            if dev_id != "twinkle":
                wheel_container = ctk.CTkFrame(row, fg_color="transparent")
                wheel_container.pack(side="right", padx=(5, 5), pady=12)
                
                btn_apply = ctk.CTkButton(wheel_container, text="🎨 Wheel", width=60, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
                
                frame_listen = ctk.CTkFrame(wheel_container, fg_color="transparent")
                btn_set = ctk.CTkButton(frame_listen, text="SET", width=40, corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                        command=self.apply_wheel_listen)
                btn_set.pack(side="left", padx=(0, 5))
                ctk.CTkButton(frame_listen, text="✖", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10,
                              command=self.cancel_wheel_listen).pack(side="left")
                
                btn_apply.configure(command=lambda d=dev_id, b=btn_apply, f=frame_listen, st=btn_set: self.enter_wheel_listen('device', d, b, f, st))
                btn_apply.pack(fill="both", expand=True)
                self.device_controls[dev_id]["wheel_container"] = wheel_container
                
                preset_names = list(self.presets.keys()) if self.presets else ["Presets..."]
                preset_init = self.app_state.get("devices", {}).get(dev_id, {}).get("preset", "Presets...")
                opt_var = ctk.StringVar(value=preset_init)
                opt = ctk.CTkOptionMenu(row, values=preset_names, variable=opt_var, 
                                        command=lambda v, d=dev_id: self.assign_preset_to_device(d, v),
                                        corner_radius=10, dynamic_resizing=False, width=90, font=ctk.CTkFont(family=MAIN_FONT))
                opt.pack(side="right", padx=(5, 5), pady=12)
                self.device_controls[dev_id]["preset_opt"] = opt
                self.device_controls[dev_id]["preset_var"] = opt_var
                
                scene_names = list(self.scenes_data.keys()) if hasattr(self, 'scenes_data') and self.scenes_data else ["Scenes..."]
                scene_init = self.app_state.get("devices", {}).get(dev_id, {}).get("scene", "Scenes...")
                s_opt_var = ctk.StringVar(value=scene_init)
                s_opt = ctk.CTkOptionMenu(row, values=scene_names, variable=s_opt_var,
                                          command=lambda v, d=dev_id: self.assign_scene_to_device(d, v),
                                          corner_radius=10, dynamic_resizing=False, width=90, font=ctk.CTkFont(family=MAIN_FONT))
                s_opt.pack(side="right", padx=(0, 5), pady=12)
                self.device_controls[dev_id]["scene_opt"] = s_opt
                self.device_controls[dev_id]["scene_var"] = s_opt_var
                
                if not hasattr(self, 'device_rows'):
                    self.device_rows = {}
                self.device_rows[dev_id] = {"opt": opt_var, "opt_widget": opt, "scene_opt": s_opt, "bri_btn": bri_btn}

    def on_brightness_change(self, value):
        pct = int(value * 100)
        if hasattr(self, 'lbl_bri_pct'):
            self.lbl_bri_pct.configure(text=f"{pct}%")
        if self.wled_state:
            bri = int(value * 255)
            self.wled.set_brightness(bri)

    def on_hex_enter(self, event):
        color = self.entry_hex.get()
        if len(color) == 7 and color.startswith("#"):
            self.current_color = color
            self.wheel.set_color(color)
            self.update_wheel_listen_color(color)
            if self.wled_state:
                if self.active_wheel_listener and self.active_wheel_listener["type"] == "device" and self.active_wheel_listener["id"] == "wled":
                    self.wled.set_color(color)
        else:
            self.entry_hex.delete(0, "end")
            self.entry_hex.insert(0, self.current_color)

    def on_wheel_change(self, hex_color):
        self.current_color = hex_color
        self.entry_hex.delete(0, "end")
        self.entry_hex.insert(0, hex_color)
        self.entry_hex.configure(fg_color=hex_color, text_color=get_contrasting_text_color(hex_color))
        self.update_wheel_listen_color(hex_color)
        if self.wled_state:
            if self.active_wheel_listener and self.active_wheel_listener["type"] == "device" and self.active_wheel_listener["id"] == "wled":
                self.wled.set_color(hex_color)

    def enter_wheel_listen(self, context_type, identifier, btn_wheel, frame_listen, btn_set):
        if self.active_wheel_listener:
            self.cancel_wheel_listen()
        self.active_wheel_listener = {
            "type": context_type,
            "id": identifier,
            "prev_color": self.current_color,
            "btn_wheel": btn_wheel,
            "frame_listen": frame_listen,
            "btn_set": btn_set
        }
        btn_wheel.pack_forget()
        frame_listen.pack(fill="both", expand=True)
        self.update_wheel_listen_color(self.current_color)

    def apply_wheel_listen(self, _=None):
        if not self.active_wheel_listener: return
        l_type = self.active_wheel_listener["type"]
        l_id = self.active_wheel_listener["id"]
        color = self.current_color
        
        # Hide the buttons before refreshing scenes to avoid crash
        try:
            self.active_wheel_listener["frame_listen"].pack_forget()
            self.active_wheel_listener["btn_wheel"].pack(fill="both", expand=True)
        except Exception:
            pass
            
        self.active_wheel_listener = None
        
        if l_type == 'device':
            self.log_to_console(f"Setting {l_id} to wheel color ({color})")
            if l_id == "wled" and self.wled_state:
                self.wled.set_color(color)
            if hasattr(self, 'device_rows') and l_id in self.device_rows:
                self.device_rows[l_id]["opt"].set("Presets...")
                if "scene_opt" in self.device_rows[l_id]:
                    self.device_rows[l_id]["scene_opt"].set("Scenes...")
            
            if "devices" not in self.app_state: self.app_state["devices"] = {}
            if l_id not in self.app_state["devices"]: self.app_state["devices"][l_id] = {}
            self.app_state["devices"][l_id]["preset"] = "Presets..."
            self.app_state["devices"][l_id]["scene"] = "Scenes..."
            self.app_state["devices"][l_id]["color"] = color
            self.save_app_state()
        elif l_type == 'scene':
            self.scenes_data[l_id]["color"] = color
            self.save_scenes()
            if hasattr(self, 'scene_rows') and l_id in self.scene_rows:
                self.scene_rows[l_id]["indicator"].configure(fg_color=color)
                self.scene_rows[l_id]["opt"].set("Presets...")
            self.update_devices_for_scene(l_id, color)
        elif l_type == 'new_scene':
            self.new_scene_color = color

    def cancel_wheel_listen(self, _=None):
        if not self.active_wheel_listener: return
        l = self.active_wheel_listener
        self.active_wheel_listener = None
        
        self.current_color = l["prev_color"]
        
        # Try updating UI elements; entry_hex and wheel are managed safely
        try:
            self.entry_hex.delete(0, "end")
            self.entry_hex.insert(0, self.current_color)
            self.entry_hex.configure(fg_color=self.current_color, text_color=get_contrasting_text_color(self.current_color))
        except Exception:
            pass
            
        try:
            self.wheel.set_color(self.current_color)
        except Exception:
            pass
            
        if self.wled_state and l["type"] == "device" and l["id"] == "wled":
            self.wled.set_color(self.current_color)
            
        try:
            l["frame_listen"].pack_forget()
            l["btn_wheel"].pack(fill="both", expand=True)
        except Exception:
            pass

    def update_wheel_listen_color(self, hex_color):
        if not self.active_wheel_listener: return
        btn_set = self.active_wheel_listener["btn_set"]
        text_col = get_contrasting_text_color(hex_color)
        btn_set.configure(fg_color=hex_color, hover_color=hex_color, text_color=text_col)



    def save_new_preset(self):
        name = self.entry_preset.get().strip()
        if name and self.current_color:
            self.presets[name] = self.current_color
            self.save_presets()
            self.refresh_presets_list()
            self.refresh_scene_dropdowns()
            self.entry_preset.delete(0, "end")
            
    def delete_preset(self, name):
        if name in self.presets:
            del self.presets[name]
            self.save_presets()
            self.refresh_presets_list()
            self.refresh_scene_dropdowns()

    def refresh_presets_list(self):
        for widget in self.preset_scroll.winfo_children():
            widget.destroy()
            
        for name, color in self.presets.items():
            row = ctk.CTkFrame(self.preset_scroll, fg_color="transparent")
            row.pack(fill="x", pady=4, padx=5)
            
            text_col = get_contrasting_text_color(color)
            btn_preset = ctk.CTkButton(row, text=name, fg_color=color, 
                                hover_color=color, text_color=text_col, font=ctk.CTkFont(family=MAIN_FONT, weight="bold"),
                                corner_radius=12, command=lambda c=color: self.on_wheel_change(c))
            btn_preset.pack(side="left", fill="x", expand=True)
            
            action_frame = ctk.CTkFrame(row, fg_color="transparent")
            action_frame.pack(side="right", padx=(5, 0))
            
            btn_del = ctk.CTkButton(action_frame, text="🗑", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
            btn_confirm = ctk.CTkButton(action_frame, text="✔", width=30, fg_color="#00C851", hover_color="#007E33", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
            btn_cancel = ctk.CTkButton(action_frame, text="✖", width=30, fg_color="#FF4444", hover_color="#CC0000", corner_radius=10, font=ctk.CTkFont(family=MAIN_FONT))
            
            btn_del.configure(command=lambda d=btn_del, c=btn_confirm, x=btn_cancel: self.show_confirm(d, c, x))
            btn_cancel.configure(command=lambda d=btn_del, c=btn_confirm, x=btn_cancel: self.hide_confirm(d, c, x))
            btn_confirm.configure(command=lambda n=name: self.delete_preset(n))
            
            btn_del.pack(side="right")

    def refresh_scene_dropdowns(self):
        preset_names = list(self.presets.keys()) if self.presets else ["Presets..."]
        scene_names = list(self.scenes_data.keys()) if hasattr(self, 'scenes_data') and self.scenes_data else ["Scenes..."]
        
        for scene_name, data in self.scene_rows.items():
            cmd = data["opt_widget"]._command
            data["opt_widget"].configure(command=None)
            data["opt_widget"].configure(values=preset_names)
            data["opt_widget"].configure(command=cmd)
            
        cmd = self.new_scene_opt._command
        self.new_scene_opt.configure(command=None)
        self.new_scene_opt.configure(values=preset_names)
        self.new_scene_opt.configure(command=cmd)
        
        if hasattr(self, 'device_rows'):
            for dev_id, data in self.device_rows.items():
                cmd = data["opt_widget"]._command
                data["opt_widget"].configure(command=None)
                data["opt_widget"].configure(values=preset_names)
                data["opt_widget"].configure(command=cmd)
                
                if "scene_opt" in data:
                    cmd_scene = data["scene_opt"]._command
                    data["scene_opt"].configure(command=None)
                    data["scene_opt"].configure(values=scene_names)
                    data["scene_opt"].configure(command=cmd_scene)

    def assign_preset_to_scene(self, scene_name, preset_name):
        if preset_name in self.presets:
            color = self.presets[preset_name]
            self.scenes_data[scene_name]["color"] = color
            self.save_scenes()
            if hasattr(self, 'scene_rows') and scene_name in self.scene_rows:
                self.scene_rows[scene_name]["indicator"].configure(fg_color=color)
            self.status_label.configure(text=f"Detected Scene: {scene_name}")
            self.update_devices_for_scene(scene_name, color)
            
            if "scenes" not in self.app_state: self.app_state["scenes"] = {}
            self.app_state["scenes"][scene_name] = preset_name
            self.save_app_state()

    def update_devices_for_scene(self, scene_name, color):
        if hasattr(self, 'device_rows'):
            for dev_id, data in self.device_rows.items():
                if "scene_opt" in data and data["scene_opt"].get() == scene_name:
                    self.log_to_console(f"Updating {dev_id} to match scene {scene_name} ({color})")
                    if dev_id == "wled" and self.wled_state:
                        self.wled.set_color(color)

    def assign_wheel_to_scene(self, scene_name):
        color = self.current_color
        self.scenes_data[scene_name]["color"] = color
        self.save_scenes()
        if hasattr(self, 'scene_rows') and scene_name in self.scene_rows:
            self.scene_rows[scene_name]["indicator"].configure(fg_color=color)
            self.scene_rows[scene_name]["opt"].set("Presets...")
        self.status_label.configure(text=f"Detected Scene: {scene_name}")
        
        if "scenes" not in self.app_state: self.app_state["scenes"] = {}
        self.app_state["scenes"][scene_name] = "Presets..."
        self.save_app_state()

    def build_settings_frame(self):
        self.settings_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        
        lbl_title = ctk.CTkLabel(self.settings_frame, text="System Data & Settings", font=ctk.CTkFont(family=MAIN_FONT, size=24, weight="bold"))
        lbl_title.pack(anchor="w", pady=(10, 20), padx=20)
        
        self.table_bg = ctk.CTkFrame(self.settings_frame, corner_radius=25, fg_color=("#FFFFFF", "#151515"), border_width=1, border_color=("#E0E0E0", "#222222"))
        self.table_bg.pack(fill="both", expand=True, padx=20, pady=10)
        
        header_frame = ctk.CTkFrame(self.table_bg, fg_color="transparent", height=40)
        header_frame.pack(fill="x", padx=10, pady=(15, 5))
        
        cols = ["Timestamp", "Lux", "Profile", "Decision Source"]
        weights = [2, 1, 2, 2]
        for i, (col, w) in enumerate(zip(cols, weights)):
            header_frame.grid_columnconfigure(i, weight=w)
            lbl = ctk.CTkLabel(header_frame, text=col.upper(), font=ctk.CTkFont(family=MAIN_FONT, size=12, weight="bold"), text_color=("#777", "#888"), anchor="w")
            lbl.grid(row=0, column=i, sticky="ew", padx=15)
            
        self.table_scroll = ctk.CTkScrollableFrame(self.table_bg, fg_color="transparent", scrollbar_button_color=("#FFFFFF", "#151515"), scrollbar_button_hover_color=("#CCC", "#444"))
        self.table_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        
        for i, w in enumerate(weights):
            self.table_scroll.grid_columnconfigure(i, weight=w)
            
        sample_data = [
            ("2026-05-18 10:00:00 AM", "320 lx", "Study", "Rule Engine"),
            ("2026-05-18 11:30:15 AM", "450 lx", "Daylight Auto", "Rule Engine"),
            ("2026-05-18 02:10:00 PM", "280 lx", "Gaming", "User Override"),
            ("2026-05-18 06:00:00 PM", "150 lx", "Warm Evening", "Rule Engine"),
            ("2026-05-18 09:00:00 PM", "50 lx",  "Night", "Rule Engine"),
        ]
        
        for row_idx, row_data in enumerate(sample_data):
            row_fg = ("#F8F8F8", "#1A1A1A") if row_idx % 2 == 0 else ("#F0F0F0", "#101010")
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color=row_fg, corner_radius=8)
            row_frame.grid(row=row_idx, column=0, columnspan=len(cols), sticky="ew", pady=4)
            
            for i, w in enumerate(weights):
                row_frame.grid_columnconfigure(i, weight=w)

            for col_idx, text in enumerate(row_data):
                color = None
                if col_idx == 3: 
                    color = "#E74C3C" if "User Override" in text else "#2ECC71"
                    
                lbl = ctk.CTkLabel(row_frame, text=text, font=ctk.CTkFont(family=MAIN_FONT, size=14), text_color=color, anchor="w")
                lbl.grid(row=0, column=col_idx, pady=12, sticky="ew", padx=15)
