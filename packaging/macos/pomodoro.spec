# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

ROOT_DIR = Path(SPECPATH).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

hiddenimports = collect_submodules("pomodoro")


a = Analysis(
    [str(SRC_DIR / "pomodoro" / "__main__.py")],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name="Pomodoro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Pomodoro",
)
app = BUNDLE(
    coll,
    name="Pomodoro.app",
    icon=str(ROOT_DIR / "packaging" / "macos" / "Pomodoro.icns"),
    bundle_identifier="com.example.pomodoro",
    info_plist={
        "NSPrincipalClass": "NSApplication",
        "NSAppleScriptEnabled": False,
    },
)
