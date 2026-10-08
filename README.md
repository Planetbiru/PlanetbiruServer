# Planetbiru Server Control Panel

A lightweight, **multi-instance** server management tool built with Python and PyQt5. It manages Apache, MariaDB (MySQL), and Redis services with ease — including a built-in cron scheduler, activity logging, and true **per-instance isolation**.

## Advantages

Planetbiru Server Control Panel has several key advantages that distinguish it from many other server panels, especially those that are web-based or require complex installations:

### Maximum Portability (True Portable)

**No Installation/Registry:**
The application is designed to be truly portable. Simply extract the folder to any location (USB drive, cloud folder, etc.) and run it. No traces are left on the operating system (such as registry entries or files in Program Files), unless the "Run on Windows Startup" feature is manually enabled. Ideal for developers, educators, or anyone who needs a quick server environment across multiple machines.

**Isolated Environment:**
All dependencies, configurations, and service data (Apache, MariaDB, Redis) are stored within a single directory. This minimizes conflicts with other server installations on the system and makes backup or migration easier.

### True Multi-Instance Support

**One Binary, Many Independent Servers:**
Duplicate `PlanetbiruServer.exe` to `server-01.exe`, `server-02.exe`, etc. Each copy becomes a fully independent instance with:

*   Its own SQLite database (`server-01.db`, `server-02.db`) — for settings, logs, cron jobs, and startup tasks.
*   Its own Apache, MariaDB, and Redis configuration (`config/server-01-*.conf`).
*   Its own data folder (`instances/server-01/data/mysql`, `instances/server-01/data/redis`).
*   Its own document root (`instances/server-01/www`).
*   Its own log and session folders (`instances/server-01/logs`, `instances/server-01/sessions`).
*   Its own Windows registry key for auto-start (no collision between instances).
*   Its own mutex — you can run all instances simultaneously without conflict.

**Unique Ports per Instance:**
Each instance listens on its own ports (e.g., Apache 80/81, MariaDB 3306/3307, Redis 6379/6380), so multiple servers can run side by side on the same machine.

**Shared Binaries, Isolated Data:**
Apache, MariaDB, PHP, Redis, and phpMyAdmin binaries are **shared** (one copy in the root folder), saving hundreds of MB. Only the *data* and *config* are per-instance.

### Flexible Local and Public Control

**Easy Mode Switching:**
Quickly toggle each service between "Local Mode" (127.0.0.1) and "Public Mode" (0.0.0.0) per instance. Useful for security and convenience during local development or presentations, without manually editing config files.

**Intelligent Service Status Detection:**
Before running or stopping services, the application checks both port availability and active process IDs (PIDs) to accurately determine service status and prevent conflicts, warning if ports are already in use.

### Enhanced Stability and Security

**Secure MariaDB "Force Reset" Feature:**
If the MariaDB root password is forgotten, the force reset feature can be used. This is protected by a separate Administrator Password that is hashed (SHA-256) and stored in the instance's internal database. Each instance has its own admin password.

**Graceful Process Management:**
Services (Apache, MariaDB, Redis) are stopped gracefully, allowing them time to close connections and save data instead of being forcefully terminated. This reduces the risk of data corruption. The application tracks running service PIDs per instance.

**Mutex for Single Instance (per name):**
Ensures only one instance of each `.exe` runs at a time. `server-01.exe` and `server-02.exe` use different mutex names, so they coexist peacefully.

### Powerful Automation and Task Management

**Built-in Cron Scheduler:**
Each instance has its own cron scheduler — jobs defined in `server-01.exe` are not visible to `server-02.exe`. Useful for maintenance tasks, backups, or running background scripts on a per-instance basis.

**Background Task Management:**
Tasks executed by the scheduler run in the background without intrusive console windows.

**Customizable Startup Automation:**
Define custom commands to run automatically when a specific instance starts. Perfect for initializing development tools, proxies, or custom scripts.

### Intuitive and Multilingual User Experience

**Responsive PyQt5 Interface:**
Fast and responsive desktop experience with immediate visual feedback on service actions (Start/Stop) and logical status messages during transitions (e.g., 'Running... (Stopping...)').

**Comprehensive System Tray Integration:**
Each instance has its own tray icon. Since the tray icon title includes the instance name, you can distinguish multiple running panels at a glance.

**Full Multilingual Support (Including RTL):**
The application supports multiple languages with consistent translations and automatic layout adjustments for Right-to-Left (RTL) languages such as Arabic and Urdu.

**Real-time Activity Logging:**
All important actions and service statuses are logged in real-time into the instance's own SQLite database, making monitoring and debugging easier.

### Automatic and Flexible Configuration

**Three-Tier Template System:**
Configuration files are generated using a clear three-tier approach:

