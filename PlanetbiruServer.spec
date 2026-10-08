# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('icon.ico', '.'), ('maximize.png', '.'), ('minimize.png', '.'), ('start.png', '.'), ('stop.png', '.'), ('public.png', '.'), ('local.png', '.'), ('apache.png', '.'), ('php.png', '.'), ('mariadb.png', '.'), ('redis.png', '.'), ('exit.png', '.'), ('localization.ini', '.')]
binaries = []
hiddenimports = ['croniter', 'dateutil', 'PyQt5.QtWebEngineWidgets', 'PyQt5.QtWebEngineCore', 'PyQt5.QtWebEngine', 'PyQt5.QtWebChannel']
tmp_ret = collect_all('PyQt5.QtWebEngineWidgets')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt5.QtWebEngineCore')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt5.QtWebChannel')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas', 'matplotlib', 'tkinter', 'PIL', 'PyQt5.QtQuick', 'PyQt5.QtQml', 'PyQt5.Qt3DCore', 'PyQt5.QtMultimedia', 'PyQt5.QtBluetooth', 'PyQt5.QtDesigner'],
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
    name='PlanetbiruServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
