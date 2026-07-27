#!/usr/bin/env python3
"""
SAGA EXPORT - PSP Edition
=============================
SAGA ARCHIVER / PSP Video Converter
"""

import argparse
import os
import re
import shutil
import sys
import urllib.request
import ssl
import time
from urllib.parse import urljoin
import subprocess


def app_dir():
    """Directory the output folders are created next to."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def find_tool(name):
    """Prefer a bundled binary, fall back to the PATH."""
    for base in (getattr(sys, "_MEIPASS", None), app_dir()):
        if base:
            candidate = os.path.join(base, name)
            if os.path.exists(candidate):
                return candidate
    return shutil.which(name) or name


FFMPEG = find_tool("ffmpeg")
FFPROBE = find_tool("ffprobe")


def format_bytes(size):
    """Return human-readable file size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:3.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}PB"


def get_video_duration(path):
    """Return video duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return None

# ========================== CONFIG ==========================
DIR_URL = "https://archive.org/download/shingeki-no-kyojin_aot/season-1_DUB-1080p/"

DOWNLOAD_FOLDER = "AOT_Season1_1080p"
PSP_FOLDER      = "AOT_Season1_PSP"

# PSP Video Settings
PSP_WIDTH   = 480
PSP_HEIGHT  = 272
CRF_QUALITY = 23
PRESET      = "medium"
MAXRATE     = "1500k"
# ===========================================================

def print_epic_banner():
    banner = r"""
   ███████╗ █████╗  ██████╗  █████╗      █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗██████╗ 
   ██╔════╝██╔══██╗██╔════╝ ██╔══██╗    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝██╔══██╗
   ███████╗███████║██║  ███╗███████║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗  ██████╔╝
   ╚════██║██╔══██║██║   ██║██╔══██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
   ███████║██║  ██║╚██████╔╝██║  ██║    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗██║  ██║
   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
