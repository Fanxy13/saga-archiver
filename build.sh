#!/bin/bash
# ============================================================
#   SAGA ARCHIVER — build the standalone binary
#   Result: dist/saga (Apple Silicon, ffmpeg embedded)
# ============================================================
set -euo pipefail

cd "$(dirname "$0")"

FFMPEG_RELEASE="b6.1.1"
FFMPEG_REPO="eugeneware/ffmpeg-static"

echo "[1/3] Fetching static arm64 binaries..."
mkdir -p vendor
if [ ! -f vendor/ffmpeg ] || [ ! -f vendor/ffprobe ]; then
    for tool in ffmpeg ffprobe; do
        echo "      downloading $tool..."
        curl -fsSL -o "vendor/$tool" \
            "https://github.com/${FFMPEG_REPO}/releases/download/${FFMPEG_RELEASE}/${tool}-darwin-arm64"
        chmod +x "vendor/$tool"
    done
    curl -fsSL -o vendor/darwin-arm64.LICENSE \
        "https://github.com/${FFMPEG_REPO}/releases/download/${FFMPEG_RELEASE}/darwin-arm64.LICENSE"
else
    echo "      already present"
fi

echo "[2/3] Preparing the build environment..."
if [ ! -d .buildenv ]; then
    python3 -m venv .buildenv
fi
./.buildenv/bin/pip install --quiet --upgrade pip pyinstaller

echo "[3/3] Building the binary..."
./.buildenv/bin/pyinstaller --noconfirm --clean saga.spec

echo ""
echo "Done: $(pwd)/dist/saga"
ls -lh dist/saga
