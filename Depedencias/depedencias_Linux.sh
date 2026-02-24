#!/usr/bin/env bash
set -e

line="======================================================="
echo "$line"
echo "  PyAutomator - Instalador Completo (Linux)"
echo "$line"
echo

# Detectar gerenciador
install_python() {
  echo "[INFO] Instalando Python..."
  if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-tk
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-pip python3-tkinter
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm python python-pip tk
  else
    echo "[ERRO] Sistema nao suportado."
    exit 1
  fi
}

# Verificar Python
if command -v python3 >/dev/null 2>&1; then
  PY=python3
  echo "[OK] $($PY --version)"
else
  install_python
  PY=python3
fi

echo
echo "[INFO] Atualizando pip..."
$PY -m pip install --upgrade pip

echo
echo "[INFO] Instalando bibliotecas..."
$PY -m pip install customtkinter pillow moviepy

echo
echo "$line"
echo "  SUCESSO! Ambiente pronto."
echo "$line"