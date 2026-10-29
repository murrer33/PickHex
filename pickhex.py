import json
import os
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PyQt6.QtCore import (
    QPoint,
    QPointF,
    QRect,
    QRectF,
    Qt,
    QThread,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QAction,
    QActionGroup,
    QColor,
    QCursor,
    QFont,
    QGuiApplication,
    QIcon,
    QImage,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QScreen,
    QWheelEvent,
)
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMenu,
    QProgressBar,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

APP_NAME = "PickHex"
APP_VERSION = "1.1.1"
DEFAULT_GITHUB_REPO = "murrer33/PickHex"
SINGLE_INSTANCE_KEY = "PickHexSingleInstanceServer_v1"

SUPPORTED_FORMATS = ("HEX", "HEX_RAW", "RGB", "HSL", "CSS", "TAILWIND")

# ---------------------------------------------------------------------------
# Localization (TR / EN)
# ---------------------------------------------------------------------------
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "tr": {
        "welcome_title": "PickHex — Dil Seçimi",
        "welcome_subtitle": "Lütfen kullanmak istediğiniz dili seçin:\nPlease select your preferred language:",
        "welcome_note": "Bu ayarı daha sonra sağ alttaki sistem tepsisi (Hidden Icons) menüsünden değiştirebilirsiniz.",
        "btn_start": "Başla / Start",
        "tray_tooltip": "PickHex v{ver} — Renk Seçici (Tıkla ve Renk Seç)",
        "menu_pick": "🎯 Ekrandan Renk Seç",
        "menu_recent": "Son Seçilen Renkler",
        "menu_no_recent": "Henüz renk seçilmedi",
        "menu_clear_recent": "Geçmişi Temizle",
        "menu_copy_default": "📋 Hızlı Kopyala ({code})",
        "menu_copy_formats": "Farklı Formatta Kopyala",
        "menu_shades_tints": "🎨 Tonlar ve Gölgeler (Shades & Tints)",
        "shade_lighter": "Açık Ton +{pct}%  ({hex})",
        "shade_base": "Ana Renk  ({hex})",
        "shade_darker": "Koyu Gölge -{pct}%  ({hex})",
        "shade_complement": "Zıt (Tamamlayıcı) Renk  ({hex})",
        "menu_format": "Varsayılan Kopyalama Formatı",
        "menu_lang": "Dil / Language",
        "menu_startup": "Bilgisayar Açıldığında Başlat",
        "menu_update": "🔄 Güncellemeleri Kontrol Et (v{ver})",
        "menu_quit": "Çıkış",
        "toast_copied": "Renk kodu kopyalandı: {code}",
        "toast_running_win": "PickHex arka planda çalışıyor! Renk seçmek için sağ alttaki ikona tıklayın.",
        "toast_running_mac": "PickHex üst menü çubuğunda çalışıyor! Renk seçmek için ikona tıklayın.",
        "toast_checking_update": "Güncellemeler kontrol ediliyor...",
        "toast_up_to_date": "PickHex güncel! (Sürüm v{ver})",
        "toast_update_error": "Güncelleme kontrolü başarısız oldu (GitHub sürümü bulunamadı).",
        "upd_title": "PickHex — Yeni Güncelleme Mevcut",
        "upd_found": "Yeni sürüm bulundu: v{latest}  (Mevcut: v{current})",
        "upd_notes": "Uygulama otomatik olarak indirilecek ve yeniden başlatılacaktır. Eski sürümü silmenize gerek yoktur.",
        "upd_btn_now": "Şimdi Güncelle ve Yeniden Başlat",
        "upd_btn_later": "Daha Sonra",
        "upd_downloading": "İndiriliyor... %{pct}",
        "upd_installing": "Güncelleme uygulanıyor, lütfen bekleyin...",
        "hud_controls": "Tekerlek: Zoom  |  Oklar: 1px  |  Tab: Format",
    },
    "en": {
        "welcome_title": "PickHex — Language Selection",
        "welcome_subtitle": "Please select your preferred language:\nLütfen kullanmak istediğiniz dili seçin:",
        "welcome_note": "You can change this anytime from the system tray / menu bar icon.",
        "btn_start": "Start / Başla",
        "tray_tooltip": "PickHex v{ver} — Color Picker (Click to Pick Color)",
        "menu_pick": "🎯 Pick Color from Screen",
        "menu_recent": "Recent Colors",
        "menu_no_recent": "No colors picked yet",
        "menu_clear_recent": "Clear History",
        "menu_copy_default": "📋 Quick Copy ({code})",
        "menu_copy_formats": "Copy Color As...",
        "menu_shades_tints": "🎨 Shades & Tints",
        "shade_lighter": "Tint +{pct}%  ({hex})",
        "shade_base": "Base Color  ({hex})",
        "shade_darker": "Shade -{pct}%  ({hex})",
        "shade_complement": "Complementary  ({hex})",
        "menu_format": "Default Copy Format",
        "menu_lang": "Language / Dil",
        "menu_startup": "Run on System Startup",
        "menu_update": "🔄 Check for Updates (v{ver})",
        "menu_quit": "Quit",
        "toast_copied": "Color code copied: {code}",
        "toast_running_win": "PickHex is running in the system tray! Click the icon to pick a color.",
        "toast_running_mac": "PickHex is running in the menu bar! Click the icon to pick a color.",
        "toast_checking_update": "Checking for updates...",
        "toast_up_to_date": "PickHex is up to date! (v{ver})",
        "toast_update_error": "Could not check for updates (No GitHub release found yet).",
        "upd_title": "PickHex — Update Available",
        "upd_found": "New version available: v{latest}  (Current: v{current})",
        "upd_notes": "PickHex will download and replace itself automatically. No manual reinstall needed.",
        "upd_btn_now": "Update & Restart Now",
        "upd_btn_later": "Later",
        "upd_downloading": "Downloading... {pct}%",
        "upd_installing": "Applying update, restarting...",
        "hud_controls": "Scroll: Zoom  |  Arrows: 1px  |  Tab: Format",
    },
}


