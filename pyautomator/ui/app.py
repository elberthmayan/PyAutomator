from ..shared import *
from .frames import HomeFrame, OrganizerFrame, CleanerFrame, RenamerFrame, ConverterFrame, EnergyFrame

class AutomationHub(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config_file = "nexus_config.json"
        self.config = self.load_config()

        self.title("PyAutomator - System Hub")
        self.geometry("1100x750")
        self.minsize(950, 650)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === SIDEBAR ===
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PY AUTOMATOR", 
                                     font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
                                     text_color=COLOR_TEXT_MAIN)
        self.logo_label.grid(row=0, column=0, padx=25, pady=(40, 10), sticky="w")
        
        self.subtitle_label = ctk.CTkLabel(self.sidebar_frame, text="SUITE V8.5", 
                                         text_color=COLOR_ACCENT,
                                         font=ctk.CTkFont(size=11, weight="bold"))
        self.subtitle_label.grid(row=1, column=0, padx=25, pady=(0, 30), sticky="w")

        # Botões Menu
        self.btn_home = self.create_nav_button("DASHBOARD", self.show_home)
        self.btn_home.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        self.btn_organizer = self.create_nav_button("ORGANIZAR", self.show_organizer)
        self.btn_organizer.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        self.btn_cleaner = self.create_nav_button("LIMPEZA", self.show_cleaner)
        self.btn_cleaner.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        self.btn_renamer = self.create_nav_button("RENOMEAR", self.show_renamer)
        self.btn_renamer.grid(row=5, column=0, padx=15, pady=5, sticky="ew")
        self.btn_converter = self.create_nav_button("CONVERSOR", self.show_converter)
        self.btn_converter.grid(row=6, column=0, padx=15, pady=5, sticky="ew")
        self.btn_energy = self.create_nav_button("ENERGIA", self.show_energy)
        self.btn_energy.grid(row=7, column=0, padx=15, pady=5, sticky="ew")

        # Switch de Tema
        self.theme_switch_var = ctk.StringVar(value="Dark")
        self.theme_switch = ctk.CTkSwitch(self.sidebar_frame, text="Modo Escuro", command=self.toggle_theme, 
                                        variable=self.theme_switch_var, onvalue="Dark", offvalue="Light",
                                        progress_color=COLOR_ACCENT, text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(size=12))
        self.theme_switch.grid(row=11, column=0, padx=25, pady=(0, 20), sticky="w")

        # === CONTEÚDO ===
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomeFrame, OrganizerFrame, CleanerFrame, RenamerFrame, ConverterFrame, EnergyFrame):
            frame = F(self.content_area, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_home()

    def toggle_theme(self):
        mode = self.theme_switch_var.get()
        ctk.set_appearance_mode(mode)
        self.theme_switch.configure(text="Modo Escuro" if mode == "Dark" else "Modo Claro")

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f: return json.load(f)
            except: return {}
        return {}

    def save_setting(self, key, value):
        self.config[key] = value
        try:
            with open(self.config_file, "w") as f: json.dump(self.config, f)
        except: pass

    def get_setting(self, key, default=None):
        return self.config.get(key, default)

    def create_nav_button(self, text, command):
        return ctk.CTkButton(self.sidebar_frame, text=text, fg_color="transparent", 
                           text_color=COLOR_TEXT_DIM, hover_color=COLOR_CARD, anchor="w",
                           height=40, font=ctk.CTkFont(size=12, weight="bold"), command=command)

    def highlight_btn(self, active_btn):
        for btn in [self.btn_home, self.btn_organizer, self.btn_cleaner, self.btn_renamer, self.btn_converter, self.btn_energy]:
            btn.configure(fg_color="transparent", text_color=COLOR_TEXT_DIM)
        active_btn.configure(text_color=COLOR_TEXT_MAIN, fg_color=COLOR_CARD)

    def show_frame(self, frame_class, btn):
        frame = self.frames[frame_class]
        frame.tkraise()
        self.highlight_btn(btn)
        if hasattr(frame, 'on_show'): frame.on_show()

    def show_home(self): self.show_frame(HomeFrame, self.btn_home)
    def show_organizer(self): self.show_frame(OrganizerFrame, self.btn_organizer)
    def show_cleaner(self): self.show_frame(CleanerFrame, self.btn_cleaner)
    def show_renamer(self): self.show_frame(RenamerFrame, self.btn_renamer)
    def show_converter(self): self.show_frame(ConverterFrame, self.btn_converter)
    def show_energy(self): self.show_frame(EnergyFrame, self.btn_energy)

    # Boot Logic
    def check_boot_file(self, suffix):
        sys_os = platform.system()
        if sys_os == "Windows":
            p = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup', f"PyAuto_{suffix}.bat")
            return os.path.exists(p)
        elif sys_os == "Linux":
            p = os.path.expanduser(f"~/.config/autostart/pyauto_{suffix.lower()}.desktop")
            return os.path.exists(p)
        return False

    def toggle_boot(self, state, suffix, flag):
        app_path = os.path.abspath(sys.argv[0])
        sys_os = platform.system()
        try:
            if sys_os == "Windows":
                p = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup', f"PyAuto_{suffix}.bat")
                if state == "on":
                    with open(p, "w") as f: f.write(f'@echo off\nstart "" pythonw "{app_path}" {flag}')
                else:
                    if os.path.exists(p): os.remove(p)
            elif sys_os == "Linux":
                p = os.path.expanduser(f"~/.config/autostart/pyauto_{suffix.lower()}.desktop")
                if state == "on":
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, "w") as f: f.write(f"[Desktop Entry]\nType=Application\nExec=python3 \"{app_path}\" {flag}\nHidden=false\nX-GNOME-Autostart-enabled=true\nName=PyAutomator {suffix}")
                else:
                    if os.path.exists(p): os.remove(p)
            return True
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return False


# === TELA HOME ===
