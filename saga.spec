# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller-Konfiguration für ein eigenständiges SAGA-ARCHIVER-Binary.

ffmpeg und ffprobe werden mit eingebettet, damit das Ergebnis ohne jede
Installation läuft. Erwartet werden statische Builds unter vendor/ (siehe
build.sh). Bauen mit:  pyinstaller saga.spec
"""

import os
import sys

HERE = os.path.abspath(SPECPATH)


def vendored(name):
    """Pfad zu einem einzubettenden Binary, vendor/ zuerst."""
    for candidate in (os.path.join(HERE, "vendor", name), os.path.join(HERE, name)):
        if os.path.exists(candidate):
            return candidate
    raise SystemExit(
        f"FEHLER: '{name}' nicht gefunden. Erwartet unter vendor/{name} — "
        f"siehe build.sh."
    )


a = Analysis(
    ['aot_saga_export_simple.py'],
    pathex=[],
    binaries=[
        (vendored('ffmpeg'), '.'),
        (vendored('ffprobe'), '.'),
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='saga',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