"""
    print(banner)
    print("BY GABRIEL VERSION 1.0\n")


def main():
    parser = argparse.ArgumentParser(description=" SAGA ARCHIVER (PSP COMPATIBLE)")
    parser.add_argument("--url", "-u", dest="url", default=None,
                        help="Internet Archive directory URL (e.g. https://archive.org/download/shingeki-no-kyojin_aot/season-1_DUB-1080p/)")
    args = parser.parse_args()

    # As a built binary the working directory can be anything (e.g. when
    # double-clicked). Keep output predictable, next to the application.
    if getattr(sys, "frozen", False):
        os.chdir(app_dir())

    print_epic_banner()

    dir_url = args.url
    if not dir_url:
        dir_url = input(f"URL:").strip()

    if dir_url in ["", "/getaot1"]:
        dir_url = DIR_URL

    if not dir_url.endswith("/"):
        dir_url += "/"

    download_folder = DOWNLOAD_FOLDER
    psp_folder = PSP_FOLDER
    if dir_url != DIR_URL:
        if "youtube.com" in dir_url or "youtu.be" in dir_url:
            custom_name = "YouTube_Video"
        else:
            custom_name = ""
            while not custom_name:
                custom_name = input("New URL detected. Please enter a name for the target folder: ").strip()
        download_folder = f"{custom_name}_1080p"
        psp_folder = f"{custom_name}_PSP"

    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(psp_folder, exist_ok=True)

    context = ssl._create_unverified_context()
    is_youtube = "youtube.com/watch" in dir_url or "youtu.be/" in dir_url
    if is_youtube:
        print(f"YouTube URL detected, downloading from: {dir_url}")

        # Check for a local binary first, then the PATH
        yt_binary_path = os.path.join(os.getcwd(), "yt-dlp")
        if os.path.exists(yt_binary_path):
            ytdl_bin = yt_binary_path
        else:
            ytdl_bin = shutil.which("yt-dlp") or shutil.which("youtube-dl")
        
        if not ytdl_bin:
            print("Neither yt-dlp nor youtube-dl was found. Downloading the yt-dlp binary...")
            import platform
            machine = platform.machine().lower()
            if machine == "x86_64":
                yt_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            elif machine.startswith("arm") or machine == "aarch64":
                yt_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
            else:
                yt_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"

            yt_binary_path = os.path.join(os.getcwd(), "yt-dlp")
            print(f"Downloading yt-dlp from {yt_url}...")
            try:
                context = ssl._create_unverified_context()
                with urllib.request.urlopen(yt_url, timeout=30, context=context) as response, open(yt_binary_path, 'wb') as out_file:
                    total_size = int(response.getheader('Content-Length', 0))
                    downloaded = 0
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        out_file.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = int(100 * downloaded / total_size)
                            print(f"\rDownload: {percent}%", end='', flush=True)
                    print(" - Done!")
                os.chmod(yt_binary_path, 0o755)
                ytdl_bin = yt_binary_path
                print("yt-dlp binary installed successfully!")
            except Exception as e:
                print(f"Download failed: {e}")
                print("Please install yt-dlp manually: brew install yt-dlp")
                sys.exit(1)

        yt_output_template = os.path.join(download_folder, "%(title).100s.%(ext)s")
        ytdl_cmd = [
            ytdl_bin,
            "-f", "bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", yt_output_template,
            "-q",
            "--no-warnings",
            dir_url,
        ]

        try:
            subprocess.run(ytdl_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"YouTube download failed: {e}")
            sys.exit(1)

        video_files = [f for f in os.listdir(download_folder) if f.lower().endswith(".mp4")]
        if not video_files:
            print("No MP4 files found in the download folder.")
            sys.exit(1)

        video_files = sorted(set(video_files))

    else:
        print(f"Fetching episode list from Internet Archive: {dir_url}")

        # SSL fix for the macOS certificate error - verification disabled for now
        try:
            # Temporary fix: disable SSL verification due to a certificate chain problem
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(dir_url, context=context) as resp:
                html = resp.read().decode("utf-8")
        except Exception as e:
            print(f"Could not connect to Internet Archive: {e}")
            print("\nRecommended fix:")
            print("1. Run this command:")
            print("   open /Applications/Python*/Install\\ Certificates.command")
            print("2. Then restart this script.")
            print("   Or install certifi:")
            print("   /usr/local/bin/python3 -m pip install --upgrade certifi")
            sys.exit(1)

        # Extract clean .mp4 files
        pattern = r'href="([^"]+\.mp4)"'
        matches = re.findall(pattern, html)

        video_files = [m for m in matches if m.endswith(".mp4") and not m.endswith(".ia.mp4")]

        def episode_key(x):
            match = re.search(r'E(\d+)', x, re.IGNORECASE)
            return int(match.group(1)) if match else 0

        video_files = sorted(set(video_files), key=episode_key)

    print(f"Found {len(video_files)} episodes ready for SAGA EXPORT.\n")

    # Check existing downloads
    existing_files = set(os.listdir(download_folder))
    missing_files = [f for f in video_files if f not in existing_files]

    expected_psp_files = [f"AOT_S01E{str(i).zfill(2)}_PSP.mp4" for i in range(1, len(video_files) + 1)]
    existing_psp_files = set(os.listdir(psp_folder))
    missing_psp_files = [f for f in expected_psp_files if f not in existing_psp_files]
    psp_synced = len(missing_psp_files) == 0

    redownload_all = False
    if not missing_files:
        print("All episodes are already downloaded.")
        response = input("Do you want to re-download them? (y/n): ")
        if response.lower() in ['j', 'ja', 'y', 'yes']:
            redownload_all = True
        else:
            print("Skipping downloads. Existing files will be used.\n")
    else:
        print(f"{len(missing_files)} episodes are missing and will be downloaded.\n")

    if psp_synced:
        print("PSP target folder is already synced (all PSP files are present).\n")
    else:
        print(f"PSP target folder is missing {len(missing_psp_files)} files.\n")

    convert_response = input("Do you want to convert episodes to PSP format now? (y/n): ")
    do_convert = convert_response.lower() in ['j', 'ja', 'y', 'yes']

    for i, filename in enumerate(video_files, 1):
        orig_url = urljoin(dir_url, filename)
        orig_path = os.path.join(download_folder, filename)
        psp_filename = f"AOT_S01E{str(i).zfill(2)}_PSP.mp4"
        psp_path = os.path.join(psp_folder, psp_filename)

        if is_youtube:
            print(f"[{i:02d}/{len(video_files)}] YouTube video detected and already downloaded: {filename}")
        else:
            if not os.path.exists(orig_path) or redownload_all:
                print(f"[{i:02d}/{len(video_files)}] Downloading → {filename}")
                try:
                    req = urllib.request.Request(orig_url)
                    with urllib.request.urlopen(req, context=context) as response, open(orig_path, 'wb') as out_file:
                        total_size = response.getheader('Content-Length')
                        total_size = int(total_size) if total_size and total_size.isdigit() else None
                        downloaded = 0
                        start_time = time.time()

                        while True:
                            chunk = response.read(8192)
                            if not chunk:
                                break
                            out_file.write(chunk)
                            downloaded += len(chunk)

                            elapsed = time.time() - start_time
                            elapsed = max(elapsed, 1e-6)
                            speed = downloaded / elapsed

                            if total_size:
                                percent = downloaded / total_size * 100
                                status = (f"   {percent:6.2f}% "
                                          f"{format_bytes(downloaded)}/{format_bytes(total_size)} "
                                          f"({format_bytes(speed)}/s)")
                            else:
                                status = (f"   {format_bytes(downloaded)} downloaded "
                                          f"({format_bytes(speed)}/s)")

                            print(status, end='\r', flush=True)

                        if total_size:
                            print(f"   100.00% {format_bytes(downloaded)}/{format_bytes(total_size)} ({format_bytes(speed)}/s)")
                        else:
                            print(f"   {format_bytes(downloaded)} downloaded ({format_bytes(speed)}/s)")

                    print(f"   Download complete")
                except Exception as e:
                    print(f"   Download failed → {e}")
                    continue
            else:
                print(f"[{i:02d}/{len(video_files)}] Already downloaded: {filename}")

        if do_convert:
            if not os.path.exists(psp_path):
                print(f"Converting to PSP format (480x272)...")
                duration = get_video_duration(orig_path)
                cmd = [
                    FFMPEG, "-i", orig_path,
                    "-vf", f"scale={PSP_WIDTH}:{PSP_HEIGHT}:force_original_aspect_ratio=decrease,"
                           f"pad={PSP_WIDTH}:{PSP_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
                    "-c:v", "libx264",
                    "-profile:v", "baseline",
                    "-level", "3.0",
                    "-pix_fmt", "yuv420p",
                    "-r", "29.97",
                    "-b:v", "1500k",
                    "-maxrate", "1500k",
                    "-bufsize", "2000k",
                    "-g", "30",
                    "-keyint_min", "30",
                    "-sc_threshold", "0",
                    "-c:a", "aac",
                    "-ar", "48000",
                    "-ac", "2",
                    "-b:a", "128k",
                    "-movflags", "+faststart",
                    "-progress", "pipe:1",
                    "-nostats",
                    "-y",
                    psp_path
                ]

                try:
                    proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                    )

                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            if proc.poll() is not None:
                                break
                            continue

                        line = line.strip()
                        if line.startswith("out_time=") and duration:
                            t = line.split("=", 1)[1]
                            h, m, s = t.split(":")
                            out_time = float(h) * 3600 + float(m) * 60 + float(s)
                            percent = min(100.0, out_time / duration * 100)
                            bar = int(percent // 2)
                            print(f"   Conversion progress: [{('#' * bar).ljust(50)}] {percent:6.2f}%", end='\r', flush=True)
                        elif line.startswith("progress=end"):
                            print(f"   Conversion progress: [{'#' * 50}] 100.00%")

                    retcode = proc.wait()
                    stderr_text = proc.stderr.read().strip()
                    if retcode != 0:
                        raise subprocess.CalledProcessError(retcode, cmd, stderr=stderr_text)

                    print(f"\n   Successfully exported → {psp_filename}")
                except FileNotFoundError:
                    print("   ffmpeg not found! Please install ffmpeg and add it to PATH.")
                    sys.exit(1)
                except subprocess.CalledProcessError as e:
                    print(f"   Conversion failed for episode {i}")
                    print(e.stderr[:700] if e.stderr else stderr_text)
            else:
                print(f"Already exported: {psp_filename}")
        else:
            print(f"Skipping PSP conversion for {psp_filename} as requested.")

    print("\n" + "═" * 85)
    print("SAGA EXPORT COMPLETED SUCCESSFULLY!")
    print("═" * 85)
    print(f"Original 1080p files  → {os.path.abspath(download_folder)}")
    print(f"PSP-ready files       → {os.path.abspath(psp_folder)}")
    print("\nTo play on your PSP:")
    print("   1. Connect PSP via USB")
    print("   2. Copy files to /PSP/COMMON/  or  /VIDEO/")
    print("   3. Disconnect and enjoy the Saga!")
    print("\n" + "═" * 85)


if __name__ == "__main__":
    main()