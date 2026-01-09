# 🎬 Film Öneri Sistemi - GUI Edition! 🎨

Bu proje, film verilerini kullanarak içerik tabanlı öneri sistemi geliştiren kapsamlı bir veri bilimi uygulamasıdır. **Artık iki farklı EXE formatında: Console ve GUI!**

## 🚀 Hızlı Başlangıç

### 🎨 GUI Versiyonu (Önerilen)
**📁 `outputs/FilmOneriSistemi_GUI.exe` - Çift tıklayın!**

- ✅ **Grafik arayüz** (Tkinter)
- ✅ **4 farklı sekme** (Öneri, Tahmin, Arama, İstatistik)
- ✅ **Konsol penceresi yok**
- ✅ **Kullanıcı dostu** tasarım
- ✅ **Kolay kullanım**

### 💻 Console Versiyonu (Geliştiriciler için)
**📁 `outputs/FilmOneriSistemi.exe` - Çift tıklayın!**

- ✅ **Console arayüz** (CMD)
- ✅ **Menü tabanlı** navigasyon
- ✅ **Kompakt tasarım**
- ✅ **Hızlı erişim**

## � GUI Kullanım Rehberi

### 🎨 Ana Arayüz

```
┌─────────────────────────────────────────────────┐
│        🎬 Film Öneri Sistemi v2.0              │
│     AI Destekli Film Önerileri ve Rating       │
├─────────────────────────────────────────────────┤
│ 🎯 Film Önerisi │ 📈 Rating │ 🔍 Arama │ 📊 İst │
│                 │   Tahmini │         │    atik │
└─────────────────────────────────────────────────┘
```

### 1️⃣ Film Önerisi Sekmesi

**📝 Nasıl Kullanılır:**
1. Film adını girin (örn: "Inception", "Eşkıya")
2. "🔍 Öneri Al" butonuna tıklayın
3. 5 benzer film listesini görün

**📊 Sonuç Tablosu:**
```
Film                Rating  Tür           Ülke      Benzerlik
Matrix Reloaded 23  7.4     Bilim Kurgu   Amerika   0.943
Interstellar Quest  8.1     Bilim Kurgu   Amerika   0.921
```

### 2️⃣ Rating Tahmini Sekmesi

**🎯 Özellik Girişi:**
- **🎭 Tür (0-23)**: Film türü kodu
- **🌍 Ülke (0-22)**: Ülke kodu  
- **🎥 Yönetmen (0-48)**: Yönetmen kodu
- **� Yıl**: Film yılı
- **⏱️ Süre**: Dakika cinsinden
- **😄 Mizah (1-10)**: Mizah seviyesi
- **💥 Aksiyon (1-10)**: Aksiyon oranı
- **💕 Romantizm (1-10)**: Romantik öğeler
- **😰 Gerilim (1-10)**: Gerilim seviyesi

**📈 Tahmin Sonucu:**
```
🎯 Tahmin Edilen Rating: 7.2/10
🌟 Harika film olacak!
```

### 3️⃣ Film Arama Sekmesi

**� Gelişmiş Arama:**
- Film adı, tür, ülke, yönetmene göre arama
- Sonuçlar tablo halinde görüntülenir
- İlk 50 sonuç gösterilir

### 4️⃣ İstatistikler Sekmesi

**📊 Sistem Bilgileri:**
```
📱 Toplam film sayısı         : 4,000
🎭 Farklı tür sayısı          : 24
🌍 Farklı ülke sayısı         : 23
⭐ Ortalama rating           : 6.50
🕐 Ortalama süre             : 130 dakika
```

## 🎮 Kullanım Rehberi

### Ana Menü Seçenekleri:

```
🎬 Film Öneri Sistemi - Ana Menü
============================================================
1️⃣  Film Önerisi Al
2️⃣  Rating Tahmini Yap  
3️⃣  Film Ara
4️⃣  Sistem İstatistikleri
5️⃣  Popüler Filmler
6️⃣  Çıkış
============================================================
```

### 1️⃣ Film Önerisi Alma

```
🎬 Film Önerisi
📝 Film adını girin: Inception
🔍 'Inception' için benzer filmler aranıyor...

✅ 'Inception' için 5 benzer film:
------------------------------------------------------------
1. 🎬 Matrix Reloaded 23
   📊 Rating: 7.4
   🎭 Tür: Bilim Kurgu
   🌍 Ülke: Amerika
   ⭐ Benzerlik: 0.943

2. 🎬 Interstellar Quest
   📊 Rating: 8.1
   🎭 Tür: Bilim Kurgu
   🌍 Ülke: Amerika
   ⭐ Benzerlik: 0.921
```

### 2️⃣ Film Rating Tahmini

```
📈 Rating Tahmini
📝 Film özelliklerini girin (1-10 arası):
🎭 Tür kodu: 5
🌍 Ülke kodu: 12
🎥 Yönetmen kodu: 8
📅 Yıl: 2023
⏱️ Süre (dakika): 120
😄 Mizah (1-10): 7
💥 Aksiyon (1-10): 8
💕 Romantizm (1-10): 5
😰 Gerilim (1-10): 9

✅ Tahmin edilen rating: 7.2/10
🌟 Harika film olacak!
```

