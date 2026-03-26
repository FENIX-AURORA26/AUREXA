#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_PYINSTALLER="$PROJECT_ROOT/.venv/bin/pyinstaller"
DIST_DIR="$PROJECT_ROOT/dist"
OUT_DIR="$PROJECT_ROOT/installer_output"
APP_NAME="KVP_STUDIO"

if [[ ! -x "$VENV_PYINSTALLER" ]]; then
  echo "PyInstaller nao encontrado em .venv/bin. Rode a instalacao do ambiente primeiro."
  exit 1
fi

echo "Limpando builds antigos..."
rm -rf "$PROJECT_ROOT/build" "$DIST_DIR" "$OUT_DIR"

echo "Gerando binario Linux..."
"$VENV_PYINSTALLER" "$PROJECT_ROOT/app_main.spec"

if [[ ! -f "$DIST_DIR/$APP_NAME" && ! -f "$DIST_DIR/$APP_NAME.exe" ]]; then
  echo "Falha: binario nao encontrado em dist/$APP_NAME"
  exit 1
fi

mkdir -p "$OUT_DIR/linux"

if [[ -f "$DIST_DIR/$APP_NAME" ]]; then
  cp "$DIST_DIR/$APP_NAME" "$OUT_DIR/linux/$APP_NAME"
  chmod +x "$OUT_DIR/linux/$APP_NAME"
else
  cp "$DIST_DIR/$APP_NAME.exe" "$OUT_DIR/linux/$APP_NAME"
  chmod +x "$OUT_DIR/linux/$APP_NAME"
fi

cp "$PROJECT_ROOT/README.md" "$OUT_DIR/linux/README.md"
cp "$PROJECT_ROOT/.env.example" "$OUT_DIR/linux/.env.example"
cp "$PROJECT_ROOT/installer/linux/kvp_studio.desktop" "$OUT_DIR/linux/kvp_studio.desktop"

tar -czf "$OUT_DIR/KVP_STUDIO_linux_portable.tar.gz" -C "$OUT_DIR/linux" .

echo "Pacote Linux gerado em: $OUT_DIR/KVP_STUDIO_linux_portable.tar.gz"