# ---------------------------------------------------------------------------
# Color Formatting & Harmonies Helper
# ---------------------------------------------------------------------------
def format_qcolor(color: QColor, fmt: str) -> str:
    hex_code = color.name().upper()
    if fmt == "HEX_RAW":
        return hex_code.lstrip("#")
    elif fmt == "RGB":
        return f"rgb({color.red()}, {color.green()}, {color.blue()})"
    elif fmt == "HSL":
        h = max(0, color.hslHue())
        s = round((color.hslSaturation() / 255.0) * 100)
        l = round((color.lightness() / 255.0) * 100)
        return f"hsl({h}, {s}%, {l}%)"
    elif fmt == "CSS":
        return f"color: {hex_code};"
    elif fmt == "TAILWIND":
        return f"bg-[{hex_code}]"
    return hex_code


def generate_shades_and_tints(hex_color: str) -> List[Tuple[str, int, str]]:
    base = QColor(hex_color)
    r, g, b = base.red(), base.green(), base.blue()
    results: List[Tuple[str, int, str]] = []

    for pct in (60, 40, 20):
        factor = pct / 100.0
        nr = min(255, round(r + (255 - r) * factor))
        ng = min(255, round(g + (255 - g) * factor))
        nb = min(255, round(b + (255 - b) * factor))
        results.append(("lighter", pct, QColor(nr, ng, nb).name().upper()))

    results.append(("base", 0, base.name().upper()))

    for pct in (20, 40, 60):
        factor = 1.0 - (pct / 100.0)
        nr = max(0, round(r * factor))
        ng = max(0, round(g * factor))
        nb = max(0, round(b * factor))
        results.append(("darker", pct, QColor(nr, ng, nb).name().upper()))

    h, s, l, a = base.getHsl()
    if h >= 0:
        comp = QColor.fromHsl((h + 180) % 360, s, l, a)
    else:
        comp = QColor(255 - r, 255 - g, 255 - b)
    results.append(("complement", 180, comp.name().upper()))

    return results


