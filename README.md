# 🔥 Proxy Checker V.3 - Ultimate Edition

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Profesyonel Proxy Test ve Kontrol Aracı**

[English](#english) | [Türkçe](#turkish)

</div>

---

## 🇹🇷 <a name="turkish"></a>Türkçe

### 📖 Açıklama
Proxy Checker V.3, HTTP, HTTPS, SOCKS4 ve SOCKS5 proxy'lerini hız, stabilite ve ülke bilgisi ile test eden gelişmiş bir araçtır. Çoklu thread desteği ve kullanıcı dostu arayüzü ile proxy listenizi hızlıca kontrol edebilirsiniz.

### ✨ Özellikler
- 🚀 **Çoklu Thread Desteği**: 10-200 thread arası ayarlanabilir hız
- ⚡ **Hız Filtreleme**: 500-5000ms arası özelleştirilebilir limit
- 🌍 **Otomatik Ülke Tespiti**: Her proxy için coğrafi konum bilgisi
- 📊 **Canlı İstatistikler**: Gerçek zamanlı analiz ve raporlama
- 💾 **Çoklu Export Formatları**: ip:port, user:pass@ip:port, ip:port:user:pass
- 🎨 **4 Farklı Tema**: Mor, Mavi, Yeşil, Kırmızı
- 📁 **Esnek Veri Girişi**: Dosya, GitHub URL, manuel yapıştırma

### 🛠️ Kurulum

#### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

#### Adım 1: Repository'yi İndirin
```bash
git clone https://github.com/KULLANICI_ADIN/Proxy-Checker-V3.git
cd Proxy-Checker-V3
```

#### Adım 2: Gerekli Paketleri Kurun
```bash
pip install -r requirements.txt
```

#### Adım 3: Programı Çalıştırın
```bash
python Checker.py
```

### 🚀 Kullanım

1. **Proxy Ekleme**:
   - 📁 Dosya Ekle: .txt dosyasından proxy listesi yükle
   - 🔗 GitHub: GitHub URL'sinden direkt yükle
   - 📋 Çoklu Yapıştır: Manuel olarak kopyala-yapıştır

2. **Ayarlar**:
   - **Tip**: http, https, socks4, socks5 seçin
   - **Hız (ms)**: Maksimum kabul edilebilir ping süresi (varsayılan 1500ms)
   - **Threads**: Eşzamanlı test sayısı (varsayılan 80)

3. **Test Başlatma**:
   - ▶ Başlat butonuna tıklayın
   - Sonuçları gerçek zamanlı izleyin
   - Test bittiğinde otomatik olarak "hizli.txt" dosyasına kaydedilir

### 📋 Desteklenen Proxy Tipleri
- ✅ HTTP
- ✅ HTTPS
- ✅ SOCKS4
- ✅ SOCKS5

### 💡 İpuçları
- Hızlı tarama için thread sayısını 100-200 arasına yükseltin
- Kaliteli proxy için hız limitini 1000-1500ms tutun
- SOCKS5 proxy'ler genelde HTTP/HTTPS'den daha yavaş çalışır (%1-3 başarı oranı normal)
- Çalışan proxy'leri kopyalamak için "📋 Hızlıları Kopyala" butonunu kullanın

### 📊 İstatistikler
- **Toplam**: Test edilen proxy sayısı
- **Çalışan**: Başarılı geçen proxy sayısı
- **Başarısız**: Timeout veya hata veren proxy'ler
- **Ortalama Ping**: Çalışan proxy'lerin ortalama yanıt süresi
- **En Hızlı 10**: En düşük ping'e sahip proxy'ler
- **Ülkeler**: Coğrafi dağılım istatistikleri

### 👨‍💻 Geliştirici
**youmean25**  
Discord: youmean25

### ⚠️ Sorumluluk Reddi
Bu araç **sadece yasal ve etik amaçlarla** kullanılmalıdır. Proxy'lerin sahibinin iznini almadan test edilmesi veya kullanılması yasaktır. Kullanıcı, bu aracın kullanımından kaynaklanan tüm yasal sorumluluğu kabul eder. Geliştirici, aracın kötüye kullanımından sorumlu değildir.

### 📄 Lisans
Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

## 🇬🇧 <a name="english"></a>English

### 📖 Description
Proxy Checker V.3 is an advanced tool for testing HTTP, HTTPS, SOCKS4, and SOCKS5 proxies with speed, stability, and country information. With multi-threading support and a user-friendly interface, you can quickly verify your proxy lists.

### ✨ Features
- 🚀 **Multi-Threading Support**: Adjustable speed from 10-200 threads
- ⚡ **Speed Filtering**: Customizable limit from 500-5000ms
- 🌍 **Automatic Country Detection**: Geographic location for each proxy
- 📊 **Live Statistics**: Real-time analysis and reporting
- 💾 **Multiple Export Formats**: ip:port, user:pass@ip:port, ip:port:user:pass
- 🎨 **4 Different Themes**: Purple, Blue, Green, Red
- 📁 **Flexible Input**: File, GitHub URL, manual paste

### 🛠️ Installation

#### Requirements
- Python 3.8 or higher
- pip (Python package manager)

#### Step 1: Clone Repository
```bash
git clone https://github.com/USERNAME/Proxy-Checker-V3.git
cd Proxy-Checker-V3
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Run Program
```bash
python Checker.py
```

### 🚀 Usage

1. **Add Proxies**:
   - 📁 File: Load proxy list from .txt file
   - 🔗 GitHub: Load directly from GitHub URL
   - 📋 Paste: Manual copy-paste

2. **Settings**:
   - **Type**: Select http, https, socks4, or socks5
   - **Speed (ms)**: Maximum acceptable ping time (default 1500ms)
   - **Threads**: Number of concurrent tests (default 80)

3. **Start Testing**:
   - Click ▶ Start button
   - Monitor results in real-time
   - Results automatically saved to "hizli.txt"

### 📋 Supported Proxy Types
- ✅ HTTP
- ✅ HTTPS
- ✅ SOCKS4
- ✅ SOCKS5

### 💡 Tips
- Increase threads to 100-200 for faster scanning
- Keep speed limit at 1000-1500ms for quality proxies
- SOCKS5 proxies typically slower than HTTP/HTTPS (1-3% success rate is normal)
- Use "📋 Copy Fast" button to copy working proxies

### 📊 Statistics
- **Total**: Number of tested proxies
- **Working**: Successfully passed proxies
- **Failed**: Timeout or error proxies
- **Average Ping**: Mean response time of working proxies
- **Top 10 Fastest**: Proxies with lowest ping
- **Countries**: Geographic distribution statistics

### 👨‍💻 Developer
**youmean25**  
Discord: youmean25

### ⚠️ Disclaimer
This tool should be used **for legal and ethical purposes only**. Testing or using proxies without the owner's permission is prohibited. The user accepts all legal responsibility arising from the use of this tool. The developer is not responsible for misuse of the tool.

### 📄 License
This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**  
**⭐ If you like this project, don't forget to give it a star!**

Made with ❤️ by youmean25

</div>
