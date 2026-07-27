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
| `aot_saga_export.py` | Variante mit Attack-on-Titan-Voreinstellung |
| `aot_saga_export_backup.py` | Ältere Sicherungskopie |
| `saga_archiver.command` | Launcher für macOS inkl. Abhängigkeitsprüfung |
| `saga.spec` | PyInstaller-Konfiguration für ein Standalone-Binary |

## Auf die PSP übertragen

1. PSP per USB verbinden
2. Dateien nach `/PSP/COMMON/` oder `/VIDEO/` kopieren
3. Trennen und abspielen

## Hinweis

Das Tool lädt nur, was du ihm an URLs vorgibst. Achte darauf, dass du die Rechte
an den Inhalten besitzt bzw. die Nutzungsbedingungen der jeweiligen Quelle einhältst.

---

Version 1.0 — by Gabriel