# ---------------------------------------------------------------------------
# Configuration Management
# ---------------------------------------------------------------------------
class ConfigManager:
    def __init__(self) -> None:
        self.config_dir = Path.home() / ".pickhex"
        self.config_file = self.config_dir / "config.json"
        self.data = {
            "language": None,
            "format": "HEX",
            "grid_radius": 5,
            "github_repo": DEFAULT_GITHUB_REPO,
            "recent_colors": [],
        }
        self.load()

    def load(self) -> None:
        try:
            if self.config_file.exists():
                loaded = json.loads(self.config_file.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    self.data.update(loaded)
        except Exception:
            pass

    def save(self) -> None:
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.config_file.write_text(
                json.dumps(self.data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    @property
    def lang(self) -> str:
        val = self.data.get("language")
        return val if val in ("tr", "en") else "tr"

    @lang.setter
    def lang(self, value: str) -> None:
        self.data["language"] = value
        self.save()

    @property
    def is_first_run(self) -> bool:
        return self.data.get("language") not in ("tr", "en")

    @property
    def color_format(self) -> str:
        fmt = self.data.get("format", "HEX")
        return fmt if fmt in SUPPORTED_FORMATS else "HEX"

    @color_format.setter
    def color_format(self, value: str) -> None:
        self.data["format"] = value
        self.save()

    @property
    def grid_radius(self) -> int:
        val = self.data.get("grid_radius", 5)
        return max(3, min(9, int(val))) if isinstance(val, int) else 5

    @grid_radius.setter
    def grid_radius(self, value: int) -> None:
        self.data["grid_radius"] = max(3, min(9, int(value)))
        self.save()

    @property
    def github_repo(self) -> str:
        return str(self.data.get("github_repo") or DEFAULT_GITHUB_REPO)

    @property
    def recent_colors(self) -> List[str]:
        items = self.data.get("recent_colors", [])
        return [str(x) for x in items if isinstance(x, str)][:8]

    def add_recent_color(self, hex_code: str) -> None:
        hex_code = hex_code.upper()
        current = [c.upper() for c in self.recent_colors if c.upper() != hex_code]
        current.insert(0, hex_code)
        self.data["recent_colors"] = current[:8]
        self.save()

    def clear_recent_colors(self) -> None:
        self.data["recent_colors"] = []
        self.save()


# ---------------------------------------------------------------------------
# Auto-Update System (GitHub Releases API + In-Place Binary Replacement)
# ---------------------------------------------------------------------------
def parse_version_tuple(ver_str: str) -> Tuple[int, ...]:
    cleaned = ver_str.strip().lstrip("vV")
    parts = []
    for p in cleaned.split("."):
        num = "".join(ch for ch in p if ch.isdigit())
        parts.append(int(num) if num else 0)
    return tuple(parts or [0])


def cleanup_old_update_artifacts() -> None:
    """Deletes leftover .old executable from a previous self-update."""
    if getattr(sys, "frozen", False):
        old_exe = Path(sys.executable + ".old")
        if old_exe.exists():
            try:
                old_exe.unlink()
            except Exception:
                pass


def _urlopen_with_ssl_fallback(req: urllib.request.Request, timeout: int = 10):
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), ssl.SSLError):
            ctx = ssl._create_unverified_context()
            return urllib.request.urlopen(req, timeout=timeout, context=ctx)
        raise


class ReleaseCheckWorker(QThread):
    # (status, latest_version, download_url, release_body)
    # status: "up_to_date" | "update_available" | "error"
    finished_check = pyqtSignal(str, str, str, str)

    def __init__(self, repo: str) -> None:
        super().__init__()
        self.repo = repo

    def run(self) -> None:
        url = f"https://api.github.com/repos/{self.repo}/releases/latest"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": f"{APP_NAME}/{APP_VERSION}",
            },
        )
        try:
            with _urlopen_with_ssl_fallback(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            self.finished_check.emit("error", "", "", "")
            return

        tag_name = str(data.get("tag_name", "")).strip()
        if not tag_name:
            self.finished_check.emit("error", "", "", "")
            return

        latest_ver = tag_name.lstrip("vV")
        if parse_version_tuple(latest_ver) <= parse_version_tuple(APP_VERSION):
            self.finished_check.emit("up_to_date", latest_ver, "", "")
            return

        # Find matching platform asset URL
        assets = data.get("assets", [])
        download_url = ""
        if sys.platform == "win32":
            for asset in assets:
                name = str(asset.get("name", "")).lower()
                if name.endswith(".exe"):
                    download_url = str(asset.get("browser_download_url", ""))
                    break
        elif sys.platform == "darwin":
            for asset in assets:
                name = str(asset.get("name", "")).lower()
                if "macos" in name or name.endswith(".zip") or name.endswith(".dmg"):
                    download_url = str(asset.get("browser_download_url", ""))
                    break

        # Fallback to raw script URL if running from source or no binary asset attached
        if not download_url:
            download_url = (
                f"https://raw.githubusercontent.com/{self.repo}/{tag_name}/pickhex.py"
            )

        body = str(data.get("body", "") or "")
        self.finished_check.emit("update_available", latest_ver, download_url, body)


class DownloadUpdateWorker(QThread):
    progress = pyqtSignal(int)
    completed = pyqtSignal(bool, str)  # (success, downloaded_file_path)

    def __init__(self, download_url: str, target_path: Path) -> None:
        super().__init__()
        self.download_url = download_url
        self.target_path = target_path

    def run(self) -> None:
        req = urllib.request.Request(
            self.download_url,
            headers={"User-Agent": f"{APP_NAME}/{APP_VERSION}"},
        )
        try:
            with _urlopen_with_ssl_fallback(req, timeout=30) as resp:
                total = int(resp.headers.get("Content-Length", 0) or 0)
                downloaded = 0
                chunk_size = 65536
                with self.target_path.open("wb") as out:
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        out.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = min(100, int((downloaded * 100) / total))
                            self.progress.emit(pct)
            self.progress.emit(100)
            self.completed.emit(True, str(self.target_path))
        except Exception as e:
            self.completed.emit(False, str(e))


class UpdateDialog(QDialog):
    def __init__(
        self,
        lang: str,
        latest_ver: str,
        download_url: str,
    ) -> None:
        super().__init__()
        self.lang = lang
        self.latest_ver = latest_ver
        self.download_url = download_url
        self.dl_worker: Optional[DownloadUpdateWorker] = None

        t = TRANSLATIONS[self.lang]
        self.setWindowTitle(t["upd_title"])
        self.setWindowIcon(create_app_icon(64))
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(420, 240)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #181822;
                color: #F2F4F8;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
            QLabel#title {
                font-size: 17px;
                font-weight: 700;
                color: #FFFFFF;
            }
            QLabel#notes {
                font-size: 12px;
                color: #B4B9C8;
            }
            QProgressBar {
                border: 1px solid #34374C;
                border-radius: 6px;
                background-color: #232433;
                text-align: center;
                color: #FFFFFF;
                font-size: 11px;
                font-weight: 600;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #6366F1;
                border-radius: 5px;
            }
            QPushButton#updateBtn {
                background-color: #6366F1;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 700;
                padding: 10px 16px;
            }
            QPushButton#updateBtn:hover {
                background-color: #4F46E5;
            }
            QPushButton#laterBtn {
                background-color: #232433;
                border: 1px solid #34374C;
                border-radius: 8px;
                color: #B4B9C8;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 16px;
            }
            QPushButton#laterBtn:hover {
                background-color: #2C2E42;
                color: #FFFFFF;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel(
            "🚀 " + t["upd_found"].format(latest=latest_ver, current=APP_VERSION)
        )
        title.setObjectName("title")
        layout.addWidget(title)

        self.notes_lbl = QLabel(t["upd_notes"])
        self.notes_lbl.setObjectName("notes")
        self.notes_lbl.setWordWrap(True)
        layout.addWidget(self.notes_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_later = QPushButton(t["upd_btn_later"])
        self.btn_later.setObjectName("laterBtn")
        self.btn_later.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_later.clicked.connect(self.reject)

        self.btn_now = QPushButton(t["upd_btn_now"])
        self.btn_now.setObjectName("updateBtn")
        self.btn_now.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_now.clicked.connect(self._start_download)

        btn_row.addWidget(self.btn_later)
        btn_row.addWidget(self.btn_now, stretch=1)
        layout.addLayout(btn_row)

    def _start_download(self) -> None:
        self.btn_now.setEnabled(False)
        self.btn_later.setEnabled(False)
        self.progress_bar.show()

        if getattr(sys, "frozen", False) and sys.platform == "win32":
            target = Path(sys.executable + ".new")
        elif getattr(sys, "frozen", False) and sys.platform == "darwin":
            target = Path(tempfile.gettempdir()) / "PickHex-update.zip"
        else:
            target = Path(__file__).resolve().with_suffix(".py.new")

        self.dl_worker = DownloadUpdateWorker(self.download_url, target)
        self.dl_worker.progress.connect(self._on_progress)
        self.dl_worker.completed.connect(self._on_download_completed)
        self.dl_worker.start()

    def _on_progress(self, pct: int) -> None:
        t = TRANSLATIONS[self.lang]
        self.progress_bar.setValue(pct)
        self.notes_lbl.setText(t["upd_downloading"].format(pct=pct))

    def _on_download_completed(self, success: bool, path_or_err: str) -> None:
        t = TRANSLATIONS[self.lang]
        if not success:
            self.notes_lbl.setText(t["toast_update_error"])
            self.btn_later.setEnabled(True)
            return

        self.notes_lbl.setText(t["upd_installing"])
        downloaded_path = Path(path_or_err)
        self._apply_update_and_restart(downloaded_path)

    def _apply_update_and_restart(self, downloaded_path: Path) -> None:
        try:
            if getattr(sys, "frozen", False) and sys.platform == "win32":
                current_exe = Path(sys.executable)
                old_exe = Path(sys.executable + ".old")
                if old_exe.exists():
                    try:
                        old_exe.unlink()
                    except Exception:
                        pass
                # Windows allows renaming the currently running .exe!
                current_exe.rename(old_exe)
                downloaded_path.rename(current_exe)
                subprocess.Popen([str(current_exe)], close_fds=True)
                QApplication.quit()
                os._exit(0)

            elif getattr(sys, "frozen", False) and sys.platform == "darwin":
                # Extract PickHex.app and replace current bundle
                extract_dir = Path(tempfile.gettempdir()) / "pickhex_extracted"
                if extract_dir.exists():
                    shutil.rmtree(extract_dir, ignore_errors=True)
                with zipfile.ZipFile(downloaded_path, "r") as zf:
                    zf.extractall(extract_dir)
                new_app = extract_dir / "PickHex.app"
                # Current executable is inside PickHex.app/Contents/MacOS/PickHex
                current_app = Path(sys.executable).parents[2]
                if new_app.exists() and current_app.suffix == ".app":
                    shutil.rmtree(current_app, ignore_errors=True)
                    shutil.move(str(new_app), str(current_app))
                    subprocess.Popen(["open", "-n", str(current_app)])
                    QApplication.quit()
                    os._exit(0)
            else:
                # Running from Python script
                script_path = Path(__file__).resolve()
                shutil.move(str(downloaded_path), str(script_path))
                subprocess.Popen([sys.executable, str(script_path)], close_fds=True)
                QApplication.quit()
                os._exit(0)
        except Exception:
            self.reject()


# ---------------------------------------------------------------------------
# Auto-Start Helper (Windows Registry & macOS LaunchAgent)
# ---------------------------------------------------------------------------
class StartupManager:
    WIN_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    MAC_PLIST_NAME = "com.pickhex.eyedropper.plist"

    @staticmethod
    def get_executable_command() -> str:
        if getattr(sys, "frozen", False):
            return f'"{sys.executable}"'
        return f'"{sys.executable}" "{Path(__file__).resolve()}"'

    @classmethod
    def is_enabled(cls) -> bool:
        if sys.platform == "win32":
            try:
                import winreg
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, cls.WIN_REG_PATH, 0, winreg.KEY_READ
                ) as key:
                    val, _ = winreg.QueryValueEx(key, APP_NAME)
                    return bool(val)
            except Exception:
                return False
        elif sys.platform == "darwin":
            plist_path = Path.home() / "Library" / "LaunchAgents" / cls.MAC_PLIST_NAME
            return plist_path.exists()
        return False

    @classmethod
    def set_enabled(cls, enable: bool) -> None:
        if sys.platform == "win32":
            try:
                import winreg
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, cls.WIN_REG_PATH, 0, winreg.KEY_SET_VALUE
                ) as key:
                    if enable:
                        winreg.SetValueEx(
                            key, APP_NAME, 0, winreg.REG_SZ, cls.get_executable_command()
                        )
                    else:
                        try:
                            winreg.DeleteValue(key, APP_NAME)
                        except FileNotFoundError:
                            pass
            except Exception:
                pass
        elif sys.platform == "darwin":
            plist_dir = Path.home() / "Library" / "LaunchAgents"
            plist_path = plist_dir / cls.MAC_PLIST_NAME
            try:
                if enable:
                    plist_dir.mkdir(parents=True, exist_ok=True)
                    exe_path = (
                        sys.executable
                        if getattr(sys, "frozen", False)
                        else str(Path(__file__).resolve())
                    )
                    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pickhex.eyedropper</string>
    <key>ProgramArguments</key>
    <array>
        <string>{exe_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
                    plist_path.write_text(plist_content, encoding="utf-8")
                else:
                    if plist_path.exists():
                        plist_path.unlink()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Dynamic Vector Icon Generator (Zero External File Dependencies at Runtime)
# ---------------------------------------------------------------------------
def create_app_icon(size: int = 64) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    pad = size * 0.06
    rect = QRectF(pad, pad, size - 2 * pad, size - 2 * pad)

    painter.setPen(QPen(QColor(75, 82, 105), max(1.5, size * 0.03)))
    painter.setBrush(QColor(24, 24, 34))
    painter.drawRoundedRect(rect, size * 0.24, size * 0.24)

    import math
    cx, cy = size * 0.5, size * 0.5
    ring_r = size * 0.27
    dot_r = size * 0.095
    palette = [
        QColor(255, 75, 92),
        QColor(255, 159, 28),
        QColor(46, 196, 182),
        QColor(58, 134, 255),
        QColor(131, 56, 236),
        QColor(255, 214, 10),
    ]
    painter.setPen(Qt.PenStyle.NoPen)
    for i, col in enumerate(palette):
        angle = (i / len(palette)) * 2 * math.pi - math.pi / 2
        px = cx + math.cos(angle) * ring_r
        py = cy + math.sin(angle) * ring_r
        painter.setBrush(col)
        painter.drawEllipse(QPointF(px, py), dot_r, dot_r)

    painter.setBrush(QColor(255, 255, 255))
    painter.drawEllipse(QPointF(cx, cy), size * 0.135, size * 0.135)
    painter.setBrush(QColor(24, 24, 34))
    painter.drawEllipse(QPointF(cx, cy), size * 0.06, size * 0.06)

    painter.end()
    return QIcon(pixmap)


def create_color_swatch_icon(hex_color: str, size: int = 16) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setPen(QPen(QColor(255, 255, 255, 160), 1))
    painter.setBrush(QColor(hex_color))
    painter.drawRoundedRect(QRectF(1, 1, size - 2, size - 2), 3, 3)
    painter.end()
    return QIcon(pixmap)


# ---------------------------------------------------------------------------
# First-Run Language Selection Dialog
# ---------------------------------------------------------------------------
class LanguageSetupDialog(QDialog):
    def __init__(self, initial_lang: str = "tr") -> None:
        super().__init__()
        self.selected_lang = initial_lang
        self.setWindowTitle("PickHex — Setup / Kurulum")
        self.setWindowIcon(create_app_icon(64))
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(400, 270)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #181822;
                color: #F2F4F8;
                font-family: 'Segoe UI', -apple-system, sans-serif;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 700;
                color: #FFFFFF;
            }
            QLabel#subtitle {
                font-size: 13px;
                color: #B4B9C8;
            }
            QLabel#note {
                font-size: 11px;
                color: #7E859A;
            }
            QPushButton.langBtn {
                background-color: #232433;
                border: 2px solid #34374C;
                border-radius: 8px;
                color: #E2E6F0;
                font-size: 14px;
                font-weight: 600;
                padding: 12px 16px;
            }
            QPushButton.langBtn:hover {
                border-color: #5661F6;
                background-color: #292B3E;
            }
            QPushButton.langBtn[selected="true"] {
                background-color: #2E335A;
                border: 2px solid #6366F1;
                color: #FFFFFF;
            }
            QPushButton#confirmBtn {
                background-color: #6366F1;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 700;
                padding: 10px;
            }
            QPushButton#confirmBtn:hover {
                background-color: #4F46E5;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("🎨 PickHex")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Lütfen uygulama dilini seçin\nPlease select your application language"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.btn_tr = QPushButton("🇹🇷  Türkçe")
        self.btn_tr.setProperty("class", "langBtn")
        self.btn_tr.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tr.clicked.connect(lambda: self._select("tr"))

        self.btn_en = QPushButton("🇬🇧  English")
        self.btn_en.setProperty("class", "langBtn")
        self.btn_en.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_en.clicked.connect(lambda: self._select("en"))

        btn_row.addWidget(self.btn_tr)
        btn_row.addWidget(self.btn_en)
        layout.addLayout(btn_row)

        self.note_lbl = QLabel()
        self.note_lbl.setObjectName("note")
        self.note_lbl.setWordWrap(True)
        self.note_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.note_lbl)

        self.btn_confirm = QPushButton("Başla / Start")
        self.btn_confirm.setObjectName("confirmBtn")
        self.btn_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_confirm.clicked.connect(self.accept)
        layout.addWidget(self.btn_confirm)

        self._select(initial_lang)

    def _select(self, lang: str) -> None:
        self.selected_lang = lang
        self.btn_tr.setProperty("selected", "true" if lang == "tr" else "false")
        self.btn_en.setProperty("selected", "true" if lang == "en" else "false")
        self.btn_tr.style().unpolish(self.btn_tr)
        self.btn_tr.style().polish(self.btn_tr)
        self.btn_en.style().unpolish(self.btn_en)
        self.btn_en.style().polish(self.btn_en)

        if lang == "tr":
            self.note_lbl.setText(TRANSLATIONS["tr"]["welcome_note"])
            self.btn_confirm.setText("Kaydet ve Başla")
        else:
            self.note_lbl.setText(TRANSLATIONS["en"]["welcome_note"])
            self.btn_confirm.setText("Save & Start")


