"""
Cross-platform build script for PickHex (Windows .exe & macOS .app).
Usage:
    python build.py
"""
import plistlib
import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = Path(__file__).parent.resolve()
    assets_dir = root / "assets"

    # 1. Ensure icons exist
    subprocess.run([sys.executable, str(root / "generate_icon.py")], check=True)

    exclude_modules = [
        "PyQt6.QtQuick",
        "PyQt6.QtQml",
        "PyQt6.QtSql",
        "PyQt6.QtTest",
        "PyQt6.QtXml",
        "PyQt6.QtDBus",
        "PyQt6.QtDesigner",
        "PyQt6.QtHelp",
        "PyQt6.QtMultimedia",
        "PyQt6.QtMultimediaWidgets",
        "PyQt6.QtOpenGL",
        "PyQt6.QtOpenGLWidgets",
        "PyQt6.QtPdf",
        "PyQt6.QtPdfWidgets",
        "PyQt6.QtPositioning",
        "PyQt6.QtPrintSupport",
        "PyQt6.QtRemoteObjects",
        "PyQt6.QtSensors",
        "PyQt6.QtSerialPort",
        "PyQt6.QtSpatialAudio",
        "PyQt6.QtStateMachine",
        "PyQt6.QtSvg",
        "PyQt6.QtSvgWidgets",
        "PyQt6.QtTextToSpeech",
        "PyQt6.QtWebChannel",
        "PyQt6.QtWebSockets",
        "PIL",
        "tkinter",
        "unittest",
    ]

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name=PickHex",
        "--windowed",
    ]

    for mod in exclude_modules:
        cmd.extend(["--exclude-module", mod])

    if sys.platform == "win32":
        cmd.append("--onefile")
        ico_file = assets_dir / "icon.ico"
        if ico_file.exists():
            cmd.append(f"--icon={ico_file}")
    elif sys.platform == "darwin":
        cmd.extend(["--osx-bundle-identifier", "com.pickhex.eyedropper"])
        icns_file = assets_dir / "icon.icns"
        if icns_file.exists():
            cmd.append(f"--icon={icns_file}")
    else:
        cmd.append("--onefile")

    cmd.append(str(root / "pickhex.py"))

    print("Building PickHex executable...")
    subprocess.run(cmd, cwd=str(root), check=True)

    # On macOS, mark Info.plist with LSUIElement=True so it runs exclusively
    # in the top Menu Bar without showing a Dock icon.
    if sys.platform == "darwin":
        plist_path = root / "dist" / "PickHex.app" / "Contents" / "Info.plist"
        if plist_path.exists():
            with plist_path.open("rb") as f:
                plist_data = plistlib.load(f)
            plist_data["LSUIElement"] = True
            plist_data["NSHighResolutionCapable"] = True
            with plist_path.open("wb") as f:
                plistlib.dump(plist_data, f)
            print("Configured macOS Info.plist with LSUIElement=True (Menu Bar mode).")

    print("\nBuild complete! Output is located in:", root / "dist")


if __name__ == "__main__":
    main()