## 📋 İçerik ve Özellikler

### 🤖 Yapay Zeka Özellikleri
- **İçerik Tabanlı Öneri**: CountVectorizer + Cosine Similarity
- **Rating Tahmini**: Doğrusal Regresyon + StandardScaler
- **Akıllı Arama**: Fuzzy string matching
- **Otomatik Sınıflandırma**: Median tabanlı ikili sınıflandırma

### 📊 Veri Özellikleri
- **4000 Film**: Türk ve dünya sineması
- **24 Farklı Tür**: Aksiyon'dan Drama'ya
- **23 Ülke**: Geniş coğrafi kapsamı  
- **49 Yönetmen**: Ünlü yönetmenler
- **9 Özellik**: Mizah, aksiyon, ritim, gerilim vb.

### 🎯 Sistem Yetenekleri
- **Real-time Öneri**: Anlık benzerlik hesaplama
- **Akıllı Tahmin**: ML tabanlı rating tahmini
- **Kapsamlı Arama**: Kısmi isim eşleştirme
- **İstatistiksel Analiz**: Detaylı sistem bilgileri

## 🗂️ Proje Yapısı (Geliştiriciler İçin)

```
film_oneri_sistemi/
├── outputs/
│   ├── FilmOneriSistemi.exe       # 🚀 ÇIFT TIKLA ÇALIŞTIR!
│   ├── *.xlsx                     # İşlenmiş veriler
│   ├── *.png                      # Grafikler
│   └── *.odt                      # Raporlar
├── src/                           # Kaynak kodlar
│   ├── film_oneri_sistemi.py      # Ana standalone kod
│   ├── build_exe.py               # EXE builder
│   └── [diğer modüller]
└── README.md                      # Bu dosya
```

## � Geliştiriciler İçin (Python Versiyonu)

### Gereksinimler
```bash
Python 3.8+
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
pyinstaller>=5.0  # EXE oluşturmak için
```

### Kaynak Koddan Çalıştırma
```bash
cd src
python film_oneri_sistemi.py
```

### Yeni EXE Oluşturma
```bash
cd src
python build_exe.py
```

## 📈 Sistem Performansı

### 🎯 Öneri Sistemi
- **Benzerlik Skorları**: 0.85 - 1.00
- **Yanıt Süresi**: < 1 saniye
- **Doğruluk**: Yüksek içerik benzerliği

### 📊 Regresyon Modeli  
- **Eğitim Seti**: 3,200 film
- **Test Seti**: 800 film
- **Özellik Sayısı**: 9 boyutlu vektör

### 💾 Sistem Kaynakları
- **Bellek Kullanımı**: ~50 MB
- **Disk Alanı**: 99 MB (EXE)
- **CPU**: Düşük kaynak kullanımı

## 🎓 Eğitim Değeri

### Öğrenilen Teknolojiler
- **Makine Öğrenmesi**: Supervised & Unsupervised
- **Veri Bilimi**: Preprocessing, Feature Engineering
- **Python**: Pandas, NumPy, Scikit-learn
- **Deployment**: PyInstaller, Standalone Apps

### Uygulama Alanları
- **E-ticaret**: Ürün öneri sistemleri
- **Streaming**: Netflix, Spotify algoritmaları  
- **Sosyal Medya**: İçerik kişiselleştirme
- **Pazarlama**: Hedefli reklam sistemleri

## 🆚 Sürüm Karşılaştırması

| Özellik | Python Sürümü | EXE Sürümü |
|---------|---------------|------------|
| Kurulum | Python + Kütüphaneler | ❌ Gereksiz |
| Çalıştırma | `python main.py` | ⚡ Çift tık |
| Boyut | ~10 MB | 99 MB |
| Taşınabilirlik | ❌ Bağımlılık var | ✅ Standalone |
| Hız | Hızlı | Hızlı |
| Güncelleme | Kolay | EXE yeniden build |

## 🚨 Sorun Giderme

### EXE Çalışmıyor?
1. **Windows Defender**: Geçici olarak devre dışı bırakın
2. **Admin Hakları**: Yönetici olarak çalıştırın
3. **Klasör İzinleri**: Yazma iznini kontrol edin

### Performans Sorunu?
1. **RAM**: En az 4 GB RAM önerilir
2. **Diğer Programlar**: Ağır uygulamaları kapatın
3. **Disk Alanı**: En az 1 GB boş alan

### Veri Sorunu?
1. **Otomatik**: Sistem otomatik veri oluşturur
2. **Yeniden Başlat**: Programı yeniden çalıştırın
3. **Klasör**: EXE'yi farklı klasörde deneyin

## 🎉 Özellikler ve Avantajlar

### ✅ Kullanıcı Dostu
- Sezgisel menü sistemi
- Anlaşılır hata mesajları
- Emoji destekli arayüz
- Adım adım rehberlik

