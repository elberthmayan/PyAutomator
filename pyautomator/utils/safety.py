from ..shared import os, time

def is_safe_to_move(filepath):
    if os.path.isdir(filepath): return False
    if os.path.basename(filepath).startswith("log_"): return False
    try:
        size1 = os.path.getsize(filepath)
        time.sleep(1.0)
        size2 = os.path.getsize(filepath)
        if size1 != size2: return False 
    except: return False
    try:
        new = filepath + "_check"
        os.rename(filepath, new); os.rename(new, filepath)
        return True
    except: return False

# =============================================================================
# INTERFACE GRÁFICA PRINCIPAL
# =============================================================================
