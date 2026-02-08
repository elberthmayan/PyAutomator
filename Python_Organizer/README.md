🐍 Python Organizer – Automation Hub

Um aplicativo desktop em Python + CustomTkinter para organizar arquivos automaticamente e limpar arquivos temporários do sistema, com interface moderna e suporte a execução automática no Windows.

🚀 Funcionalidades
📂 Organizador de Arquivos

Organiza arquivos por categoria:

Imagens

Documentos

Vídeos

Músicas

Códigos

Executáveis

Compactados

Cria subpastas por data de modificação

Gera relatório automático da organização

Pode ser usado em:

Qualquer pasta

Pasta Downloads automaticamente

🧹 Limpeza de Sistema

Remove:

Arquivos temporários do usuário (%TEMP%)

Cache do Windows (modo administrador)

Prefetch

Cache do Chrome e Edge

Mostra:

Quantidade de arquivos removidos

Espaço em disco recuperado (MB)

⚙️ Automação

Opção para:

Iniciar organizador com o Windows

Iniciar limpador com o Windows

Cria scripts .bat automaticamente na pasta de inicialização

🖥️ Interface

Tema escuro/claro

Sidebar moderna

Log em tempo real

Interface feita com CustomTkinter

📦 Tecnologias Usadas

Python 3

CustomTkinter

Tkinter

Threading

OS / Shutil / Pathlib

📥 Instalação
1️⃣ Clone o repositório
git clone https://github.com/seu-usuario/python-organizer.git

2️⃣ Instale as dependências
pip install customtkinter

3️⃣ Execute
python main.py


(ou o nome do seu arquivo .py)

📝 Estrutura de Organização

Os arquivos são movidos para:

PastaEscolhida/
 ├── Imagens/
 │    └── 2026-02-08/
 ├── Documentos/
 ├── Videos/
 ├── Codigos/
 └── Outros/

🔐 Permissões

Para limpeza avançada (Windows Temp, Prefetch, cache de navegador):

O programa solicita execução como Administrador

📄 Relatório

Após organizar arquivos, é criado automaticamente:

Relatorio_Organizacao_YYYYMMDD_HHMMSS.txt


Com:

Data

Pasta analisada

Arquivos movidos

Erros (se houver)
