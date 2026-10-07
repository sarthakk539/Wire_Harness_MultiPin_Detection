# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Wire Harness Detector

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('docs', 'docs'),
        ('examples', 'examples'),
    ],
    hiddenimports=[
        'cv2',
        'numpy',
        'backend.multi_pin_bfs',
        'backend.getsequence',
        'backend.reference',
        'backend.compare',
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
    a.binaries,
    a.datas,
    [],
    name='WireHarnessDetector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Uncomment below to create a macOS .app bundle
# app = BUNDLE(
#     exe,
#     name='WireHarnessDetector.app',
#     icon=None,
#     bundle_identifier=None,
#     info_plist={
#         'NSPrincipalClass': 'NSApplication',
#     },
# )
