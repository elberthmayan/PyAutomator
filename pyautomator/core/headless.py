from ..shared import os, json, platform, ctk, messagebox

def run_headless_organizer():
    target_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    try:
        if os.path.exists("nexus_config.json"):
            with open("nexus_config.json", "r") as f:
                cfg = json.load(f)
                if "last_organizer_path" in cfg and os.path.exists(cfg["last_organizer_path"]):
                    target_dir = cfg["last_organizer_path"]
    except: pass

    if not os.path.exists(target_dir): return

    moved = 0
    ext_map = {
        'Imagens': ['.jpg','.png','.gif','.webp','.jpeg','.svg'], 
        'Documentos': ['.pdf','.docx','.txt','.xlsx','.pptx'], 
        'Apps': ['.exe','.msi','.bat','.iso'], 
        'Compactados': ['.zip','.rar','.7z'], 
        'Midia': ['.mp4','.mp3','.mkv','.wav']
    }
    
    for f in os.listdir(target_dir):
        fp = os.path.join(target_dir, f)
        if not is_safe_to_move(fp): continue
        _, ext = os.path.splitext(f)
        cat = "Outros"
        for k, v in ext_map.items(): 
            if ext.lower() in v: cat = k; break
        d = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m')
        dest = os.path.join(target_dir, cat, d)
        os.makedirs(dest, exist_ok=True)
        try:
            shutil.move(fp, os.path.join(dest, f))
            moved += 1
        except: pass

    if moved > 0:
        root = ctk.CTk()
        root.withdraw() 
        messagebox.showinfo("PyAutomator", f"Organização Automática:\n{moved} arquivos organizados.")
        root.destroy()

def run_headless_cleaner():
    count = 0
    paths = [os.environ.get('TEMP')] if platform.system() == "Windows" else ["/tmp"]
    for p in paths:
        if not p: continue
        for root_dir, _, files in os.walk(p):
            for f in files:
                try: os.remove(os.path.join(root_dir, f)); count += 1
                except: pass
    if count > 0:
        root = ctk.CTk()
        root.withdraw()
        messagebox.showinfo("PyAutomator", f"Limpeza Automática:\n{count} arquivos removidos.")
        root.destroy()

