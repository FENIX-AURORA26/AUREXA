#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname)" != "Darwin" ]]; then
  echo "Este script deve ser executado em macOS para gerar .app/.dmg"
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if [[ ! -x ".venv/bin/pyinstaller" ]]; then
  echo "PyInstaller nao encontrado em .venv/bin"
  echo "Rode: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

rm -rf build dist installer_output/macos

source .venv/bin/activate
pyinstaller --windowed --name KVP_STUDIO_MAC app_main.py

mkdir -p installer_output/macos
cp -r dist/KVP_STUDIO_MAC.app installer_output/macos/

echo "App macOS gerado em installer_output/macos/KVP_STUDIO_MAC.app"
echo "Para DMG use: hdiutil create -volname KVP_STUDIO -srcfolder installer_output/macos/KVP_STUDIO_MAC.app -ov -format UDZO installer_output/macos/KVP_STUDIO_MAC.dmg"