# ---------------------------------------------------------------------------
# On-Screen Toast Notification (Crisp, No Animation Lag)
# ---------------------------------------------------------------------------
class ToastNotification(QWidget):
    def __init__(self) -> None:
        super().__init__(None)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
            | Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        self._message = ""
        self._swatch_color: Optional[QColor] = None
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_toast(
        self,
        message: str,
        hex_color: Optional[str] = None,
        duration_ms: int = 2000,
    ) -> None:
        self._message = message
        self._swatch_color = QColor(hex_color) if hex_color else None

        font = QFont("Segoe UI", 11, QFont.Weight.DemiBold)
        self.setFont(font)
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(self._message)

        swatch_space = 30 if self._swatch_color else 0
        width = max(240, text_width + swatch_space + 48)
        height = 48
        self.setFixedSize(width, height)

        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos) or QGuiApplication.primaryScreen()
        if screen:
            avail = screen.availableGeometry()
            x = avail.x() + (avail.width() - width) // 2
            y = avail.y() + avail.height() - height - 48
            self.move(x, y)

        self.show()
        self.raise_()
        self.update()
        self._timer.start(duration_ms)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = QRectF(1.5, 1.5, self.width() - 3, self.height() - 3)

        painter.setPen(QPen(QColor(255, 255, 255, 45), 1.5))
        painter.setBrush(QColor(20, 21, 30, 242))
        painter.drawRoundedRect(rect, 12, 12)

        text_x = 20
        if self._swatch_color:
            swatch_rect = QRectF(16, (self.height() - 22) / 2, 22, 22)
            painter.setPen(QPen(QColor(255, 255, 255, 200), 1.5))
            painter.setBrush(self._swatch_color)
            painter.drawRoundedRect(swatch_rect, 6, 6)
            text_x = 48

        painter.setPen(QColor(248, 250, 252))
        text_rect = QRectF(text_x, 0, self.width() - text_x - 16, self.height())
        painter.drawText(
            text_rect,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            self._message,
        )
        painter.end()


