# 🎨 PickHex — Free & Open-Source System Tray / Menu Bar Color Picker

[![Latest Release](https://img.shields.io/github/v/release/murrer33/PickHex?label=Download%20Latest&style=for-the-badge&color=6366F1)](https://github.com/murrer33/PickHex/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-2EC4B6?style=for-the-badge)](https://github.com/murrer33/PickHex/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-FF9F1C?style=for-the-badge)](https://opensource.org/licenses/MIT)

**PickHex** is a fast, lightweight, zero-bloat color picker (eyedropper) that lives quietly in your **Windows System Tray (Hidden Icons)** and **macOS Menu Bar**. Click the icon, click any pixel on your screen, and the color code (`HEX`, `RGB`, `HSL`, `CSS`, or `Tailwind`) is instantly copied to your clipboard.

> 💡 **Why PickHex?** Many menu-bar color pickers cost $8+ or only support macOS. **PickHex** is 100% free, open-source, cross-platform (**Windows & macOS**), and built for speed with a zero-UI workflow.

---

## 📥 Download & Installation

### 🍎 macOS (Recommended — Zero Gatekeeper Popups)

**Option A — Via Homebrew (`brew`):**
Automatically installs `PickHex.app` to `/Applications` and clears macOS quarantine so it opens with zero security warnings:
```bash
brew tap murrer33/pickhex https://github.com/murrer33/PickHex
brew install --cask pickhex
```

**Option B — 1-Line Quick Installer (No Homebrew required):**
Paste into **Terminal** to install directly into `/Applications` and launch immediately without any Gatekeeper popup:
```bash
curl -fsSL https://raw.githubusercontent.com/murrer33/PickHex/main/install-mac.sh | bash
```

**Option C — Direct `.zip` Download:**
* Download **[`PickHex-macOS.zip`](https://github.com/murrer33/PickHex/releases/latest/download/PickHex-macOS.zip)**
* *(If macOS shows an unverified developer prompt on first launch: open **System Settings → Privacy & Security → Open Anyway**).*

---

### 🪟 Windows

* Download **[`PickHex.exe`](https://github.com/murrer33/PickHex/releases/latest/download/PickHex.exe)** (Single-file portable executable — no installation needed)

---

## ✨ Features

* **🚀 One-Click Instant Eyedropper:**
  * **Windows:** Left-click the **PickHex** icon in your System Tray (*Hidden Icons*) to immediately launch the live screen magnifier.
  * **macOS:** Click the **PickHex** icon in the top Menu Bar and select **"Pick Color from Screen"**.
* **🔍 Interactive Magnifier Controls (Zero-UI):**
  * **Mouse Scroll Wheel:** Dynamically adjust the magnifier zoom level (`3x` to `9x`) in real time.
  * **Arrow Keys (`↑` `↓` `←` `→`):** Nudge the cursor by **1 exact pixel** to effortlessly capture thin borders and text.
  * **`Tab` Key:** Cycle through copy formats (`HEX` → `HEX_RAW` → `RGB` → `HSL` → `CSS` → `TAILWIND`) live inside the magnifier HUD.
* **🎨 Instant Shades, Tints & Harmonies:**
  * Hover over any color under **Recent Colors** in the right-click menu to instantly copy **3 Lighter Tints (`+20%`, `+40%`, `+60%`)**, **3 Darker Shades (`-20%`, `-40%`, `-60%`)**, or its **Complementary Color** without opening a single window.
* **📋 6 Developer Copy Formats:**
  * `HEX` (`#FF5733`)
  * `HEX Raw` (`FF5733`)
  * `RGB` (`rgb(255, 87, 51)`)
  * `HSL` (`hsl(11, 100%, 60%)`)
  * `CSS` (`color: #FF5733;`)
  * `Tailwind` (`bg-[#FF5733]`)
* **🔔 Crisp On-Screen Toast Notification:** Displays a brief, non-intrusive pill notification with a live color swatch confirming the copied code.
* **🔄 Built-in Self-Updater:** Click **"Check for Updates"** in the tray menu to automatically download and install new releases in-place—no manual uninstall or reinstall needed.
* **🌍 Multi-Language Support (English & Turkish):** Choose your preferred language on first launch or switch anytime from the tray menu.
* **⚡ Run on System Startup:** Optional one-click toggle to launch automatically when you log in.

---

## 🛠️ Running from Source & Building

### Run from Source
```bash
pip install -r requirements.txt
python pickhex.py
```
*(To re-open the first-time language selection dialog, run `python pickhex.py --setup`).*

### Build Standalone Executable (`.exe` / `.app`)
```bash
python build.py
```
* **Windows:** Generates a single-file `dist/PickHex.exe`.
* **macOS:** Generates a native Menu Bar app bundle `dist/PickHex.app` (`LSUIElement=True`).

---

<details>
<summary><b>🇹🇷 Türkçe Açıklama ve Kullanım Kılavuzu (Tıklayın)</b></summary>

<br>

**PickHex**, Windows'ta **Sistem Tepsisinde (Hidden Icons)** ve macOS'ta **Üst Menü Çubuğunda (Menu Bar)** arka planda sessizce çalışan, tek tıkla ekrandaki herhangi bir pikselin rengini anında panoya kopyalayan **%100 ücretsiz ve açık kaynaklı** bir renk seçici (eyedropper) aracıdır.

### Öne Çıkan Özellikler
* **Tek Tıkla Renk Seçimi:** Sağ alttaki *Hidden Icons* içindeki PickHex ikonuna sol tıkladığınız anda ekranda canlı büyüteç açılır, tıkladığınız yerin rengini kopyalar.
* **Akıllı Büyüteç Kontrolleri:** Fare tekerleği ile zoom (`3x`-`9x`) yapabilir, yön tuşlarıyla imleci `1 piksel` kaydırabilir, `Tab` tuşuyla format değiştirebilirsiniz.
* **Penceresiz Ton ve Gölge Üretici:** Sağ tık menüsündeki *Son Seçilen Renkler* altından her rengin açık tonlarını, koyu gölgelerini ve zıt rengini tek tıkla kopyalayabilirsiniz.
* **Otomatik Güncelleme:** Sağ tık menüsündeki *"Güncellemeleri Kontrol Et"* butonu ile eski sürümü silmeye gerek kalmadan tek tıkla güncellenir.

</details>

---

## 📄 License
MIT License — Free forever.
