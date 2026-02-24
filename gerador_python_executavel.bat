@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
title Conversor Python para EXE

:: =========================
:: CORES MODERNAS
:: =========================
color 0F

set "APPNAME=Conversor Python -> EXE"
set "TARGET_DIR=%USERPROFILE%\Downloads\Executaveis Python"

:: =========================
:: FUNÇÃO PRINT BONITA
:: =========================
set "line======================================================="

:: =========================
:: HEADER
:: =========================
cls
echo %line%
echo   %APPNAME%  (V4.0)
echo %line%
echo.

:: =========================
:: 1) PYTHON
:: =========================
echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python não encontrado.
    echo Instale em: https://python.org
    goto :FIM
)

for /f "delims=" %%V in ('python --version 2^>^&1') do set "PYVER=%%V"
echo [OK] %PYVER%
echo.

:: =========================
:: 2) PYINSTALLER
:: =========================
echo [INFO] Verificando PyInstaller...
python -m pip show pyinstaller >nul 2>&1

if errorlevel 1 (
    echo [AVISO] PyInstaller não encontrado. Instalando...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar PyInstaller.
        goto :FIM
    )
    echo [OK] PyInstaller instalado.
) else (
    echo [OK] PyInstaller já está instalado.
)

echo.

:: =========================
:: 3) SELECIONAR ARQUIVO
:: =========================
echo [INFO] Selecione o arquivo .py...

set "ps_cmd=Add-Type -AssemblyName System.Windows.Forms;$f=New-Object System.Windows.Forms.OpenFileDialog;$f.Filter='Arquivos Python (*.py)|*.py';$f.Title='Selecione o Script Python';$f.ShowDialog()|Out-Null;$f.FileName"

set "PYTHON_FILE="
for /f "delims=" %%I in ('powershell -noprofile -command "%ps_cmd%"') do set "PYTHON_FILE=%%I"

if "%PYTHON_FILE%"=="" (
    echo.
    echo [CANCELADO] Nenhum arquivo selecionado.
    goto :FIM
)

echo [OK] Arquivo selecionado:
echo "%PYTHON_FILE%"
echo.

:: =========================
:: 4) DESTINO
:: =========================
if not exist "%TARGET_DIR%" (
    echo [INFO] Criando pasta destino...
    mkdir "%TARGET_DIR%" >nul 2>&1
)

set "TEMP_BUILD_DIR=%TEMP%\py_build_%RANDOM%_%RANDOM%"
mkdir "%TEMP_BUILD_DIR%" >nul 2>&1

:: =========================
:: 5) MENU
:: =========================
:MENU
cls
echo %line%
echo   MODO DE EXECUÇÃO
echo %line%
echo.
echo Arquivo : "%PYTHON_FILE%"
echo Destino : "%TARGET_DIR%"
echo.
echo [1] COM console (aparece terminal)
echo [2] SEM console (apenas janela do app)
echo.
set /p "OPCAO=Escolha (1 ou 2): "

if "%OPCAO%"=="1" (
    set "WINDOW_MODE=--console"
    set "MODE_TEXT=COM console"
) else if "%OPCAO%"=="2" (
    set "WINDOW_MODE=--noconsole"
    set "MODE_TEXT=SEM console"
) else (
    echo.
    echo [AVISO] Digite apenas 1 ou 2.
    timeout /t 2 >nul
    goto :MENU
)

:: =========================
:: 6) CONVERSÃO
:: =========================
cls
echo %line%
echo   CONVERTENDO... AGUARDE
echo %line%
echo.
echo [INFO] Modo: %MODE_TEXT%
echo [INFO] Destino: "%TARGET_DIR%"
echo.

python -m PyInstaller --onefile --clean %WINDOW_MODE% ^
 --distpath "%TARGET_DIR%" ^
 --workpath "%TEMP_BUILD_DIR%" ^
 --specpath "%TEMP_BUILD_DIR%" ^
 "%PYTHON_FILE%"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na conversão.
    echo Verifique erros acima.
    rmdir /s /q "%TEMP_BUILD_DIR%" >nul 2>&1
    goto :FIM
)

:: =========================
:: 7) LIMPEZA
:: =========================
echo.
echo [INFO] Limpando arquivos temporários...
rmdir /s /q "%TEMP_BUILD_DIR%" >nul 2>&1

:: =========================
:: 8) SUCESSO
:: =========================
cls
echo %line%
echo   SUCESSO! EXE GERADO!
echo %line%
echo.
echo Seu executável está em:
echo "%TARGET_DIR%"
echo.

explorer "%TARGET_DIR%"

:FIM
echo.
echo Pressione qualquer tecla para sair...
pause >nul