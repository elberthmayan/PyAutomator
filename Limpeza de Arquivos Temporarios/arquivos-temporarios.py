import os
import shutil
import platform
import ctypes
import sys
import time
from pathlib import Path

def is_admin():
    """Verifica se o script está rodando como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def obter_pastas_para_limpar():
    """Retorna uma lista de pastas para limpar baseada no SO"""
    sistema = platform.system()
    pastas = []

    if sistema == "Windows":
        # 1. Pasta Temp do Usuário (%TEMP%)
        temp_user = os.environ.get('TEMP')
        if temp_user:
            pastas.append(temp_user)
        
        # 2. Pasta Temp do Windows (Requer Admin)
        pastas.append(r"C:\Windows\Temp")

        # 3. Pasta Temp Raiz (Legado)
        if os.path.exists(r"C:\Temp"):
            pastas.append(r"C:\Temp")
        
    elif sistema == "Linux":
        pastas.append("/tmp")
        pastas.append(os.path.expanduser("~/.cache"))
        pastas.append("/var/tmp")
    
    return pastas

def limpar_pasta(caminho_pasta):
    """Apaga arquivos e subpastas dentro do caminho especificado"""
    if not os.path.exists(caminho_pasta):
        return 0 

    # Se estiver rodando invisível (pythonw), não adianta dar print,
    # mas mantemos para quando você rodar manualmente.
    print(f"\n🧹 Varrendo: {caminho_pasta}")
    bytes_liberados = 0
    
    try:
        itens = os.listdir(caminho_pasta)
    except PermissionError:
        print(f"   ⛔ Sem permissão para acessar.")
        return 0

    for item in itens:
        caminho_item = os.path.join(caminho_pasta, item)
        
        try:
            tamanho = 0
            if os.path.isfile(caminho_item):
                tamanho = os.path.getsize(caminho_item)
                os.remove(caminho_item)
                print(f"   ✅ Apagado arquivo: {item}")
            
            elif os.path.isdir(caminho_item):
                for root, dirs, files in os.walk(caminho_item):
                    for f in files:
                        fp = os.path.join(root, f)
                        tamanho += os.path.getsize(fp)
                shutil.rmtree(caminho_item)
                print(f"   ✅ Apagada pasta: {item}")
            
            bytes_liberados += tamanho

        except:
            # Em modo silencioso, erros são ignorados para não travar
            pass

    return bytes_liberados

def esvaziar_lixeira():
    if platform.system() == "Windows":
        print("\n🗑️ Tentando esvaziar a Lixeira...")
        try:
            ctypes.windll.shell32.SHELLEmptyRecycleBinW(None, None, 7)
            print("   ✅ Lixeira esvaziada!")
            return True
        except:
            return False
    return False

def configurar_inicializacao():
    """Configura para iniciar junto com o sistema de forma INVISÍVEL"""
    sistema = platform.system()
    caminho_script = os.path.abspath(__file__)
    
    if sistema == "Windows":
        pasta_inicializar = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
        arquivo_bat = os.path.join(pasta_inicializar, "LimpezaPC.bat")
        
        if os.path.exists(arquivo_bat):
            return # Já configurado

        print("\n" + "="*40)
        resposta = input("Deseja que esta limpeza rode AUTOMATICAMENTE ao ligar o PC? (S/N): ").strip().upper()
        if resposta == 'S':
            try:
                with open(arquivo_bat, "w") as bat:
                    # TRUQUE: Usamos 'pythonw' em vez de 'python' para não abrir janela preta!
                    bat.write(f'@echo off\nstart "" pythonw "{caminho_script}"')
                print(f"✅ Configurado! Vai rodar silencioso no próximo boot.")
            except Exception as e:
                print(f"❌ Erro: {e}")

    elif sistema == "Linux":
        # No Linux a lógica é parecida, mas via .desktop
        pasta_autostart = os.path.expanduser("~/.config/autostart")
        arquivo_desktop = os.path.join(pasta_autostart, "limpeza_pc.desktop")
        
        if os.path.exists(arquivo_desktop):
            return 

        print("\n" + "="*40)
        resposta = input("Deseja rodar no boot do Linux? (S/N): ").strip().upper()
        if resposta == 'S':
            try:
                if not os.path.exists(pasta_autostart):
                    os.makedirs(pasta_autostart)
                
                conteudo = f"""[Desktop Entry]
Type=Application
Name=Limpeza PC
Exec=python3 "{caminho_script}"
X-GNOME-Autostart-enabled=true
"""
                with open(arquivo_desktop, "w") as f:
                    f.write(conteudo)
                print(f"✅ Configurado!")
            except Exception as e:
                print(f"❌ Erro: {e}")

def main():
    print("--- 🧹 INICIANDO LIMPEZA DE TEMPORÁRIOS 🧹 ---")
    
    # Se estiver rodando invisível (boot), não verificamos admin nem pedimos input
    # Sabemos que é invisível se não tiver 'console' (simplificação)
    modo_silencioso = False
    
    # Executa a limpeza
    total_bytes = 0
    pastas = obter_pastas_para_limpar()

    for pasta in pastas:
        if pasta:
            total_bytes += limpar_pasta(pasta)

    esvaziar_lixeira()
    
    mb_liberados = total_bytes / (1024 * 1024)
    
    # Só tenta configurar inicialização se estivermos rodando manualmente (com janela)
    # Se o sys.stdin.isatty() for True, tem um humano olhando.
    if sys.stdin and sys.stdin.isatty():
        print("\n" + "="*40)
        print(f"🎉 LIMPEZA CONCLUÍDA!")
        print(f"💾 Espaço recuperado: {mb_liberados:.2f} MB")
        print("="*40)
        configurar_inicializacao()
        time.sleep(5)

if __name__ == "__main__":
    main()
