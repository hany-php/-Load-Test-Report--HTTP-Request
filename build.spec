# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Load Tester application.
"""

import os
import platform

block_cipher = None

# Determine the current OS for including the right ab binary
current_os = platform.system().lower()
if current_os == 'windows':
    ab_binary = ('vendor/ab/windows/ab.exe', 'vendor/ab/windows')
elif current_os == 'darwin':
    ab_binary = ('vendor/ab/macos/ab', 'vendor/ab/macos')
else:
    ab_binary = ('vendor/ab/linux/ab', 'vendor/ab/linux')

# Data files to include
datas = [
    ('assets', 'assets'),
    ('THIRD_PARTY_NOTICES.txt', '.'),
    ('LICENSES', 'LICENSES'),
    ('vendor/ab/README.md', 'vendor/ab'),
]

# Binary files
binaries = [ab_binary]

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LoadTester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LoadTester',
)
