@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
title PyAutomator - Instalador Completo
color 0F

set "PYTHON_URL=https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
set "PYTHON_INSTALLER=%TEMP%\python_installer.exe"

set "line======================================================="

cls
echo %line%
echo   PyAutomator - Instalador Completo (Windows)
echo %line%
echo.

:: =========================
:: VERIFICAR PYTHON
:: =========================
echo [INFO] Verificando Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo [AVISO] Python nao encontrado. Baixando...

    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

    if not exist "%PYTHON_INSTALLER%" (
        echo [ERRO] Falha ao baixar Python.
        goto :FIM
    )

    echo [INFO] Instalando Python...
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    echo [INFO] Aguardando instalacao...
    timeout /t 10 >nul
)

echo [OK] Python detectado.
python --version
echo.

:: =========================
:: ATUALIZAR PIP
:: =========================
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip
echo.

:: =========================
:: INSTALAR LIBS
:: =========================
echo [INFO] Instalando bibliotecas...
python -m pip install customtkinter pillow moviepy

echo.
echo %line%
echo   SUCESSO! Tudo instalado.
echo %line%

:FIM
echo.
pause