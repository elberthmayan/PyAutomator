import os
import shutil
import time
import ctypes
import sys
import traceback
from pathlib import Path
from datetime import datetime

# --- CONFIGURAÇÃO ---
NOME_NO_STARTUP = "organizador_downloads_auto.pyw"

def adicionar_ao_startup():
    """
    Gerencia a instalação no Startup.
    Agora pergunta SEMPRE se quer configurar a inicialização,
    para permitir testar se a cópia está funcionando.
    """
    pasta_startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    caminho_destino = os.path.join(pasta_startup, NOME_NO_STARTUP)
    caminho_atual = os.path.abspath(__file__)

    # Se já estiver rodando da pasta de startup, não faz nada (apenas segue o fluxo silencioso)
    if caminho_atual.lower() == caminho_destino.lower():
        return

    # Mensagem direta como solicitado
    titulo = "Configurar Inicialização"
    mensagem = ("Deseja fazer o Organizador iniciar junto com o Windows?\n\n"
                "Clique em SIM para instalar/atualizar.")

    # 4=Yes/No, 0x40=IconInfo, 0x1000=SystemModal (Fica por cima de tudo)
    resposta = ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, 4 | 0x40 | 0x1000)
    
    if resposta == 6: # 6 = Botão Yes/Sim
        try:
            # Força a cópia (sobrescreve se existir)
            shutil.copy2(caminho_atual, caminho_destino)
            ctypes.windll.user32.MessageBoxW(0, 
                f"Funcionou! Instalado com sucesso.\n\nO arquivo foi copiado para:\n{pasta_startup}", 
                "Sucesso", 0x40)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Erro ao copiar: {e}", "Erro", 0x10)
    else:
        # Feedback visual caso escolha Não
        ctypes.windll.user32.MessageBoxW(0, "Ok, não será instalado na inicialização.", "Cancelado", 0x40)

class OrganizadorDownloads:
    def __init__(self):
        self.download_path = Path.home() / "Downloads"
        # Log salvo na própria pasta downloads para fácil acesso
        self.arquivo_log = self.download_path / "log_organizador_debug.txt"
        
        # Mapeamento de extensões
        self.diretorios = {
            'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.heic'],
            'Videos': ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv', '.odt', '.rtf'],
            'Instaladores': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.iso'],
            'Compactados': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Scripts_Codigos': ['.py', '.pyw', '.js', '.html', '.css', '.cpp', '.java', '.json', '.sql', '.php'],
            'Design_3D': ['.psd', '.ai', '.blend', '.obj', '.fbx', '.stl']
        }
        
        # Arquivos para ignorar
        self.ignorar = [
            '.tmp', '.crdownload', '.part', '.ini', 
            'desktop.ini', 
            self.arquivo_log.name, 
            os.path.basename(__file__),
            NOME_NO_STARTUP
        ]

    def registrar_log(self, mensagem):
        """Log simples com tratamento de erro de encoding."""
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open(self.arquivo_log, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {mensagem}\n")
        except:
            pass 

    def obter_pasta_destino(self, arquivo):
        ext = arquivo.suffix.lower()
        pasta_categoria = 'Outros'
        
        for pasta, extensoes in self.diretorios.items():
            if ext in extensoes:
                pasta_categoria = pasta
                break
        
        # Tenta pegar data, se falhar usa data atual
        try:
            timestamp_arquivo = arquivo.stat().st_mtime
            data_arquivo = datetime.fromtimestamp(timestamp_arquivo)
        except:
            data_arquivo = datetime.now()

        subpasta_data = data_arquivo.strftime("%Y-%m")
        return self.download_path / pasta_categoria / subpasta_data

    def mover_arquivo(self, arquivo, destino_pasta):
        # Cria a pasta se não existir
        if not destino_pasta.exists():
            try:
                destino_pasta.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.registrar_log(f"ERRO ao criar pasta {destino_pasta}: {e}")
                return False

        destino_final = destino_pasta / arquivo.name
        
        # Lógica de renomeação para não sobrescrever arquivos diferentes
        contador = 1
        while destino_final.exists():
            # Se for EXATAMENTE o mesmo arquivo (tamanho e nome), deleta o da origem (já está organizado)
            if destino_final.stat().st_size == arquivo.stat().st_size:
                try:
                    arquivo.unlink() # Deleta o duplicado na origem
                    self.registrar_log(f"DUPLICADO REMOVIDO: {arquivo.name}")
                    return True
                except:
                    return False
            
            # Se for diferente, renomeia
            destino_final = destino_pasta / f"{arquivo.stem}_{contador}{arquivo.suffix}"
            contador += 1

        try:
            shutil.move(str(arquivo), str(destino_final))
            self.registrar_log(f"MOVIDO: {arquivo.name} -> {pasta_categoria}/{subpasta_data}") # type: ignore
            return True
        except PermissionError:
            # Arquivo em uso, normal
            return False
        except Exception as e:
            self.registrar_log(f"FALHA ao mover {arquivo.name}: {e}")
            return False

    def limpar_pastas_vazias(self):
        # Varre apenas as categorias conhecidas para evitar apagar coisas erradas
        for categoria in self.diretorios.keys():
            pasta_cat = self.download_path / categoria
            if pasta_cat.exists():
                for subpasta in pasta_cat.iterdir():
                    try:
                        if subpasta.is_dir() and not any(subpasta.iterdir()):
                            subpasta.rmdir()
                    except: pass

    def ciclo_organizacao(self):
        """Um ciclo único de verificação."""
        if not self.download_path.exists(): return

        for item in self.download_path.iterdir():
            if not item.is_file(): continue
            if item.name.startswith('.') or item.name in self.ignorar: continue
            if item.suffix.lower() in ['.tmp', '.crdownload', '.part']: continue # Ignora downloads ativos

            try:
                pasta_destino = self.obter_pasta_destino(item)
                # A função mover agora trata erros internamente
                self.mover_arquivo(item, pasta_destino)
            except Exception as e:
                self.registrar_log(f"Erro crítico no arquivo {item.name}: {e}")

        self.limpar_pastas_vazias()

    def monitorar(self):
        self.registrar_log("--- SERVIÇO INICIADO (V3.0) ---")
        
        while True:
            try:
                self.ciclo_organizacao()
            except Exception as e:
                # Se der erro global, loga e continua vivo
                self.registrar_log(f"CRASH NO CICLO: {traceback.format_exc()}")
            
            time.sleep(10) # Verifica a cada 10 segundos

if __name__ == "__main__":
    # Tenta instalar/atualizar
    adicionar_ao_startup()
    
    # Inicia o serviço
    app = OrganizadorDownloads()
    app.monitorar()
