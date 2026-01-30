# 🚀 Windows Automation Suite

Um conjunto de ferramentas inteligentes desenvolvidas em **Python** e
**Batch** para automatizar a manutenção do Windows, organizar ficheiros
e facilitar a criação de executáveis.

------------------------------------------------------------------------

## 🛠️ Funcionalidades

### 🧹 Faxina Automática (`limpeza.py`)

Script para remover ficheiros temporários e lixo do sistema.

**Inclui:** - Limpeza de `%TEMP%`, `C:\Windows\Temp`, `Prefetch` e
ficheiros recentes. - Limpeza de cache dos browsers: Chrome, Edge, Opera
e Brave. - Opção de auto-instalação na inicialização do Windows. -
Execução automática a cada arranque do sistema.

------------------------------------------------------------------------

### 📂 Organizador de Downloads (`organiza_downloads.py`)

Organiza automaticamente os ficheiros da pasta Downloads.

**Recursos:** - Separação por categorias: Imagens, Vídeos, Áudio,
Documentos, Instaladores, Compactados e Código. - Criação automática de
subpastas por data (Ano-Mês). - Sistema anti-conflito de nomes. - Pode
ser convertido para `.pyw` para rodar em segundo plano.

------------------------------------------------------------------------

### ⚡ Conversor Python para EXE (`gerador_python_executavel.bat`)

Ferramenta para gerar executáveis a partir de scripts Python.

**Funções:** - Menu interativo. - Escolha entre modo Terminal ou Janela
Invisível. - Verifica e instala Python e PyInstaller automaticamente. -
Remove ficheiros temporários após a compilação.

------------------------------------------------------------------------

## ⚙️ Requisitos

-   Windows 10 ou 11
-   Python 3.x (o conversor instala se necessário)

------------------------------------------------------------------------

## 🚀 Como Usar

### Limpeza e Organização

1.  Executa os scripts `.py`
2.  Na primeira execução, aceita a opção de iniciar com o Windows

### Criar um Executável

1.  Executa `gerador_python_executavel.bat`
2.  Seleciona o teu script Python
3.  Escolhe o modo de visualização
4.  O `.exe` será criado na pasta Downloads

------------------------------------------------------------------------

## 📁 Estrutura do Projeto

    Projeto de Automatizações/
    ├── Limpeza de Arquivos Temporarios/
    │   └── limpeza.py
    ├── Organizador de Downloads/
    │   └── organiza_downloads.py
    └── gerador_python_executavel.bat

------------------------------------------------------------------------

## ⚠️ Nota de Segurança

Estes scripts são destinados a uso pessoal. Para limpar pastas do
sistema como `C:\Windows\Temp`, executa como Administrador.

------------------------------------------------------------------------

## 📜 Licença

Projeto livre para uso educacional e pessoal.

------------------------------------------------------------------------

**Desenvolvido por Mayan 🚀**