### ✅ Teknik Üstünlük
- Modern ML algoritmaları
- Optimize edilmiş kod yapısı
- Hızlı veri işleme
- Düşük kaynak kullanımı

### ✅ Pratik Çözüm
- Kurulum gerektirmez
- Taşınabilir uygulama
- Offline çalışır
- Güvenli ve temiz

## 🔮 Gelecek Planları

### Kısa Vadeli
- [ ] GUI (Tkinter/PyQt) arayüzü
- [ ] Web tabanlı versiyon (Flask/FastAPI)
- [ ] TF-IDF algoritması entegrasyonu
- [ ] Daha büyük veri seti desteği

### Uzun Vadeli  
- [ ] Deep Learning modelleri
- [ ] Collaborative Filtering
- [ ] API entegrasyonları
- [ ] Mobil uygulama versiyonu

## 📄 Lisans

Bu proje eğitim amaçlıdır ve açık kaynak olarak paylaşılmıştır.

## 📞 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

*🎬 Film severlerin AI destekli öneri sistemi - Artık sadece çift tıkla!*

**⚡ Hemen deneyin: `outputs/FilmOneriSistemi.exe`**

## 🎯 Kullanım

### Ana Uygulama Menüsü

1. **🎯 Film Öneri Al**: Bir film adı girerek benzer filmler alabilirsiniz
2. **📈 Film Rating Tahmini**: Film özelliklerini girerek rating tahmini yapabilirsiniz
3. **📊 Veri Analizi**: Korelasyon matrisi ve görselleştirmeler
4. **🎬 Popüler Filmler**: En yüksek puanlı filmleri görüntüleme
5. **📋 Sistem Bilgileri**: Proje hakkında detaylı bilgiler

### Jupyter Notebook

```bash
cd notebooks
jupyter notebook film_oneri_sistemi_demo.ipynb
```

## 📊 Modüller ve Özellikler

### 1. Veri Ön İşleme (`data_preprocessing.py`)
- Kategorik verileri LabelEncoder ile encode etme
- Toplam skor hesaplama
- Film sınıflandırma (median eşik değeri)

### 2. Öneri Sistemi (`recommendation_system.py`)
- CountVectorizer ile özellik vektörizasyonu
- Cosine Similarity ile benzerlik hesaplama
- İçerik tabanlı film önerileri

### 3. Regresyon Analizi (`regression_analysis.py`)
- Doğrusal regresyon ile rating tahmini
- Model performans değerlendirmesi (MSE, R², MAE)
- Özellik önem analizi

### 4. Korelasyon Analizi (`correlation_analysis.py`)
- Özellikler arası korelasyon matrisi
- Heatmap görselleştirme
- Scatter matrix ve dağılım analizleri

## 📈 Sonuçlar

### Model Performansı
- **MSE**: ~1.61
- **R² Score**: ~0.18
- **Sonuç**: Sınırlı açıklama gücü, iyileştirme gerekli

### Korelasyon Bulguları
- En yüksek korelasyonlar: rhythm (0.10), tension (0.08)
- Genel korelasyon seviyesi: Zayıf
- Özellikler arası güçlü doğrusal ilişki bulunmuyor

## 🔧 İyileştirme Önerileri

1. **Daha Büyük Veri Seti**: Daha fazla film ve özellik
2. **Gelişmiş NLP**: TF-IDF, Word2Vec, BERT
3. **Collaborative Filtering**: Kullanıcı-film etkileşimi
4. **Deep Learning**: Neural Collaborative Filtering
5. **Feature Engineering**: Yeni özellik oluşturma

## 📝 Veri Seti

Proje 50 film içeren örnek veri seti ile çalışır:
- **Türk Filmleri**: Eşkıya, G.O.R.A, Babam ve Oğlum vb.
- **Dünya Filmleri**: The Godfather, Titanic, Inception vb.

### Özellikler:
- `title`: Film adı
- `genre`: Tür
- `country`: Ülke
- `directors`: Yönetmen
- `duration`: Süre (dakika)
- `avg_vote`: Ortalama oy (1-10)
- `humor`: Mizah seviyesi (1-10)
- `rhythm`: Ritim/tempo (1-10)
- `effort`: Çaba/kalite (1-10)
- `tension`: Gerilim (1-10)
- `erotism`: Erotizm (1-10)

## 🎓 Eğitim Amaçlı Notlar

Bu proje veri bilimi eğitimi için tasarlanmıştır ve şu konuları kapsar:

- **Veri Ön İşleme**: Temizleme, encode etme, normalizasyon
- **Keşifsel Veri Analizi**: Dağılım, korelasyon, görselleştirme
- **Makine Öğrenmesi**: Regresyon, sınıflandırma
- **Öneri Sistemleri**: İçerik tabanlı filtreleme
- **Python Kütüphaneleri**: pandas, scikit-learn, matplotlib

## 📄 Lisans

Bu proje eğitim amaçlıdır ve açık kaynak olarak paylaşılmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📞 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

*Bu proje, veri bilimi ve makine öğrenmesi tekniklerinin pratik uygulamasını göstermek amacıyla geliştirilmiştir.*