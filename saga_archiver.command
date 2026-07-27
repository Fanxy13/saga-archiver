#!/bin/bash
# ============================================================
#   SAGA ARCHIVER — Auto-installer & launcher for macOS
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

cd "$(dirname "$0")"

echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}         SAGA ARCHIVER — Setup & Launcher             ${NC}"
echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
echo ""

# ── 1. Check Python3 ───────────────────────────────────────
echo -e "${YELLOW}[1/3] Checking Python3...${NC}"
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}      ✓ Found $(python3 --version)${NC}"
else
    echo -e "${RED}      ✗ Python3 not found. Installing via Homebrew...${NC}"
    if ! command -v brew &>/dev/null; then
        echo -e "${YELLOW}      Installing Homebrew (one time, ~2 min)...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        [ -f "/opt/homebrew/bin/brew" ] && eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install python3
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}      ✗ Failed. Please install manually: https://www.python.org${NC}"
        read -p "Press Enter to exit..."; exit 1
    fi
    echo -e "${GREEN}      ✓ Python3 installed${NC}"
fi

# ── 2. Check ffmpeg ────────────────────────────────────────
echo -e "${YELLOW}[2/3] Checking ffmpeg...${NC}"
if [ -f "./ffmpeg" ]; then
    echo -e "${GREEN}      ✓ Found local ffmpeg${NC}"
elif command -v ffmpeg &>/dev/null; then
    echo -e "${GREEN}      ✓ Found ffmpeg on the system${NC}"
    ln -sf "$(command -v ffmpeg)" ./ffmpeg 2>/dev/null
    ln -sf "$(command -v ffprobe)" ./ffprobe 2>/dev/null
else
    echo -e "${RED}      ✗ ffmpeg not found. Installing via Homebrew...${NC}"
    if ! command -v brew &>/dev/null; then
        echo -e "${YELLOW}      Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        [ -f "/opt/homebrew/bin/brew" ] && eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install ffmpeg
    if ! command -v ffmpeg &>/dev/null; then
        echo -e "${RED}      ✗ ffmpeg installation failed.${NC}"
        read -p "Press Enter to exit..."; exit 1
    fi
    ln -sf "$(command -v ffmpeg)" ./ffmpeg 2>/dev/null
    ln -sf "$(command -v ffprobe)" ./ffprobe 2>/dev/null
    echo -e "${GREEN}      ✓ ffmpeg installed${NC}"
fi

# ── 3. Launch ──────────────────────────────────────────────
echo -e "${YELLOW}[3/3] Starting SAGA ARCHIVER...${NC}"
echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
echo ""

python3 aot_saga_export_simple.py "$@"
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}   ✓ Done!${NC}"
else
    echo -e "${RED}   ✗ Error (code $EXIT_CODE)${NC}"
fi
echo ""
read -p "Press Enter to close..."
