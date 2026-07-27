# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller configuration for a standalone SAGA ARCHIVER binary.

ffmpeg and ffprobe are embedded so the result runs without any installation.
Static builds are expected under vendor/ (see build.sh).
Build with:  pyinstaller saga.spec
"""

import os
import sys

HERE = os.path.abspath(SPECPATH)


def vendored(name):
    """Path to a binary that should be embedded, vendor/ first."""
    for candidate in (os.path.join(HERE, "vendor", name), os.path.join(HERE, name)):
        if os.path.exists(candidate):
            return candidate
    raise SystemExit(
        f"ERROR: '{name}' not found. Expected at vendor/{name} — see build.sh."
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
