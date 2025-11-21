# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('bgimage', 'bgimage'), ('bgimage2', 'bgimage2'), ('cr_data', 'cr_data'), ('cr_data_png', 'cr_data_png'), ('cr_event', 'cr_event'), ('data', 'data'), ('fgimage', 'fgimage'), ('GINKA', 'GINKA'), ('character_analysis.json', '.'), ('ginka_composer', 'ginka_composer')],
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
    [],
    exclude_binaries=True,
    name='GINKA立绘搭配软件',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    name='GINKA立绘搭配软件',
)
