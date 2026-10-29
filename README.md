# 🎨 PickHex — Free & Open-Source System Tray / Menu Bar Color Picker

**PickHex**, Windows'ta **Sistem Tepsisinde (Hidden Icons)** ve macOS'ta **Üst Menü Çubuğunda (Menu Bar)** arka planda sessizce çalışan, tek tıkla ekrandaki herhangi bir pikselin rengini (`HEX`, `RGB`, `HSL`, `CSS` veya `Tailwind`) anında panoya kopyalayan **%100 ücretsiz ve açık kaynaklı** bir renk seçici (eyedropper) aracıdır.

> 💡 **Why PickHex?** Many menu-bar color pickers are paid ($8+) or limited to macOS only. **PickHex** is 100% free, open-source, lightweight, and works natively on both **Windows** and **macOS** with zero-UI bloat.

---

## ✨ Özellikler / Features

* **🚀 Tek Tıkla Renk Seçimi (One-Click Eyedropper):**
  * **Windows:** Sağ alttaki *Hidden Icons (Sistem Tepsisi)* içindeki **PickHex** ikonuna sol tıkladığınız anda ekranda canlı büyüteç açılır.
  * **macOS:** Sağ üstteki *Menu Bar* içindeki **PickHex** ikonundan **"Ekrandan Renk Seç / Pick Color"** seçeneğine tıkladığınızda büyüteç devreye girer.
* **🔍 Akıllı Büyüteç Kontrolleri (Interactive Magnifier Controls):**
  * **Fare Tekerleği (Scroll Wheel):** Büyüteç yakınlaştırma oranını (`3x` - `9x`) anlık olarak değiştirir.
  * **Yön Tuşları (`↑` `↓` `←` `→`):** İmleci **1 piksel** hassasiyetle kaydırarak ince çizgileri ve kenarlıkları yakalamanızı sağlar.
  * **`Tab` Tuşu:** Büyüteç açıkken kopyalama formatları (`HEX` -> `RGB` -> `HSL` -> `CSS` -> `Tailwind`) arasında anında geçiş yapar.
* **🎨 Penceresiz Ton & Gölge Üretici (Zero-UI Shades, Tints & Harmony):**
  * Sağ tık menüsündeki **Son Seçilen Renkler** altında herhangi bir rengin üzerine geldiğinizde; o rengin **3 açık tonunu (+20%, +40%, +60%)**, **3 koyu gölgesini (-20%, -40%, -60%)** ve **Zıt (Complementary) rengini** hiçbir ek pencere açmadan tek tıkla kopyalayabilirsiniz!
* **📋 Çoklu Format Desteği (6 Developer Formats):**
  * `HEX` (`#FF5733`)
  * `HEX Raw` (`FF5733`)
  * `RGB` (`rgb(255, 87, 51)`)
  * `HSL` (`hsl(11, 100%, 60%)`)
  * `CSS` (`color: #FF5733;`)
  * `Tailwind` (`bg-[#FF5733]`)
* **🔔 Anında Bildirim (Toast Notification):** Renge tıkladığınız anda kodu panoya kopyalar ve ekranda seçtiğiniz dile göre (`"Renk kodu kopyalandı: #FF5733"` / `"Color code copied: #FF5733"`) bildirim gösterir.
* **🌍 Türkçe & İngilizce Dil Desteği:** İlk açılışta dil seçimi sorar; daha sonra sağ tık menüsünden istediğiniz zaman değiştirebilirsiniz.
* **⚡ Başlangıçta Çalıştır (Run on Startup):** Bilgisayar açıldığında otomatik olarak arka planda başlama seçeneği.

---

## 🖥️ Kurulum ve Kullanım / Installation & Usage

### 1. Hazır `.exe` / `.app` İle Kullanım
* **Windows:** `PickHex.exe` dosyasını çift tıklayarak çalıştırın. İlk açılışta dilinizi (**Türkçe / English**) seçin. Uygulama sağ alttaki **Hidden Icons (Sistem Tepsisi)** bölümüne yerleşecektir.
* **macOS:** `PickHex.app` uygulamasını çalıştırın. Uygulama Dock'ta yer kaplamadan doğrudan üstteki **Menu Bar**'a yerleşir.

### 2. Kaynak Koddan Çalıştırma / Running from Source
```bash
pip install -r requirements.txt
python pickhex.py
```
*(İlk kurulum dil seçimi ekranını tekrar görmek isterseniz `python pickhex.py --setup` komutuyla başlatabilirsiniz).*

### 3. Kendi `.exe` veya `.app` Dosyanızı Derleme / Building Executable
```bash
python build.py
```
* Windows'ta `dist/PickHex.exe` tek dosya olarak üretilir.
* macOS'ta `dist/PickHex.app` (Menu Bar uygulaması olarak) üretilir.

---

## 📄 Lisans / License
MIT License — Free forever.