# ---------------------------------------------------------------------------
# Full-Screen Eyedropper Overlay with Interactive Magnifier Controls
# ---------------------------------------------------------------------------
class EyedropperOverlay(QWidget):
    LENS_PIXEL_SIZE = 132

    def __init__(
        self,
        config: ConfigManager,
        on_color_picked,
        on_cancelled,
        on_format_changed,
    ) -> None:
        super().__init__(None)
        self.config = config
        self.on_color_picked = on_color_picked
        self.on_cancelled = on_cancelled
        self.on_format_changed = on_format_changed

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.screen_captures: List[tuple[QScreen, QRect, QPixmap, QImage]] = []
        self.virtual_rect = QRect()
        self.current_pos = QPoint(0, 0)
        self.current_color = QColor(255, 255, 255)

    def start_picking(self) -> None:
        self.screen_captures.clear()

        screens = QGuiApplication.screens()
        if not screens:
            return

        combined = screens[0].geometry()
        for s in screens:
            combined = combined.united(s.geometry())
            pix = s.grabWindow(0)
            img = pix.toImage()
            self.screen_captures.append((s, s.geometry(), pix, img))

        self.virtual_rect = combined
        self.setGeometry(self.virtual_rect)

        self.current_pos = QCursor.pos()
        self.current_color = self._sample_pixel(self.current_pos)

        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.update()

    def _sample_pixel(self, global_pos: QPoint) -> QColor:
        for _screen, geom, _pix, img in self.screen_captures:
            if geom.contains(global_pos):
                dpr = img.devicePixelRatio()
                rx = int((global_pos.x() - geom.x()) * dpr)
                ry = int((global_pos.y() - geom.y()) * dpr)
                rx = max(0, min(img.width() - 1, rx))
                ry = max(0, min(img.height() - 1, ry))
                return img.pixelColor(rx, ry)
        return QColor(0, 0, 0)

    def _sample_grid_pixel(self, global_pos: QPoint, dx: int, dy: int) -> QColor:
        for _screen, geom, _pix, img in self.screen_captures:
            if geom.contains(global_pos):
                dpr = img.devicePixelRatio()
                rx = int((global_pos.x() - geom.x()) * dpr) + dx
                ry = int((global_pos.y() - geom.y()) * dpr) + dy
                if 0 <= rx < img.width() and 0 <= ry < img.height():
                    return img.pixelColor(rx, ry)
        return QColor(20, 20, 20)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.current_pos = event.globalPosition().toPoint()
        self.current_color = self._sample_pixel(self.current_pos)
        self.update()

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        if delta > 0:
            self.config.grid_radius = max(3, self.config.grid_radius - 1)
        elif delta < 0:
            self.config.grid_radius = min(9, self.config.grid_radius + 1)
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.globalPosition().toPoint()
            picked_color = self._sample_pixel(pos)
            self.hide()
            self.on_color_picked(picked_color)
        elif event.button() == Qt.MouseButton.RightButton:
            self.hide()
            self.on_cancelled()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.hide()
            self.on_cancelled()
            return

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            picked_color = self._sample_pixel(self.current_pos)
            self.hide()
            self.on_color_picked(picked_color)
            return

        if key == Qt.Key.Key_Tab:
            idx = SUPPORTED_FORMATS.index(self.config.color_format)
            next_fmt = SUPPORTED_FORMATS[(idx + 1) % len(SUPPORTED_FORMATS)]
            self.config.color_format = next_fmt
            self.on_format_changed()
            self.update()
            return

        nudge = QPoint(0, 0)
        if key == Qt.Key.Key_Left:
            nudge = QPoint(-1, 0)
        elif key == Qt.Key.Key_Right:
            nudge = QPoint(1, 0)
        elif key == Qt.Key.Key_Up:
            nudge = QPoint(0, -1)
        elif key == Qt.Key.Key_Down:
            nudge = QPoint(0, 1)

        if not nudge.isNull():
            new_pos = self.current_pos + nudge
            QCursor.setPos(new_pos)
            self.current_pos = new_pos
            self.current_color = self._sample_pixel(self.current_pos)
            self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        for _screen, geom, pix, _img in self.screen_captures:
            local_top_left = geom.topLeft() - self.virtual_rect.topLeft()
            painter.drawPixmap(local_top_left, pix)

        cursor_local = self.current_pos - self.virtual_rect.topLeft()

        grid_radius = self.config.grid_radius
        grid_count = grid_radius * 2 + 1
        cell_size = self.LENS_PIXEL_SIZE / grid_count
        lens_size = self.LENS_PIXEL_SIZE

        card_width = 210
        card_height = lens_size + 94

        offset_x = 24
        offset_y = 24
        if cursor_local.x() + offset_x + card_width > self.width() - 12:
            offset_x = -card_width - 24
        if cursor_local.y() + offset_y + card_height > self.height() - 12:
            offset_y = -card_height - 24

        card_x = cursor_local.x() + offset_x
        card_y = cursor_local.y() + offset_y
        card_rect = QRectF(card_x, card_y, card_width, card_height)

        painter.setPen(QPen(QColor(255, 255, 255, 65), 1.5))
        painter.setBrush(QColor(18, 19, 28, 244))
        painter.drawRoundedRect(card_rect, 12, 12)

        lens_x = card_x + (card_width - lens_size) / 2
        lens_y = card_y + 12
        lens_rect = QRectF(lens_x, lens_y, lens_size, lens_size)

        clip_path = QPainterPath()
        clip_path.addRoundedRect(lens_rect, 8, 8)
        painter.save()
        painter.setClipPath(clip_path)

        for gy in range(-grid_radius, grid_radius + 1):
            for gx in range(-grid_radius, grid_radius + 1):
                pcol = self._sample_grid_pixel(self.current_pos, gx, gy)
                cell_x = lens_x + (gx + grid_radius) * cell_size
                cell_y = lens_y + (gy + grid_radius) * cell_size
                cell_rect = QRectF(cell_x, cell_y, cell_size + 0.5, cell_size + 0.5)
                painter.fillRect(cell_rect, pcol)
                if grid_radius <= 6:
                    painter.setPen(QPen(QColor(255, 255, 255, 22), 0.5))
                    painter.drawRect(cell_rect)

        painter.restore()

        painter.setPen(QPen(QColor(255, 255, 255, 130), 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(lens_rect, 8, 8)

        zoom_mult = 12 - grid_radius
        badge_rect = QRectF(lens_x + lens_size - 34, lens_y + 5, 29, 16)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(15, 16, 24, 200))
        painter.drawRoundedRect(badge_rect, 4, 4)
        painter.setPen(QColor(210, 215, 230))
        painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, f"{zoom_mult}x")

        center_x = lens_x + grid_radius * cell_size
        center_y = lens_y + grid_radius * cell_size
        center_rect = QRectF(center_x, center_y, cell_size, cell_size)
        painter.setPen(QPen(QColor(0, 0, 0, 230), 2.0))
        painter.drawRect(center_rect.adjusted(-1, -1, 1, 1))
        painter.setPen(QPen(QColor(255, 255, 255, 255), 1.5))
        painter.drawRect(center_rect)

        info_y = lens_y + lens_size + 10
        swatch_rect = QRectF(card_x + 12, info_y + 2, 24, 24)
        painter.setPen(QPen(QColor(255, 255, 255, 190), 1.2))
        painter.setBrush(self.current_color)
        painter.drawRoundedRect(swatch_rect, 6, 6)

        active_fmt = self.config.color_format
        formatted_preview = format_qcolor(self.current_color, active_fmt)

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        painter.drawText(
            QRectF(card_x + 42, info_y - 2, card_width - 50, 18),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            formatted_preview,
        )

        r, g, b = (
            self.current_color.red(),
            self.current_color.green(),
            self.current_color.blue(),
        )
        sub_line = f"[{active_fmt}]  RGB({r}, {g}, {b})"
        painter.setPen(QColor(165, 174, 196))
        painter.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
        painter.drawText(
            QRectF(card_x + 42, info_y + 15, card_width - 50, 15),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            sub_line,
        )

        hint_y = info_y + 36
        painter.setPen(QPen(QColor(255, 255, 255, 25), 1))
        painter.drawLine(
            QPointF(card_x + 10, hint_y), QPointF(card_x + card_width - 10, hint_y)
        )
        painter.setPen(QColor(135, 144, 165))
        painter.setFont(QFont("Segoe UI", 7))
        hint_text = TRANSLATIONS[self.config.lang]["hud_controls"]
        painter.drawText(
            QRectF(card_x + 6, hint_y + 3, card_width - 12, 18),
            Qt.AlignmentFlag.AlignCenter,
            hint_text,
        )

        painter.end()


