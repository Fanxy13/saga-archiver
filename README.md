# SAGA ARCHIVER

A command-line tool for macOS that downloads videos from an Internet Archive
directory page or from YouTube and converts them to a PSP-compatible format
(480×272, H.264 Baseline).

## Features

- Downloads every `.mp4` file from an Internet Archive directory
- Alternatively, downloads a single YouTube video via `yt-dlp` (installed automatically when needed)
- Progress display for both downloading and converting
- Converts to PSP specification: 480×272, H.264 Baseline Level 3.0, AAC 128 kbit/s, faststart
- Skips files that already exist, so interrupted runs can be resumed

## Download (ready-to-run build)

The [Releases](https://github.com/Fanxy13/saga-archiver/releases) page has a
standalone binary for **macOS on Apple Silicon**. Python and ffmpeg are included
— nothing needs to be installed.

```bash
cd ~/Downloads/saga-archiver-v1.0-macos-arm64
xattr -dr com.apple.quarantine saga
./saga
```

The `xattr` step is needed once because the binary is not notarized by Apple;
without it macOS refuses to start the program.

## Requirements (running from source)

- macOS
- Python 3
- ffmpeg / ffprobe

The launcher checks for both and installs whatever is missing via Homebrew.

## Usage

The simplest way — double-click `saga_archiver.command`, or in a terminal:

```bash
./saga_archiver.command
```

Directly via Python:

```bash
python3 aot_saga_export_simple.py --url "https://archive.org/download/<item>/<directory>/"
```

Without `--url` the script asks for the address interactively. For a new URL it
also asks for a name for the target folders, then creates `<name>_1080p` (the
original files) and `<name>_PSP` (the converted files).

## Files

| File | Purpose |
| --- | --- |
| `aot_saga_export_simple.py` | Main script, started by the launcher |
| `saga_archiver.command` | macOS launcher including the dependency check |
| `build.sh` | Builds the standalone binary into `dist/saga` |
| `saga.spec` | PyInstaller configuration for the standalone binary |

## Building it yourself

```bash
./build.sh
```

The script downloads static arm64 builds of ffmpeg and ffprobe into `vendor/`,
sets up a build environment and produces `dist/saga`. The embedded ffmpeg comes
from [ffmpeg-static](https://github.com/eugeneware/ffmpeg-static) and is GPL v2+
because of libx264.

## Copying to your PSP

1. Connect the PSP over USB
2. Copy the files to `/PSP/COMMON/` or `/VIDEO/`
3. Disconnect and play

## Note

The tool only downloads what you point it at. Make sure you hold the rights to
the content, or that you are complying with the terms of the source you use.

---

Version 1.0 — by Gabriel
