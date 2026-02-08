import os
import shutil
import platform
import ctypes
import sys
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
        # Geralmente em: C:\Users\SeuNome\AppData\Local\Temp
        temp_user = os.environ.get('TEMP')
        if temp_user:
            pastas.append(temp_user)
        
        # 2. Pasta Temp do Windows (A "só Temp")
        # Geralmente em: C:\Windows\Temp (Requer Admin)
        pastas.append(r"C:\Windows\Temp")

        # 3. Pasta Temp Raiz (Legado)
        # Alguns programas criam C:\Temp, se existir, limpamos.
        if os.path.exists(r"C:\Temp"):
            pastas.append(r"C:\Temp")
        
        # NOTA: Removemos a pasta 'Prefetch' da limpeza para não deixar
        # o computador lento durante a inicialização/boot.
        
    elif sistema == "Linux":
        pastas.append("/tmp")
        pastas.append(os.path.expanduser("~/.cache"))
        pastas.append("/var/tmp")
    
    return pastas

def limpar_pasta(caminho_pasta):
    """Apaga arquivos e subpastas dentro do caminho especificado"""
    if not os.path.exists(caminho_pasta):
        return 0 # Pasta não existe

    print(f"\n🧹 Varrendo: {caminho_pasta}")
    bytes_liberados = 0
    
    try:
        itens = os.listdir(caminho_pasta)
    except PermissionError:
        print(f"   ⛔ Sem permissão para acessar (Tente rodar como Administrador)")
        return 0

    for item in itens:
        caminho_item = os.path.join(caminho_pasta, item)
        
        try:
            # Tenta pegar o tamanho antes de apagar para calcular o ganho
            tamanho = 0
            if os.path.isfile(caminho_item):
                tamanho = os.path.getsize(caminho_item)
                os.remove(caminho_item)
                print(f"   ✅ Apagado arquivo: {item}")
            
            elif os.path.isdir(caminho_item):
                # Calcula tamanho da pasta (aproximado)
                for root, dirs, files in os.walk(caminho_item):
                    for f in files:
                        fp = os.path.join(root, f)
                        tamanho += os.path.getsize(fp)
                
                shutil.rmtree(caminho_item)
                print(f"   ✅ Apagada pasta: {item}")
            
            bytes_liberados += tamanho

        except PermissionError:
            print(f"   🔒 Acesso negado: {item}")
        except OSError:
            print(f"   ⚙️ Arquivo em uso (pulinho): {item}")
        except Exception as e:
            print(f"   ❌ Erro genérico: {e}")

    return bytes_liberados

def esvaziar_lixeira():
    """Esvazia a lixeira no Windows"""
    if platform.system() == "Windows":
        print("\n🗑️ Tentando esvaziar a Lixeira...")
        try:
            # Flags: SHERB_NOCONFIRMATION (não pede sim/não), SHERB_NOPROGRESSUI, SHERB_NOSOUND
            ctypes.windll.shell32.SHELLEmptyRecycleBinW(None, None, 7)
            print("   ✅ Lixeira esvaziada!")
            return True
        except Exception as e:
            print(f"   ⚠️ Não foi possível esvaziar a lixeira (pode estar vazia ou sem permissão).")
            return False
    return False

def configurar_inicializacao():
    """Configura para iniciar junto com o sistema"""
    sistema = platform.system()
    caminho_script = os.path.abspath(__file__)
    
    if sistema == "Windows":
        pasta_inicializar = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
        arquivo_bat = os.path.join(pasta_inicializar, "LimpezaPC.bat")
        
        if os.path.exists(arquivo_bat):
            return

        print("\n" + "="*40)
        resposta = input("Deseja que esta limpeza rode AUTOMATICAMENTE ao ligar o PC? (S/N): ").strip().upper()
        if resposta == 'S':
            try:
                with open(arquivo_bat, "w") as bat:
                    # Roda minimizado ou rápido
                    bat.write(f'@echo off\npython "{caminho_script}"')
                print(f"✅ Configurado para iniciar com o Windows!")
            except Exception as e:
                print(f"❌ Erro ao configurar: {e}")

    elif sistema == "Linux":
        pasta_autostart = os.path.expanduser("~/.config/autostart")
        arquivo_desktop = os.path.join(pasta_autostart, "limpeza_pc.desktop")
        
        if os.path.exists(arquivo_desktop):
            return 

        print("\n" + "="*40)
        resposta = input("Deseja que esta limpeza rode AUTOMATICAMENTE ao ligar o Linux? (S/N): ").strip().upper()
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
                print(f"✅ Configurado para iniciar com o Linux!")
            except Exception as e:
                print(f"❌ Erro: {e}")

def main():
    print("--- 🧹 INICIANDO LIMPEZA DE TEMPORÁRIOS 🧹 ---")
    
    if platform.system() == "Windows" and not is_admin():
        print("⚠️ AVISO: Você não está rodando como Administrador.")
        print("A pasta Temp do Sistema (C:\\Windows\\Temp) não será limpa totalmente.")
        print("Para limpeza completa, rode o terminal como Administrador.\n")

    total_bytes = 0
    pastas = obter_pastas_para_limpar()

    for pasta in pastas:
        if pasta: # Verifica se o caminho não é None
            total_bytes += limpar_pasta(pasta)

    esvaziar_lixeira()
    
    # Converte bytes para MB
    mb_liberados = total_bytes / (1024 * 1024)
    
    print("\n" + "="*40)
    print(f"🎉 LIMPEZA CONCLUÍDA!")
    print(f"💾 Espaço recuperado: {mb_liberados:.2f} MB")
    print("="*40)

    configurar_inicializacao()
    
    # Pequena pausa para o usuário ver o resultado se não for automático
    import time
    time.sleep(5)

if __name__ == "__main__":
    main()