1.  **Tier 1 (Canonical)**: `config/httpd-template.conf` — the master template. **Edit this to customize.** Uses placeholders like `{INSTALL_ROOT}`, `{APACHE_PORT}`, `{INSTANCE_WWW}`, etc.
2.  **Tier 2 (Instance Template)**: `config/server-01-httpd-template.conf` — auto-synced copy of Tier 1. **Do not edit** — it will be overwritten.
3.  **Tier 3 (Final Config)**: `config/server-01-httpd.conf` — generated output with all placeholders replaced. Consumed by Apache/MariaDB/Redis/PHP at runtime. **Do not edit.**

This makes it trivial to update a common setting (e.g., add a new Apache module) across all instances: edit Tier 1 and restart each instance.

**Shared phpMyAdmin:**
One copy of phpMyAdmin in `phpMyAdmin/` is served by every Apache instance through an `Alias` directive. It automatically connects to the correct MariaDB port by reading the `MYSQL_PORT` environment variable set per instance.

### Cross-Instance Coordination

**Shared `config.db`:**
A lightweight SQLite file at the root (`config.db`) records each instance's ports and application ID in the `instance_config` table. phpMyAdmin uses this as a fallback to locate the correct MariaDB port if the environment variable is missing — and any future tool can query it for routing purposes.

**Dynamic Per-Instance Starter Page:**
Each instance's `www/index.php` is a **live** page that reads ports from `config.db`, probes Apache/MariaDB/Redis with `fsockopen()`, and displays real-time service status. No static values — always up-to-date.

---

## 🚀 Features

*   **Multi-Instance Support:** Run multiple independent servers from the same binary. Each `.exe` (or `APP_NAME` env var) gets its own database, config, logs, sessions, and data.
*   **Service Management:** Individual and batch control (Start/Stop) for Apache, MariaDB, and Redis, per instance.
    *   **Intelligent Status Detection:** Uses both port and PID to ensure accurate UI representation.
*   **Access Control:** Toggle services between **Local Mode** (127.0.0.1) and **Public Mode** (0.0.0.0).
*   **MariaDB Password Management:** Change or reset the MariaDB root password. Secure **Force Reset** protected by a hashed Administrator Password (per instance).
*   **Redis Data Management:** Integrated Redis CLI and a built-in **Redis Data Viewer** (Strings, Lists, Sets, Hashes, ZSets) with real-time search.
*   **Precise Cron Scheduler:** Execute system commands or PHP scripts using cron expressions, per instance.
*   **Startup Task Manager:** Manage commands executed when the panel opens. Includes real-time status, PID tracking, and manual start/stop.
*   **System Tray Integration:** Runs in background. Tray icon title includes instance name.
*   **Port Collision Detection:** Warns before starting services if ports are already in use.
*   **Activity Logging:** Real-time, thread-safe SQLite logging per instance.
*   **Three-Tier Configuration:** Clear separation between master template, instance template, and final config.
*   **Shared phpMyAdmin via Apache Alias:** One copy serves all instances; auto-selects correct MariaDB port.
*   **Per-Instance PHP Configuration:** Each instance has its own `php.ini` (with `extension=mysqli`, etc.) — isolated extensions, error logs, session paths.
*   **Multi-language Support:** English, Indonesian, Malay, Javanese, Sundanese, Chinese, Japanese, Korean, Hindi, Arabic, and Urdu.
*   **RTL Support:** Automatic layout adjustment for Right-to-Left languages.
*   **Windows Integration:** Graceful process termination, per-instance registry key, per-instance mutex.
*   **Responsive UI:** Remembers window size and maximization state per instance.

---

## 🏗️ Multi-Instance Architecture

### Instance Identity

`APP_NAME` is derived from the executable filename (without extension). For `server-01.exe`, `APP_NAME = "server-01"`. In development mode, use the environment variable:

```cmd
set APP_NAME=server-01
python main.py
```

### Directory Layout

```
<root>/
├── PlanetbiruServer.exe            ← default instance
├── server-01.exe                   ← copy for a new instance
├── server-02.exe                   ← another one
├── PlanetbiruServer.db             ← instance database
├── server-01.db
├── server-02.db
├── config.db                       ← shared: instance_config table
│
├── config/                         ← canonical templates + generated configs
│   ├── httpd-template.conf         ← Tier 1 (edit here)
│   ├── my-template.ini
│   ├── php-template.ini
│   ├── redis.windows-service-template.conf
│   │
│   ├── server-01-httpd-template.conf       ← Tier 2 (auto-synced)
│   ├── server-01-httpd.conf                ← Tier 3 (generated)
│   ├── server-01-my-template.ini
│   ├── server-01-my.ini
│   ├── server-01-redis.windows-service-template.conf
│   ├── server-01-redis.conf
│   │
│   └── server-02-*                         ← same for each instance
│
├── instances/                      ← per-instance data & document roots
│   ├── server-01/
│   │   ├── php.ini                         ← PHP configuration for this instance
│   │   ├── www/                            ← document root
│   │   │   └── index.php
│   │   ├── data/
│   │   │   ├── mysql/                      ← MariaDB datadir
│   │   │   └── redis/                      ← Redis dump directory
│   │   ├── logs/                           ← Apache, PHP, MariaDB, Redis logs
│   │   ├── tmp/
│   │   ├── sessions/
│   │   ├── apache.pid
│   │   └── apache.scoreboard
│   │
│   └── server-02/                          ← same structure
│
├── apache/            ← shared Apache binary
├── mysql/             ← shared MariaDB binary
├── php/               ← shared PHP binary
├── redis/             ← shared Redis binary
└── phpMyAdmin/        ← shared phpMyAdmin (served via Apache Alias)
```

