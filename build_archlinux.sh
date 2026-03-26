#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="$PROJECT_ROOT/installer_output/archlinux"
APP_NAME="kvp-studio"
VERSION="1.0.0"

mkdir -p "$OUT_DIR"

cat > "$OUT_DIR/PKGBUILD" <<PKG
pkgname=${APP_NAME}
pkgver=${VERSION}
pkgrel=1
pkgdesc="KVP Studio desktop/console launcher"
arch=('x86_64')
url='https://aurexa-api.onrender.com'
license=('custom')
depends=('python' 'python-pip')
source=()
sha256sums=()

package() {
  install -dm755 "$pkgdir/opt/kvp-studio"
  cp -r "$srcdir/../../"* "$pkgdir/opt/kvp-studio/"
  install -dm755 "$pkgdir/usr/bin"
  cat > "$pkgdir/usr/bin/kvp-studio" <<'EOF'
#!/usr/bin/env bash
cd /opt/kvp-studio
python run.py
EOF
  chmod +x "$pkgdir/usr/bin/kvp-studio"
}
PKG

cat > "$OUT_DIR/README_ARCH.md" <<'MD'
# Build Arch Linux (PKGBUILD)

1. Rode `./build_archlinux.sh`
2. Entre em `installer_output/archlinux`
3. Execute:

```bash
makepkg -si
```

Isso instala `kvp-studio` em `/opt/kvp-studio` e cria comando `kvp-studio`.
MD

echo "Arquivos Arch Linux gerados em $OUT_DIR"
