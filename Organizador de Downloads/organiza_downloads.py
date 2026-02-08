import os
import shutil
import time
import sys
import platform
from pathlib import Path

# --- CONFIGURAÇÕES ---
PASTA_DOWNLOADS = str(Path.home() / "Downloads")

# Mapeamento de Extensões para Pastas
EXTENSOES = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Musicas": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Executaveis": [".exe", ".msi", ".bat", ".sh", ".deb", ".AppImage", ".apk"],
    "ISOs": [".iso", ".img"],
    "Codigos": [".py", ".js", ".html", ".css", ".cpp", ".java", ".json", ".sql"],
    "Torrents": [".torrent"]
}

EXTENSOES_TEMP = [".crdownload", ".part", ".tmp", ".download"]

def arquivo_esta_pronto(caminho_arquivo):
    """
    Verifica se o arquivo terminou de ser baixado.
    Lógica:
    1. Não pode ter extensão temporária.
    2. O tamanho do arquivo deve permanecer estável por X segundos.
    """
    nome_arquivo = os.path.basename(caminho_arquivo)
    
    for ext in EXTENSOES_TEMP:
        if nome_arquivo.endswith(ext):
            return False

    try:
        tamanho_inicial = os.path.getsize(caminho_arquivo)
        if tamanho_inicial == 0:
            return False 
            
        time.sleep(2) # O famoso "Delayzein"
        
        tamanho_final = os.path.getsize(caminho_arquivo)
        
        if tamanho_inicial != tamanho_final:
            return False
            
        return True
    except OSError:
        return False 

def configurar_inicializacao():
    """Configura para iniciar junto com o sistema (Modo Invisível/Silencioso)"""
    sistema = platform.system()
    caminho_script = os.path.abspath(__file__)
    
    # Só tenta configurar se tiver alguém olhando (não roda se já estiver invisível)
    if not (sys.stdin and sys.stdin.isatty()):
        return

    if sistema == "Windows":
        pasta_inicializar = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
        arquivo_bat = os.path.join(pasta_inicializar, "OrganizadorDownloads.bat")
        
        if os.path.exists(arquivo_bat):
            return 

        print("\n" + "="*40)
        resposta = input("Deseja que o Organizador inicie com o Windows (Invisível)? (S/N): ").strip().upper()
        if resposta == 'S':
            try:
                with open(arquivo_bat, "w") as bat:
                    # TRUQUE: start "" pythonw ... faz rodar sem janela preta
                    bat.write(f'@echo off\nstart "" pythonw "{caminho_script}"')
                print(f"✅ Configurado! Vai rodar escondido no próximo boot.")
            except Exception as e:
                print(f"❌ Erro: {e}")

    elif sistema == "Linux":
        pasta_autostart = os.path.expanduser("~/.config/autostart")
        arquivo_desktop = os.path.join(pasta_autostart, "organizador_downloads.desktop")
        
        if os.path.exists(arquivo_desktop):
            return

        print("\n" + "="*40)
        resposta = input("Deseja que o Organizador inicie com o Linux? (S/N): ").strip().upper()
        if resposta == 'S':
            try:
                if not os.path.exists(pasta_autostart):
                    os.makedirs(pasta_autostart)
                
                conteudo = f"""[Desktop Entry]
Type=Application
Name=Organizador de Downloads
Exec=python3 "{caminho_script}"
X-GNOME-Autostart-enabled=true
"""
                with open(arquivo_desktop, "w") as f:
                    f.write(conteudo)
                print(f"✅ Configurado para Linux!")
            except Exception as e:
                print(f"❌ Erro: {e}")

def organizar():
    print(f"--- 📂 INICIANDO ORGANIZADOR DE DOWNLOADS 📂 ---")
    print(f"Vigiando a pasta: {PASTA_DOWNLOADS}")
    print("Pressione Ctrl+C para parar (se estiver visível).\n")
    
    configurar_inicializacao()

    while True: # Loop infinito
        try:
            # Lista apenas arquivos (ignora pastas para não mover pastas já organizadas)
            arquivos = [f for f in os.listdir(PASTA_DOWNLOADS) if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))]

            for arquivo in arquivos:
                caminho_origem = os.path.join(PASTA_DOWNLOADS, arquivo)
                nome, extensao = os.path.splitext(arquivo)
                extensao = extensao.lower()

                # Ignora o próprio script
                if "organizador_downloads" in nome:
                    continue

                # Verifica integridade
                if not arquivo_esta_pronto(caminho_origem):
                    continue

                moved = False
                for pasta, exts in EXTENSOES.items():
                    if extensao in exts:
                        pasta_destino = os.path.join(PASTA_DOWNLOADS, pasta)
                        
                        if not os.path.exists(pasta_destino):
                            try:
                                os.makedirs(pasta_destino)
                            except: pass

                        caminho_destino = os.path.join(pasta_destino, arquivo)

                        # Renomeia se já existir (arquivo_1.jpg)
                        contador = 1
                        while os.path.exists(caminho_destino):
                            novo_nome = f"{nome}_{contador}{extensao}"
                            caminho_destino = os.path.join(pasta_destino, novo_nome)
                            contador += 1

                        try:
                            shutil.move(caminho_origem, caminho_destino)
                            # Print só aparece se rodar manualmente
                            if sys.stdout: print(f"✅ Movido: {arquivo} -> {pasta}")
                            moved = True
                        except: pass
                        
                        break 
                
                # Move para "Outros" se não tiver categoria
                if not moved and arquivo_esta_pronto(caminho_origem):
                    pasta_destino = os.path.join(PASTA_DOWNLOADS, "Outros")
                    if not os.path.exists(pasta_destino):
                        try: os.makedirs(pasta_destino)
                        except: pass
                    
                    caminho_destino = os.path.join(pasta_destino, arquivo)
                    try:
                        shutil.move(caminho_origem, caminho_destino)
                        if sys.stdout: print(f"📦 Movido para Outros: {arquivo}")
                    except: pass

        except Exception as e:
            # Em modo silencioso, ignoramos erros para não crashar
            pass

        time.sleep(5) 

if __name__ == "__main__":
    try:
        organizar()
    except KeyboardInterrupt:
        pass