### Key Points

| Concern | Shared? | Location |
|---|---|---|
| **Binary** (Apache, MariaDB, PHP, Redis) | ✅ Shared | `<root>/apache/`, `<root>/mysql/`, etc. |
| **phpMyAdmin** | ✅ Shared | `<root>/phpMyAdmin/` |
| **Canonical template** | ✅ Shared | `<root>/config/*-template.*` |
| **Config (final)** | ❌ Per-instance | `<root>/config/<APP_NAME>-*.conf` |
| **Database** (settings, logs, cron) | ❌ Per-instance | `<root>/<APP_NAME>.db` |
| **Document root** | ❌ Per-instance | `<root>/instances/<APP_NAME>/www/` |
| **MariaDB data** | ❌ Per-instance | `<root>/instances/<APP_NAME>/data/mysql/` |
| **Redis dump** | ❌ Per-instance | `<root>/instances/<APP_NAME>/data/redis/` |
| **Logs** | ❌ Per-instance | `<root>/instances/<APP_NAME>/logs/` |
| **Sessions** | ❌ Per-instance | `<root>/instances/<APP_NAME>/sessions/` |
| **Registry key** (auto-start) | ❌ Per-instance | `PortableServerPanel_<APP_NAME>` |
| **Mutex** (single-instance) | ❌ Per-instance | `PortableServerControlPanelMutex_<APP_NAME>` |

---

## 🛠️ Prerequisites

*   **Operating System:** Windows (uses Windows-specific APIs for Mutex, Registry, and Process management).
*   **Python:** 3.10 or higher recommended.
*   **Server Binaries:** The application expects the following directory structure in the root folder:
    *   `/apache` (containing `bin/httpd.exe`)
    *   `/mysql` (containing `bin/mysqld.exe`)
    *   `/redis` (containing `redis-server.exe`)
    *   `/php` (containing `php.exe` and extensions)
    *   `/phpMyAdmin` (containing phpMyAdmin files)

---

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Planetbiru/PlanetbiruServer.git
    cd PlanetbiruServer
    ```

2.  **Install dependencies:**
    ```bash
    pip install PyQt5 croniter
    ```

3.  **Setup templates:** Ensure your `config/` folder contains the canonical templates:
    *   `httpd-template.conf`
    *   `php-template.ini`
    *   `my-template.ini`
    *   `redis.windows-service-template.conf`

    Use placeholders like `{INSTALL_ROOT}`, `{INSTANCE_WWW}`, `{INSTANCE_LOGS}`, `{APACHE_PORT}`, `{MYSQL_PORT}`, `{REDIS_PORT}`, `{PHPMYADMIN_DIR}`, `{CONFIG_DIR}` — these are dynamically replaced at runtime.

4.  **Setup phpMyAdmin:** Download phpMyAdmin from [phpmyadmin.net](https://www.phpmyadmin.net/downloads/) and extract its contents into `<root>/phpMyAdmin/`. Create `<root>/phpMyAdmin/config.inc.php` reading `MYSQL_PORT` from environment:

    ```php
    <?php
    $cfg['blowfish_secret'] = 'YourSecret32CharsMinimumHere';
    $i = 0;
    $i++;
    $cfg['Servers'][$i]['auth_type'] = 'cookie';
    $cfg['Servers'][$i]['host']      = '127.0.0.1';
    $cfg['Servers'][$i]['port']      = getenv('MYSQL_PORT') ?: '3306';
    $cfg['Servers'][$i]['compress']  = false;
    $cfg['Servers'][$i]['AllowNoPassword'] = true;
    $cfg['Servers'][$i]['extension'] = 'mysqli';
    ```

---

## 🖥️ Usage

### Single Instance

```bash
python main.py
```

The application automatically prepares the environment (creates `instances/main/`, generates configs) and generates the starter `index.php`.

### Multiple Instances

**Step 1 — Copy the executable:**

```cmd
copy PlanetbiruServer.exe server-01.exe
copy PlanetbiruServer.exe server-02.exe
```

**Step 2 — Run each one.** Each instance will:

*   Create its own database (`server-01.db`, `server-02.db`)
*   Create its own folder (`instances/server-01/`, `instances/server-02/`)
*   Generate configs from the shared templates
*   Default to ports 80 / 3306 / 6379

**Step 3 — Configure distinct ports.** Open each instance, click **Configure App**:

| Instance | Apache Port | MariaDB Port | Redis Port |
|---|---|---|---|
| `server-01.exe` | 80 | 3306 | 6379 |
| `server-02.exe` | 81 | 3307 | 6380 |
| `server-03.exe` | 82 | 3308 | 6381 |

Each Save updates `config.db`, so phpMyAdmin will route to the correct MariaDB port automatically.

**Step 4 — Start services.** Click **Start All Services** in each panel. Verify with:

```cmd
netstat -ano | findstr ":80 :81 :3306 :3307 :6379 :6380"
```

**Step 5 — Access your applications:**

*   Instance 1: `http://localhost/`
*   Instance 2: `http://localhost:81/`
*   phpMyAdmin (instance 1): `http://localhost/phpMyAdmin/`
*   phpMyAdmin (instance 2): `http://localhost:81/phpMyAdmin/`

