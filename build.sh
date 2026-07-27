#!/bin/bash
# ============================================================
#   SAGA ARCHIVER — Build eines eigenständigen Binaries
#   Ergebnis: dist/saga (Apple Silicon, ffmpeg eingebettet)
# ============================================================
set -euo pipefail

cd "$(dirname "$0")"

FFMPEG_RELEASE="b6.1.1"
FFMPEG_REPO="eugeneware/ffmpeg-static"

echo "[1/3] Statische arm64-Binaries besorgen..."
mkdir -p vendor
if [ ! -f vendor/ffmpeg ] || [ ! -f vendor/ffprobe ]; then
    for tool in ffmpeg ffprobe; do
        echo "      lade $tool..."
        curl -fsSL -o "vendor/$tool" \
            "https://github.com/${FFMPEG_REPO}/releases/download/${FFMPEG_RELEASE}/${tool}-darwin-arm64"
        chmod +x "vendor/$tool"
    done
    curl -fsSL -o vendor/darwin-arm64.LICENSE \
        "https://github.com/${FFMPEG_REPO}/releases/download/${FFMPEG_RELEASE}/darwin-arm64.LICENSE"
else
    echo "      bereits vorhanden"
fi

echo "[2/3] Build-Umgebung vorbereiten..."
if [ ! -d .buildenv ]; then
    python3 -m venv .buildenv
fi
./.buildenv/bin/pip install --quiet --upgrade pip pyinstaller

echo "[3/3] Binary bauen..."
./.buildenv/bin/pyinstaller --noconfirm --clean saga.spec

echo ""
echo "Fertig: $(pwd)/dist/saga"
ls -lh dist/saga
