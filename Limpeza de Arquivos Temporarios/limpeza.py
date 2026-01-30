import os
import shutil
import tempfile
import ctypes
import sys

# --- CONFIGURAÇÕES ---
NOME_APP = "LimpezaArquivosTemporarios"

def adicionar_ao_startup():
    """
    Copia este arquivo automaticamente para a pasta 'Inicializar' do Windows.
    Substitui a necessidade de abrir o 'shell:startup' manualmente.
    """
    # Caminho da pasta Inicializar do Windows (shell:startup)
    pasta_startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    
    # Caminho onde este script DEVERIA estar (com o NOVO NOME solicitado)
    caminho_destino = os.path.join(pasta_startup, "limpeza_arquivos_temporarios.pyw")
    
    # Caminho de onde este script ESTÁ rodando agora
    caminho_atual = os.path.abspath(__file__)

    # 1. Verifica se já está rodando da pasta certa (ou seja, o PC acabou de ligar)
    if caminho_atual.lower() == caminho_destino.lower():
        return # Não faz nada, apenas segue para limpar o PC

    # 2. Verifica se o arquivo já existe lá (para não perguntar toda vez que você clicar no arquivo original)
    if os.path.exists(caminho_destino):
        return 

    # 3. Pergunta se quer instalar (Mover automaticamente)
    resposta = ctypes.windll.user32.MessageBoxW(0, 
        "Deseja instalar o 'limpeza_arquivos_temporarios' para rodar com o Windows?\n\n(Isso copiará o arquivo para sua pasta de Inicialização automaticamente)", 
        "Instalação Automática", 4 | 0x40) # 4=Yes/No, 0x40=InfoIcon
    
    if resposta == 6: # 6 = Yes
        try:
            # Copia o arquivo atual para a pasta de startup com o novo nome
            shutil.copy2(caminho_atual, caminho_destino)
            
            ctypes.windll.user32.MessageBoxW(0, 
                "Instalado com sucesso!\n\nO arquivo 'limpeza_arquivos_temporarios.pyw' foi criado na inicialização.\nAgora você pode apagar este arquivo da pasta Downloads se quiser.", 
                "Sucesso", 0x40)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"Erro ao copiar: {e}", "Erro", 0x10)

def limpar_pasta(pasta):
    if not os.path.exists(pasta):
        return 0
    
    contador = 0
    # PROTEÇÃO NOVA: Tenta listar os arquivos. Se der "Acesso Negado", pula a pasta.
    try:
        itens = os.listdir(pasta)
    except (PermissionError, OSError):
        return 0 # Sem permissão para ler esta pasta, ignora e segue a vida.

    for item in itens:
        caminho_item = os.path.join(pasta, item)
        try:
            if os.path.isfile(caminho_item) or os.path.islink(caminho_item):
                os.unlink(caminho_item)
                contador += 1
            elif os.path.isdir(caminho_item):
                shutil.rmtree(caminho_item)
                contador += 1
        except Exception:
            pass
    return contador

def main():
    # Tenta se auto-copiar para o startup antes de limpar
    adicionar_ao_startup()

    # --- LISTA DE LIMPEZA EXPANDIDA ---
    pastas_alvo = [
        tempfile.gettempdir(), # %TEMP% Usuário
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'), # Temp Sistema
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'), # Prefetch
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SoftwareDistribution', 'Download'), # Updates Antigos
        os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Recent"), # Histórico de Arquivos Recentes
        # --- NAVEGADORES ---
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data"),
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Cache\Cache_Data"),
        os.path.expanduser(r"~\AppData\Local\Opera Software\Opera Stable\Cache\Cache_Data"),
        os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Cache\Cache_Data"),
    ]

    total_removido = 0
    
    # 1. Limpa Pastas
    for pasta in pastas_alvo:
        total_removido += limpar_pasta(pasta)

    # 3. Relatório Final
    if total_removido > 0:
        msg = f"PC Limpo!\n{total_removido} arquivos de lixo removidos."
    else:
        # Se rodar e não tiver nada, não mostra nada (silencioso total) ou msg discreta
        # Vamos manter a msg para você saber que funcionou
        msg = "O computador já está totalmente limpo."
        
    ctypes.windll.user32.MessageBoxW(0, msg, "Faxina Concluída", 0x40)

if __name__ == "__main__":
    main()