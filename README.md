# SAGA ARCHIVER

Ein Kommandozeilen-Tool für macOS, das Videos von einer Internet-Archive-Verzeichnisseite
oder von YouTube herunterlädt und sie anschließend in ein PSP-taugliches Format
(480×272, H.264 Baseline) konvertiert.

## Features

- Lädt alle `.mp4`-Dateien aus einem Internet-Archive-Verzeichnis herunter
- Alternativ: Download einzelner YouTube-Videos via `yt-dlp` (wird bei Bedarf automatisch installiert)
- Fortschrittsanzeige für Download und Konvertierung
- Konvertierung nach PSP-Spezifikation: 480×272, H.264 Baseline Level 3.0, AAC 128 kbit/s, faststart
- Überspringt bereits vorhandene Dateien, sodass Abbrüche fortgesetzt werden können

## Download (fertiges Programm)

Unter [Releases](https://github.com/Fanxy13/saga-archiver/releases) gibt es ein
eigenständiges Binary für **macOS auf Apple Silicon**. Python und ffmpeg sind
darin enthalten — es muss nichts installiert werden.

```bash
cd ~/Downloads/saga-archiver-v1.0-macos-arm64
xattr -dr com.apple.quarantine saga
./saga
```

Der `xattr`-Schritt ist einmalig nötig, weil das Binary nicht bei Apple
notarisiert ist; ohne ihn verweigert macOS den Start.

## Voraussetzungen

- macOS
- Python 3
- ffmpeg / ffprobe

Der Launcher prüft beides und installiert Fehlendes bei Bedarf über Homebrew.

## Verwendung

Der einfachste Weg — Doppelklick auf `saga_archiver.command`, oder im Terminal:

```bash
./saga_archiver.command
```

Direkt über Python:

```bash
python3 aot_saga_export_simple.py --url "https://archive.org/download/<item>/<verzeichnis>/"
```

Ohne `--url` fragt das Skript die Adresse interaktiv ab. Bei einer neuen URL wird
nach einem Namen für die Zielordner gefragt; angelegt werden dann `<Name>_1080p`
(Originaldateien) und `<Name>_PSP` (konvertierte Dateien).

## Dateien

| Datei | Zweck |
| --- | --- |
| `aot_saga_export_simple.py` | Hauptskript, wird vom Launcher gestartet |
| `saga_archiver.command` | Launcher für macOS inkl. Abhängigkeitsprüfung |
| `build.sh` | Baut das eigenständige Binary nach `dist/saga` |
| `saga.spec` | PyInstaller-Konfiguration für das Standalone-Binary |

## Selbst bauen

```bash
./build.sh
```

Das Skript lädt statische arm64-Builds von ffmpeg und ffprobe nach `vendor/`,
richtet eine Build-Umgebung ein und erzeugt `dist/saga`. Das eingebettete
ffmpeg stammt von [ffmpeg-static](https://github.com/eugeneware/ffmpeg-static)
und steht wegen libx264 unter GPL v2+.

## Auf die PSP übertragen

1. PSP per USB verbinden
2. Dateien nach `/PSP/COMMON/` oder `/VIDEO/` kopieren
3. Trennen und abspielen

## Hinweis

Das Tool lädt nur, was du ihm an URLs vorgibst. Achte darauf, dass du die Rechte
an den Inhalten besitzt bzw. die Nutzungsbedingungen der jeweiligen Quelle einhältst.

---

Version 1.0 — by Gabriel
