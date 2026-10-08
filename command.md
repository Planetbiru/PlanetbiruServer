# Build & Run Guide — Planetbiru Server

Complete guide for new users who just cloned the repository. Follow the instructions for your operating system.

---

## 📋 Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| **Python** | 3.10 – 3.13 | Python **3.14** is supported starting with PyInstaller 6.15+. For maximum stability, use **Python 3.13**. |
| **Visual C++ Redistributable** | 2015–2022 (x64) | [Download here](https://aka.ms/vs/17/release/vc_redist.x64.exe) |
| **RAM** | 4 GB | For compilation |
| **Disk** | 3 GB | Build + cache + dependencies |

> **⚠️ Python 3.14 Warning:** If you use Python 3.14 and encounter the error `Failed to load Python DLL 'python314.dll'`, see the **Troubleshooting** section at the end.

> **ℹ️ Note:** The `main.py` source code already includes the built-in QtWebEngine fix for `--onefile` mode. You do **not** need to manually patch `main.py` anymore — just build using the spec files below.

---

## 🚀 Mode 1 — Run Directly (Development / No Build)

Good for quick testing. Does **not** produce an `.exe`.

### Windows (PowerShell)

```powershell
# 1. Create virtual environment
py -m venv env

# 2. Activate (PowerShell)
.\env\Scripts\Activate.ps1

# If you get "execution of scripts is disabled", run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Install all dependencies
pip install --upgrade pip
pip install PyQt5 PyQtWebEngine croniter pyinstaller

# 4. Run
python main.py
```

### Windows (Command Prompt / CMD)

```cmd
py -m venv env
env\Scripts\activate.bat
pip install --upgrade pip
pip install PyQt5 PyQtWebEngine croniter pyinstaller
python main.py
```

### Linux / macOS

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install PyQt5 PyQtWebEngine croniter pyinstaller
python main.py
```

---

## 📦 Mode 2 — Build with Spec File (RECOMMENDED)

This is the cleanest and most stable method, and it is **required** for the mini browser (QtWebEngine). The `PlanetbiruServer.spec` file is already provided in the repository and handles automatically:
- Detection of `pythonXXX.dll` (no hardcoded paths)
- Collection of QtWebEngine resources (`QtWebEngineProcess.exe`, `.pak` files, locales)
- UPX disabled (so DLLs are not corrupted)

### Windows

```cmd
:: 1. Create venv & install dependencies
py -m venv env
env\Scripts\activate.bat
pip install --upgrade pip
pip install PyQt5 PyQtWebEngine croniter pyinstaller

:: 2. Ensure latest PyInstaller version
pip install --upgrade --force-reinstall pyinstaller

:: 3. Build
python -m PyInstaller PlanetbiruServer.spec --noconfirm --clean
```

### Linux / macOS

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install PyQt5 PyQtWebEngine croniter pyinstaller
pip install --upgrade --force-reinstall pyinstaller
python -m PyInstaller PlanetbiruServer.spec --noconfirm --clean
```

### Build Output

```
dist/
└── PlanetbiruServer/
    ├── PlanetbiruServer.exe       ← run this
    ├── icon.ico
    ├── localization.ini
    ├── *.png
    └── _internal/
        ├── pythonXXX.dll          ← MUST exist
        ├── PyQt5/
        │   └── Qt5/
        │       ├── bin/QtWebEngineProcess.exe   ← MUST exist (for mini browser)
        │       └── resources/*.pak              ← MUST exist
        └── ...
```

The `PlanetbiruServer/` folder is what you distribute. You can zip it and move it to another computer (provided VC++ Redistributable is installed there).

---

## 🧩 Mode 3 — Build with CLI (Alternative `--onedir`)

If you prefer not to use the `.spec` file, use the `--onedir` command below (`--onefile` is **not recommended** for QtWebEngine).

### Windows

```cmd
mkdir build
python -m PyInstaller --noconsole --onedir ^
    --name PlanetbiruServer ^
    --icon=icon.ico ^
    --hidden-import=croniter ^
    --hidden-import=dateutil ^
    --hidden-import=PyQt5.QtWebEngineWidgets ^
    --hidden-import=PyQt5.QtWebEngineCore ^
    --hidden-import=PyQt5.QtWebEngine ^
    --collect-all PyQt5.QtWebEngineWidgets ^
    --collect-all PyQt5.QtWebEngineCore ^
    --collect-all PyQt5.QtWebChannel ^
    --add-data "icon.ico;." ^
    --add-data "maximize.png;." ^
    --add-data "minimize.png;." ^
    --add-data "start.png;." ^
    --add-data "stop.png;." ^
    --add-data "public.png;." ^
    --add-data "local.png;." ^
    --add-data "apache.png;." ^
    --add-data "php.png;." ^
    --add-data "mariadb.png;." ^
    --add-data "redis.png;." ^
    --add-data "exit.png;." ^
    --add-data "localization.ini;." ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module matplotlib ^
    --exclude-module tkinter ^
    --exclude-module PIL ^
    --exclude-module PyQt5.QtQuick ^
    --exclude-module PyQt5.QtQml ^
    --exclude-module PyQt5.Qt3DCore ^
    --exclude-module PyQt5.QtMultimedia ^
    --exclude-module PyQt5.QtBluetooth ^
    --exclude-module PyQt5.QtDesigner ^
    --upx-dir "" ^
    main.py
```

### Linux / macOS

Replace `^` with `\` and `;` in `--add-data` with `:`:

```bash
mkdir build
python -m PyInstaller --noconsole --onedir \
    --name PlanetbiruServer \
    --icon=icon.ico \
    --hidden-import=croniter \
    --hidden-import=dateutil \
    --hidden-import=PyQt5.QtWebEngineWidgets \
    --hidden-import=PyQt5.QtWebEngineCore \
    --hidden-import=PyQt5.QtWebEngine \
    --collect-all PyQt5.QtWebEngineWidgets \
    --collect-all PyQt5.QtWebEngineCore \
    --collect-all PyQt5.QtWebChannel \
    --add-data "icon.ico:." \
    --add-data "maximize.png:." \
    --add-data "minimize.png:." \
    --add-data "start.png:." \
    --add-data "stop.png:." \
    --add-data "public.png:." \
    --add-data "local.png:." \
    --add-data "apache.png:." \
    --add-data "php.png:." \
    --add-data "mariadb.png:." \
    --add-data "redis.png:." \
    --add-data "exit.png:." \
    --add-data "localization.ini:." \
    --exclude-module numpy \
    --exclude-module pandas \
    --exclude-module matplotlib \
    --exclude-module tkinter \
    --exclude-module PIL \
    --exclude-module PyQt5.QtQuick \
    --exclude-module PyQt5.QtQml \
    --exclude-module PyQt5.Qt3DCore \
    --exclude-module PyQt5.QtMultimedia \
    --exclude-module PyQt5.QtBluetooth \
    --exclude-module PyQt5.QtDesigner \
    main.py
```

---

## 📄 Mode 4 — Single-File Build (All-in-One `.exe`)

> ⚠️ **Important Warning**
>
> `QtWebEngine` (the mini browser) has a **native subprocess** called `QtWebEngineProcess.exe` that must run as a separate process. In `--onefile` mode, PyInstaller extracts everything to a **temporary folder with a random name** each time the app runs. This makes it fragile.
>
> **Good news:** The `main.py` in this repository **already includes the required QtWebEngine environment fix** for `--onefile` mode. You do **not** need to patch the source code — just build with the spec file below.

### 📄 Method 4A — Using a Dedicated Spec File (RECOMMENDED)

Create a new file called `PlanetbiruServer-onefile.spec` in your repository root:

```python
# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all

# ============================================================
# AUTO-DETECT pythonXXX.dll (no hardcoded path)
# ============================================================
def find_python_dll():
    dll_name = f"python{sys.version_info.major}{sys.version_info.minor}.dll"
    candidates = [
        sys.base_prefix,
        os.path.join(sys.base_prefix, "DLLs"),
        os.path.dirname(sys.executable),
        os.path.dirname(sys.executable) + "\\DLLs",
        sys.prefix,
        os.path.join(sys.prefix, "DLLs"),
    ]
    for base in candidates:
        p = os.path.join(base, dll_name)
        if os.path.exists(p):
            return p
    return None

python_dll = find_python_dll()
if python_dll:
    print(f"[SPEC] Bundling Python DLL: {python_dll}")
else:
    print("[SPEC] WARNING: pythonXXX.dll not found.")

# ============================================================
# DATA FILES
# ============================================================
datas = [
    ('icon.ico', '.'),
    ('maximize.png', '.'),
    ('minimize.png', '.'),
    ('start.png', '.'),
    ('stop.png', '.'),
    ('public.png', '.'),
    ('local.png', '.'),
    ('apache.png', '.'),
    ('php.png', '.'),
    ('mariadb.png', '.'),
    ('redis.png', '.'),
    ('exit.png', '.'),
    ('localization.ini', '.'),
]

binaries = []
if python_dll:
    binaries.append((python_dll, '.'))

hiddenimports = [
    'croniter', 'dateutil',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebEngineCore',
    'PyQt5.QtWebEngine',
    'PyQt5.QtWebChannel',
]

for pkg in ['PyQt5.QtWebEngineWidgets', 'PyQt5.QtWebEngineCore', 'PyQt5.QtWebChannel']:
    tmp = collect_all(pkg)
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

# ============================================================
# ANALYSIS
# ============================================================
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy', 'pandas', 'matplotlib', 'tkinter', 'PIL',
        'PyQt5.QtQuick', 'PyQt5.QtQml', 'PyQt5.Qt3DCore',
        'PyQt5.QtMultimedia', 'PyQt5.QtBluetooth', 'PyQt5.QtDesigner',
        'PyQt5.QtSql', 'PyQt5.QtTest', 'PyQt5.QtXml', 'PyQt5.QtXmlPatterns',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# ============================================================
# SINGLE-FILE EXE
# ============================================================
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,              # <-- Embed binaries directly (single file)
    a.datas,                 # <-- Embed data files directly (single file)
    [],
    name='PlanetbiruServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,               # <-- MUST be False for QtWebEngine
    runtime_tmpdir=None,     # <-- Use default temp dir
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
```

**Build command:**

```cmd
python -m PyInstaller PlanetbiruServer-onefile.spec --noconfirm --clean
```

**Output:** `dist/PlanetbiruServer.exe` — one single executable file containing everything.

### 📄 Method 4B — Pure CLI Command (No Spec File)

#### Windows (CMD)

```cmd
mkdir build
python -m PyInstaller --noconsole --onefile ^
    --name PlanetbiruServer ^
    --icon=icon.ico ^
    --noupx ^
    --hidden-import=croniter ^
    --hidden-import=dateutil ^
    --hidden-import=PyQt5.QtWebEngineWidgets ^
    --hidden-import=PyQt5.QtWebEngineCore ^
    --hidden-import=PyQt5.QtWebEngine ^
    --hidden-import=PyQt5.QtWebChannel ^
    --collect-all PyQt5.QtWebEngineWidgets ^
    --collect-all PyQt5.QtWebEngineCore ^
    --collect-all PyQt5.QtWebChannel ^
    --add-data "icon.ico;." ^
    --add-data "maximize.png;." ^
    --add-data "minimize.png;." ^
    --add-data "start.png;." ^
    --add-data "stop.png;." ^
    --add-data "public.png;." ^
    --add-data "local.png;." ^
    --add-data "apache.png;." ^
    --add-data "php.png;." ^
    --add-data "mariadb.png;." ^
    --add-data "redis.png;." ^
    --add-data "exit.png;." ^
    --add-data "localization.ini;." ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module matplotlib ^
    --exclude-module tkinter ^
    --exclude-module PIL ^
    --exclude-module PyQt5.QtQuick ^
    --exclude-module PyQt5.QtQml ^
    --exclude-module PyQt5.Qt3DCore ^
    --exclude-module PyQt5.QtMultimedia ^
    --exclude-module PyQt5.QtBluetooth ^
    --exclude-module PyQt5.QtDesigner ^
    main.py
```

#### Linux / macOS

Replace `^` with `\` and `;` inside `--add-data` with `:`:

```bash
mkdir build
python -m PyInstaller --noconsole --onefile \
    --name PlanetbiruServer \
    --icon=icon.ico \
    --noupx \
    --hidden-import=croniter \
    --hidden-import=dateutil \
    --hidden-import=PyQt5.QtWebEngineWidgets \
    --hidden-import=PyQt5.QtWebEngineCore \
    --hidden-import=PyQt5.QtWebEngine \
    --hidden-import=PyQt5.QtWebChannel \
    --collect-all PyQt5.QtWebEngineWidgets \
    --collect-all PyQt5.QtWebEngineCore \
    --collect-all PyQt5.QtWebChannel \
    --add-data "icon.ico:." \
    --add-data "maximize.png:." \
    --add-data "minimize.png:." \
    --add-data "start.png:." \
    --add-data "stop.png:." \
    --add-data "public.png:." \
    --add-data "local.png:." \
    --add-data "apache.png:." \
    --add-data "php.png:." \
    --add-data "mariadb.png:." \
    --add-data "redis.png:." \
    --add-data "exit.png:." \
    --add-data "localization.ini:." \
    --exclude-module numpy \
    --exclude-module pandas \
    --exclude-module matplotlib \
    --exclude-module tkinter \
    --exclude-module PIL \
    --exclude-module PyQt5.QtQuick \
    --exclude-module PyQt5.QtQml \
    --exclude-module PyQt5.Qt3DCore \
    --exclude-module PyQt5.QtMultimedia \
    --exclude-module PyQt5.QtBluetooth \
    --exclude-module PyQt5.QtDesigner \
    main.py
```

### 🔧 Built-In QtWebEngine Fix (Already Applied)

The `main.py` in this repository **already includes** the required fix for `--onefile` mode. When the app is frozen, it automatically sets these environment variables before creating `QApplication`:

| Environment Variable | Purpose |
|---|---|
| `QTWEBENGINEPROCESS_PATH` | Points to `QtWebEngineProcess.exe` inside the temp-extracted folder |
| `QTWEBENGINE_RESOURCES_PATH` | Points to Chromium `.pak` resources |
| `QTWEBENGINE_LOCALES_PATH` | Points to Chromium locale files |
| `QTWEBENGINE_DISABLE_SANDBOX` | Disables sandbox (required inside temp folders) |
| `QTWEBENGINE_CHROMIUM_FLAGS` | Adds `--no-sandbox --disable-gpu --disable-software-rasterizer` for stability |

These are **only applied when `sys.frozen` is `True`** and the required paths exist, so `--onedir` builds and direct `python main.py` runs are unaffected.

You do **not** need to modify `main.py`. Just build.

### 📊 `--onefile` vs `--onedir` — Which Should You Use?

| Feature | `--onefile` | `--onedir` |
|---|---|---|
| Output | 1 `.exe` (~150–250 MB) | Folder with `.exe` + `_internal/` |
| Startup time | **Slow** (5–15 sec, extracts to temp every launch) | **Fast** (instant) |
| Mini browser stability | Requires built-in fix (already included) | **Rock solid** |
| Antivirus false positives | Very common | Rare |
| Cleanup | Auto (temp folder removed on exit) | None needed |
| Distribution | Single file (easy) | Zip the folder |
| Recommended for QtWebEngine | ⚠️ Usable, but not ideal | ✅ **Recommended** |

**Verdict:** Use `--onefile` only if you absolutely need a single file for distribution. Otherwise, `--onedir` is significantly better.

---

## 🧹 Clean Old Builds

Before rebuilding, delete old folders to avoid leftover metadata:

```cmd
:: Windows
rmdir /s /q build
rmdir /s /q dist
```

```bash
# Linux/macOS
rm -rf build dist
```

Or use the `--clean` flag when calling PyInstaller.

---

## 🔧 Troubleshooting

### ❌ `Failed to load Python DLL 'pythonXXX.dll'`

**Cause:** PyInstaller did not include the Python DLL, or the Python version is too new for PyInstaller.

**Solution:**
1. Ensure PyInstaller **≥ 6.15.0**: `python -m PyInstaller --version`
2. Force update: `pip install --upgrade --force-reinstall pyinstaller`
3. Make sure your `.spec` file includes automatic detection of `pythonXXX.dll` (see `PlanetbiruServer.spec` / `PlanetbiruServer-onefile.spec` in the repo).
4. If it still fails, **downgrade Python to version 3.13**.

### ❌ `no such table: settings`

**Cause:** `get_setting()` is called before `init_db()` in `main.py`.

**Solution:** The current `main.py` already calls `init_db()` immediately after `QApplication(sys.argv)`. If you see this error, **delete the old `setting.db`** next to the `.exe` and restart the app.

### ❌ Mini browser does not appear / blank

**Cause:** QtWebEngine resources were not collected correctly, or (in `--onefile` mode) the environment variables are missing.

**Solution:**
1. Use the spec file (not CLI) which has `collect_all('PyQt5.QtWebEngineWidgets')`.
2. Check for the file `dist/PlanetbiruServer/_internal/PyQt5/Qt5/bin/QtWebEngineProcess.exe` (for `--onedir`).
3. For `--onefile`, the built-in fix in `main.py` handles this automatically. If it still fails, verify the `.exe` was built **after** the `main.py` update.
4. Run the `.exe` from **Command Prompt** (not double-click) to see detailed error messages.

### ❌ UPX corrupts DLLs

**Cause:** UPX compresses DLLs and makes them unloadable.

**Solution:** Use the spec file which sets `upx=False`. If using CLI, add `--noupx`.

### ❌ Single-file `.exe` starts then immediately closes

**Cause:** Uncaught exception at startup (often `no such table: settings` or missing DLL).

**Solution:**
1. Run the `.exe` from **Command Prompt** to see the actual error message.
2. Ensure `init_db()` is called immediately after `QApplication(sys.argv)` (already the case in current `main.py`).
3. Ensure the latest `main.py` is used (with built-in QtWebEngine fix).

### ❌ Antivirus quarantines the single-file `.exe`

**Cause:** PyInstaller bootloader signature is often flagged as suspicious.

**Solution:**
1. Add the output folder to your antivirus whitelist.
2. Or use `--onedir` mode, which is less frequently flagged.

---

## ✅ Pre-Distribution Checklist

**For `--onedir` builds:**
- [ ] `dist/PlanetbiruServer/_internal/pythonXXX.dll` exists
- [ ] `dist/PlanetbiruServer/_internal/PyQt5/Qt5/bin/QtWebEngineProcess.exe` exists
- [ ] `dist/PlanetbiruServer/_internal/PyQt5/Qt5/resources/` contains `.pak` files
- [ ] `icon.ico`, `localization.ini`, and all `*.png` files are in the root of `dist/PlanetbiruServer/`
- [ ] Run the `.exe` on a clean machine (without Python) to verify all DLLs are included
- [ ] Ensure VC++ Redistributable (x64) is installed on the target machine

**For `--onefile` builds:**
- [ ] Only `dist/PlanetbiruServer.exe` exists (single file)
- [ ] File size is ~150–250 MB (indicates QtWebEngine was embedded)
- [ ] `main.py` contains the built-in QtWebEngine environment fix (check for `QTWEBENGINEPROCESS_PATH`)
- [ ] Test the `.exe` from a folder **without** the source code
- [ ] Test mini browser (Open Web / phpMyAdmin buttons) works
- [ ] Ensure VC++ Redistributable (x64) is installed on the target machine

---

## 📝 Quick Summary

| Purpose | Command |
|---|---|
| **Run directly (dev)** | `python main.py` |
| **Build onedir (recommended)** | `python -m PyInstaller PlanetbiruServer.spec --noconfirm --clean` |
| **Build onefile (single .exe)** | `python -m PyInstaller PlanetbiruServer-onefile.spec --noconfirm --clean` |
| **Clean build** | `rmdir /s /q build dist` (Win) or `rm -rf build dist` (Unix) |
| **Check PyInstaller version** | `python -m PyInstaller --version` |
| **Update PyInstaller** | `pip install --upgrade --force-reinstall pyinstaller` |
| **Distribute (onedir)** | Zip the `dist/PlanetbiruServer/` folder |
| **Distribute (onefile)** | Copy `dist/PlanetbiruServer.exe` |