### Configuration Management (Three Tiers)

**To add a new Apache module for all instances:**

1.  Edit `config/httpd-template.conf` (Tier 1).
2.  Restart every instance. Tier 2 files auto-sync, Tier 3 regenerates.

**To customize just one instance** (e.g., different `<Directory>` block):

1.  Edit `config/server-02-httpd-template.conf` (Tier 2) **after** stopping the instance.
2.  Do **not** restart the whole app — just start Apache. But note: the next app restart will re-sync from Tier 1 and overwrite your Tier 2 changes.

    _Better approach:_ If a per-instance tweak is permanent, add a placeholder-driven branch to the canonical template.

**To reset a corrupted config:**

1.  Delete `config/server-02-httpd-template.conf` and `config/server-02-httpd.conf`.
2.  Restart the instance. Both will be regenerated from Tier 1.

---

## 📂 Project Structure

### Core Files
*   **`main.py`**: The central engine. Manages PyQt5 GUI, per-instance SQLite database, cron scheduler, and the lifecycle of Apache, MariaDB, and Redis processes. Handles multi-instance path resolution based on `APP_NAME`.
*   **`localization.ini`**: All UI strings. Enables multi-language support and defines layout directions (LTR/RTL).
*   **`icon.ico`**: The primary application icon.

### System Tray & UI Assets
*   **Service Branding** (`apache.png`, `mariadb.png`, `redis.png`, `php.png`): Icons for service submenus, config dropdowns, password management, log categories, and Redis Data tools.
*   **Status Indicators**:
    *   `start.png` / `stop.png`: Service active/inactive state.
    *   `public.png` / `local.png`: Public (0.0.0.0) vs. Local (127.0.0.1) mode.
*   **Window & App Control**:
    *   `maximize.png` / `minimize.png`: Show / Minimize to Tray.
    *   `exit.png`: Terminate the panel and its managed services.

### Generated at Runtime
*   **`<APP_NAME>.db`**: Per-instance SQLite database (settings, logs, cron jobs, startup tasks).
*   **`config.db`**: Shared SQLite database (`instance_config` table).
*   **`config/<APP_NAME>-*`**: Per-instance template and final configs.
*   **`instances/<APP_NAME>/`**: Per-instance data, document root, logs, sessions, PHP ini.

---

## 🛠️ Building the Executable

To bundle the application into a single `.exe` using PyInstaller:

```cmd
python -m PyInstaller ^
  --noconsole ^
  --onefile ^
  --name PlanetbiruServer ^
  --icon=icon.ico ^
  --hidden-import=croniter ^
  --hidden-import=dateutil ^
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
  --add-data "config\httpd-template.conf;config" ^
  --add-data "config\php-template.ini;config" ^
  --add-data "config\my-template.ini;config" ^
  --add-data "config\redis.windows-service-template.conf;config" ^
  --exclude-module numpy ^
  --exclude-module pandas ^
  --exclude-module matplotlib ^
  main.py
```

**Note:** If you plan to build a single `.exe` and later copy it for multi-instance use, the embedded templates (`config/*-template.*`) will be extracted to `sys._MEIPASS` at runtime and copied to `config/` beside the executable on first launch. After the first run, you can freely edit these templates.

**Important:** Do not rename the base executable before the first run if you want `PlanetbiruServer` as the default instance name. After the first run, duplicating to `server-01.exe`, `server-02.exe` works cleanly.

---

## 📄 License

This project is open-source and available under the MIT License.

---

Visit our website: https://planetbiru.com

---
*Created by Kamshory*

*Note: This project is designed to be portable. Ensure you have write permissions to the application directory.*