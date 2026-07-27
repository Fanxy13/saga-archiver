#!/bin/bash
# ============================================================
#   SAGA ARCHIVER — Auto-Installer & Launcher für macOS
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

# ── 1. Python3 prüfen ──────────────────────────────────────
echo -e "${YELLOW}[1/3] Prüfe Python3...${NC}"
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}      ✓ $(python3 --version) gefunden${NC}"
else
    echo -e "${RED}      ✗ Python3 nicht gefunden. Installiere via Homebrew...${NC}"
    if ! command -v brew &>/dev/null; then
        echo -e "${YELLOW}      Homebrew wird installiert (einmalig, ~2 Min)...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        [ -f "/opt/homebrew/bin/brew" ] && eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install python3
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}      ✗ Fehlgeschlagen. Bitte manuell: https://www.python.org${NC}"
        read -p "Enter zum Beenden..."; exit 1
    fi
    echo -e "${GREEN}      ✓ Python3 installiert${NC}"
fi

# ── 2. ffmpeg prüfen ──────────────────────────────────────
echo -e "${YELLOW}[2/3] Prüfe ffmpeg...${NC}"
if [ -f "./ffmpeg" ]; then
    echo -e "${GREEN}      ✓ Lokales ffmpeg gefunden${NC}"
elif command -v ffmpeg &>/dev/null; then
    echo -e "${GREEN}      ✓ ffmpeg im System gefunden${NC}"
    ln -sf "$(command -v ffmpeg)" ./ffmpeg 2>/dev/null
    ln -sf "$(command -v ffprobe)" ./ffprobe 2>/dev/null
else
    echo -e "${RED}      ✗ ffmpeg nicht gefunden. Installiere via Homebrew...${NC}"
    if ! command -v brew &>/dev/null; then
        echo -e "${YELLOW}      Homebrew wird installiert...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        [ -f "/opt/homebrew/bin/brew" ] && eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    brew install ffmpeg
    if ! command -v ffmpeg &>/dev/null; then
        echo -e "${RED}      ✗ ffmpeg Installation fehlgeschlagen.${NC}"
        read -p "Enter zum Beenden..."; exit 1
    fi
    ln -sf "$(command -v ffmpeg)" ./ffmpeg 2>/dev/null
    ln -sf "$(command -v ffprobe)" ./ffprobe 2>/dev/null
    echo -e "${GREEN}      ✓ ffmpeg installiert${NC}"
fi

# ── 3. Starten ───────────────────────────────────────────
echo -e "${YELLOW}[3/3] Starte SAGA ARCHIVER...${NC}"
echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
echo ""

python3 aot_saga_export_simple.py "$@"
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}   ✓ Fertig!${NC}"
else
    echo -e "${RED}   ✗ Fehler (Code $EXIT_CODE)${NC}"
fi
echo ""
read -p "Enter zum Schließen..."
