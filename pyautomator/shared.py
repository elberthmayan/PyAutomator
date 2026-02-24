import os
import shutil
import datetime
import platform
import sys
import threading
import time
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- Dependências Opcionais ---
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from moviepy.editor import VideoFileClip, AudioFileClip
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False

# --- Configurações Iniciais ---
ctk.set_appearance_mode("Dark")  # Padrão inicial
ctk.set_default_color_theme("blue")

# === PALETA DE CORES INTELIGENTE (Light, Dark) ===
COLOR_BG = ("#F3F4F6", "#121212")           
COLOR_SIDEBAR = ("#FFFFFF", "#0A0A0A")      
COLOR_CARD = ("#FFFFFF", "#1E1E1E")         
COLOR_CARD_BORDER = ("#E5E7EB", "#2A2A2A")  

COLOR_INPUT_BG = ("#F9FAFB", "#181818")     
COLOR_INPUT_BORDER = ("#D1D5DB", "#333333")

COLOR_TEXT_MAIN = ("#111827", "#E0E0E0")
COLOR_TEXT_DIM = ("#6B7280", "#9CA3AF")

COLOR_ACCENT = ("#2563EB", "#2962FF")       
COLOR_ACCENT_HOVER = ("#1D4ED8", "#0039CB")
COLOR_SUCCESS = ("#059669", "#00C853")
COLOR_ERROR = ("#DC2626", "#CF6679")

# =============================================================================
# LÓGICA DE EXECUÇÃO EM BACKGROUND
# =============================================================================
