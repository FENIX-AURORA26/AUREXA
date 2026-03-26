#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker nao encontrado. Para Android use ambiente com Docker ou SDK Android local."
  exit 1
fi

mkdir -p installer_output/android

cat > installer_output/android/README_ANDROID_BUILD.txt <<'TXT'
Build Android (recomendado com Buildozer/Kivy ou BeeWare Briefcase):

Opcao 1 - Buildozer (Linux):
  pip install buildozer cython
  buildozer init
  buildozer -v android debug

Opcao 2 - Briefcase:
  pip install briefcase
  briefcase create android
  briefcase build android
  briefcase package android

Este repositorio usa PyQt5 no desktop. Para Android, recomenda-se criar front-end mobile separado em Kivy/Flutter/React Native consumindo a mesma API.
TXT

echo "Guia Android gerado em installer_output/android/README_ANDROID_BUILD.txt"