# ---------------------------------------------------------------------------
# Main System Tray Controller
# ---------------------------------------------------------------------------
class PickHexTrayApp:
    def __init__(self, app: QApplication, force_setup: bool = False) -> None:
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)
        cleanup_old_update_artifacts()
        self.config = ConfigManager()
        self.update_worker: Optional[ReleaseCheckWorker] = None

        if self.config.is_first_run or force_setup:
            dlg = LanguageSetupDialog(initial_lang=self.config.lang)
            dlg.exec()
            self.config.lang = dlg.selected_lang

        self.toast = ToastNotification()
        self.overlay = EyedropperOverlay(
            config=self.config,
            on_color_picked=self.handle_color_picked,
            on_cancelled=lambda: None,
            on_format_changed=self.rebuild_menu,
        )

        self.server = QLocalServer()
        QLocalServer.removeServer(SINGLE_INSTANCE_KEY)
        if self.server.listen(SINGLE_INSTANCE_KEY):
            self.server.newConnection.connect(self._on_second_instance_message)

        self.tray = QSystemTrayIcon(create_app_icon(64), self.app)
        self.tray.activated.connect(self._on_tray_activated)
        self.menu = QMenu()
        self._apply_menu_style()
        self.rebuild_menu()
        self.tray.setContextMenu(self.menu)
        self.tray.show()

        QTimer.singleShot(400, self._show_startup_toast)

    def t(self, key: str) -> str:
        return TRANSLATIONS[self.config.lang].get(key, key)

    def _apply_menu_style(self) -> None:
        self.menu.setStyleSheet(
            """
            QMenu {
                background-color: #1B1C28;
                color: #F1F5F9;
                border: 1px solid #33364D;
                border-radius: 8px;
                padding: 6px 4px;
                font-family: 'Segoe UI', -apple-system, sans-serif;
                font-size: 12px;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
                border-radius: 5px;
                margin: 1px 4px;
            }
            QMenu::item:selected {
                background-color: #6366F1;
                color: #FFFFFF;
            }
            QMenu::separator {
                height: 1px;
                background: #2E3146;
                margin: 5px 8px;
            }
            """
        )

    def rebuild_menu(self) -> None:
        self.menu.clear()
        self.tray.setToolTip(self.t("tray_tooltip").format(ver=APP_VERSION))

        # 1. Pick Color Action
        act_pick = QAction(self.t("menu_pick"), self.menu)
        font = act_pick.font()
        font.setBold(True)
        act_pick.setFont(font)
        act_pick.triggered.connect(self.trigger_eyedropper)
        self.menu.addAction(act_pick)

        self.menu.addSeparator()

        # 2. Recent Colors Submenu
        recent_menu = self.menu.addMenu(self.t("menu_recent"))
        recent_list = self.config.recent_colors
        if not recent_list:
            empty_act = QAction(self.t("menu_no_recent"), recent_menu)
            empty_act.setEnabled(False)
            recent_menu.addAction(empty_act)
        else:
            for hex_code in recent_list:
                qcol = QColor(hex_code)
                default_formatted = format_qcolor(qcol, self.config.color_format)

                color_submenu = recent_menu.addMenu(
                    create_color_swatch_icon(hex_code),
                    f"{hex_code}   ({default_formatted})",
                )

                quick_act = QAction(
                    self.t("menu_copy_default").format(code=default_formatted),
                    color_submenu,
                )
                qfont = quick_act.font()
                qfont.setBold(True)
                quick_act.setFont(qfont)
                quick_act.triggered.connect(
                    lambda checked=False, c=default_formatted, h=hex_code: self.copy_formatted_string(
                        c, h
                    )
                )
                color_submenu.addAction(quick_act)

                color_submenu.addSeparator()

                as_fmt_menu = color_submenu.addMenu(self.t("menu_copy_formats"))
                for fmt_key in SUPPORTED_FORMATS:
                    val_str = format_qcolor(qcol, fmt_key)
                    f_act = QAction(f"{fmt_key}:  {val_str}", as_fmt_menu)
                    f_act.triggered.connect(
                        lambda checked=False, c=val_str, h=hex_code: self.copy_formatted_string(
                            c, h
                        )
                    )
                    as_fmt_menu.addAction(f_act)

                shades_menu = color_submenu.addMenu(self.t("menu_shades_tints"))
                for kind, pct, s_hex in generate_shades_and_tints(hex_code):
                    s_formatted = format_qcolor(QColor(s_hex), self.config.color_format)
                    if kind == "lighter":
                        label = self.t("shade_lighter").format(pct=pct, hex=s_formatted)
                    elif kind == "base":
                        label = self.t("shade_base").format(hex=s_formatted)
                    elif kind == "darker":
                        label = self.t("shade_darker").format(pct=pct, hex=s_formatted)
                    else:
                        label = self.t("shade_complement").format(hex=s_formatted)

                    s_act = QAction(
                        create_color_swatch_icon(s_hex), label, shades_menu
                    )
                    s_act.triggered.connect(
                        lambda checked=False, c=s_formatted, h=s_hex: self.copy_formatted_string(
                            c, h
                        )
                    )
                    shades_menu.addAction(s_act)

            recent_menu.addSeparator()
            clear_act = QAction(self.t("menu_clear_recent"), recent_menu)
            clear_act.triggered.connect(self._clear_recent)
            recent_menu.addAction(clear_act)

        # 3. Default Copy Format Submenu
        fmt_menu = self.menu.addMenu(self.t("menu_format"))
        fmt_group = QActionGroup(fmt_menu)
        fmt_group.setExclusive(True)
        for fmt_label, fmt_val in [
            ("HEX  (#FF5733)", "HEX"),
            ("HEX Raw  (FF5733)", "HEX_RAW"),
            ("RGB  (rgb(255, 87, 51))", "RGB"),
            ("HSL  (hsl(11, 100%, 60%))", "HSL"),
            ("CSS  (color: #FF5733;)", "CSS"),
            ("Tailwind  (bg-[#FF5733])", "TAILWIND"),
        ]:
            f_act = QAction(fmt_label, fmt_menu)
            f_act.setCheckable(True)
            f_act.setChecked(self.config.color_format == fmt_val)
            f_act.triggered.connect(
                lambda checked=False, v=fmt_val: self._set_format(v)
            )
            fmt_group.addAction(f_act)
            fmt_menu.addAction(f_act)

        # 4. Language Submenu
        lang_menu = self.menu.addMenu(self.t("menu_lang"))
        lang_group = QActionGroup(lang_menu)
        lang_group.setExclusive(True)
        for l_label, l_code in [("🇹🇷  Türkçe", "tr"), ("🇬🇧  English", "en")]:
            l_act = QAction(l_label, lang_menu)
            l_act.setCheckable(True)
            l_act.setChecked(self.config.lang == l_code)
            l_act.triggered.connect(
                lambda checked=False, c=l_code: self._set_language(c)
            )
            lang_group.addAction(l_act)
            lang_menu.addAction(l_act)

        # 5. Run on Startup Toggle
        startup_act = QAction(self.t("menu_startup"), self.menu)
        startup_act.setCheckable(True)
        startup_act.setChecked(StartupManager.is_enabled())
        startup_act.triggered.connect(self._toggle_startup)
        self.menu.addAction(startup_act)

        # 6. Check for Updates
        update_act = QAction(
            self.t("menu_update").format(ver=APP_VERSION), self.menu
        )
        update_act.triggered.connect(self.check_for_updates)
        self.menu.addAction(update_act)

        self.menu.addSeparator()

        # 7. Quit
        quit_act = QAction(self.t("menu_quit"), self.menu)
        quit_act.triggered.connect(self.app.quit)
        self.menu.addAction(quit_act)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            QTimer.singleShot(80, self.trigger_eyedropper)

    def trigger_eyedropper(self) -> None:
        self.overlay.start_picking()

    def handle_color_picked(self, color: QColor) -> None:
        hex_code = color.name().upper()
        formatted = format_qcolor(color, self.config.color_format)

        clipboard = QGuiApplication.clipboard()
        if clipboard:
            clipboard.setText(formatted)

        self.config.add_recent_color(hex_code)
        self.rebuild_menu()

        msg = self.t("toast_copied").format(code=formatted)
        self.toast.show_toast(msg, hex_color=hex_code, duration_ms=2000)

    def copy_formatted_string(self, formatted_str: str, swatch_hex: str) -> None:
        clipboard = QGuiApplication.clipboard()
        if clipboard:
            clipboard.setText(formatted_str)
        msg = self.t("toast_copied").format(code=formatted_str)
        self.toast.show_toast(msg, hex_color=swatch_hex, duration_ms=2000)

    def check_for_updates(self) -> None:
        if self.update_worker and self.update_worker.isRunning():
            return
        self.toast.show_toast(
            self.t("toast_checking_update"), hex_color="#6366F1", duration_ms=1600
        )
        self.update_worker = ReleaseCheckWorker(self.config.github_repo)
        self.update_worker.finished_check.connect(self._on_update_check_finished)
        self.update_worker.start()

    def _on_update_check_finished(
        self, status: str, latest_ver: str, download_url: str, _body: str
    ) -> None:
        if status == "up_to_date":
            self.toast.show_toast(
                self.t("toast_up_to_date").format(ver=APP_VERSION),
                hex_color="#2EC4B6",
                duration_ms=2400,
            )
        elif status == "update_available":
            dlg = UpdateDialog(
                lang=self.config.lang,
                latest_ver=latest_ver,
                download_url=download_url,
            )
            dlg.exec()
        else:
            self.toast.show_toast(
                self.t("toast_update_error"),
                hex_color="#FF9F1C",
                duration_ms=2600,
            )

    def _clear_recent(self) -> None:
        self.config.clear_recent_colors()
        self.rebuild_menu()

    def _set_format(self, fmt: str) -> None:
        self.config.color_format = fmt
        self.rebuild_menu()

    def _set_language(self, lang_code: str) -> None:
        self.config.lang = lang_code
        self.rebuild_menu()

    def _toggle_startup(self, checked: bool) -> None:
        StartupManager.set_enabled(checked)
        self.rebuild_menu()

    def _show_startup_toast(self) -> None:
        key = "toast_running_mac" if sys.platform == "darwin" else "toast_running_win"
        self.toast.show_toast(self.t(key), hex_color="#6366F1", duration_ms=2800)

    def _on_second_instance_message(self) -> None:
        conn = self.server.nextPendingConnection()
        if conn:
            conn.waitForReadyRead(200)
            conn.close()
        QTimer.singleShot(100, self.trigger_eyedropper)


def notify_existing_instance() -> bool:
    socket = QLocalSocket()
    socket.connectToServer(SINGLE_INSTANCE_KEY)
    if socket.waitForConnected(250):
        socket.write(b"PICK")
        socket.waitForBytesWritten(200)
        socket.disconnectFromServer()
        return True
    return False


def main() -> None:
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    if sys.platform == "darwin":
        try:
            app.setQuitOnLastWindowClosed(False)
        except Exception:
            pass

    force_setup = "--setup" in sys.argv
    if not force_setup and notify_existing_instance():
        sys.exit(0)

    _controller = PickHexTrayApp(app, force_setup=force_setup)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
