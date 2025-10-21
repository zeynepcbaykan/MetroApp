# 🚇 İstanbul Metro Durum Takip Sistemi

---

## 📖 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Teknoloji Stack](#-teknoloji-stack)
- [Mimari](#-mimari)
- [Proje Yapısı](#-proje-yapısı)
- [Lisans](#-lisans)

---

## 🎯 Proje Hakkında

İstanbul Metro Durum Takip Sistemi, **İBB Metro API** kullanarak şehirdeki tüm metro hatlarının anlık durumunu izleyen ve kullanıcılara görsel bir arayüzle sunan **cloud-native, serverless** bir web uygulamasıdır.

### 💡 Motivasyon

Tüm motivasyonum açıköğretim sınavına giderken yolda metronun çalışmadığını öğrendim; **"Bir yerden bakamıyor muyuz buna ya?"** dediğim ana dayanıyor. 

### Demo

Canlı uygulamaya [buradan](https://metrohizmetdurumu.streamlit.app/) ulaşabilirsiniz.

---

## 🛠️ Teknoloji Stack

### Backend

| Teknoloji | Kullanım Amacı |
|-----------|----------------|
| **Azure Functions** | Serverless data collection (Timer Trigger) |
| **Python** | Core programming language |
| **Azure Cosmos DB** | NoSQL database (MongoDB API) |
| **pymongo** | Database driver |
| **requests** | HTTP client for API calls |

---

## 🏗️ Mimari

### Sistem Akışı
```
┌─────────────────────┐
│   İBB Metro API     │  İstanbul Büyükşehir Belediyesi API
└──────────┬──────────┘
           │ HTTP GET (Her 10 dakika)
           ↓
┌─────────────────────┐
│  Azure Functions    │  Timer Trigger (Cron: */10 * * * *)
│  (Serverless)       │
│                     │
│  • API'den veri çek │
│  • Veriyi işle      │
└──────────┬──────────┘
           │ MongoDB Write
           ↓
┌─────────────────────┐
│  Azure Cosmos DB    │  NoSQL Database (MongoDB API)
│                     │
│  • 18 metro hattı   │
│  • Durum bilgileri  │
│  • Timestamp'ler    │
└──────────┬──────────┘
           │ MongoDB Read
           ↓
┌─────────────────────┐
│  Streamlit App      │  Web Interface
│  (Frontend)         │
│                     │
│  • Verileri göster  │
│  • Görselleştirme   │
└──────────┬──────────┘
           │ HTTPS
           ↓
┌─────────────────────┐
│    Kullanıcı        │  Web Browser
└─────────────────────┘
```

---

## 📁 Proje Yapısı
```
istanbul-metro-tracker/
│
├── 📂 MetroFuncApp/                 # Azure Functions Backend
│   ├── 📂 MetroTimerTrigger/        # Timer trigger function
│   │   ├── __init__.py             # Function entry point
│   │   └── function.json           # Binding configuration
│   │
│   ├── 📂 src/                      # Shared modules
│   │   ├── __init__.py
│   │   ├── db.py                   # Database operations
│   │   ├── scraper.py              # API data fetching
│   │   └── setup.py                # Initial data loader to db
│   │
│   ├── host.json                   # Function app config
│   ├── requirements.txt            # Python dependencies
│   └── .funcignore                 # Deployment exclusions
│
├── 📂 streamlitApp/                 # Streamlit Frontend
│   ├── app.py                      # Main application
│   │
│   ├── 📂 assets/                   # Static assets
│   │
│   ├── 📂 .streamlit/               # Streamlit config
│   │   ├── config.toml
│   │   └── secrets.toml            # Db connection strings, keys
│   │
│   └── requirements.txt            # Python dependencies
│
├── .gitignore                      # Git exclusions
├── README.md                       # This file
└── LICENSE                         # MIT License
```

---

## 📈 Gelecek Geliştirmeler

- [ ] **Push Notifications**: Email/SMS bildirimleri
- [ ] **Historical Data**: Geçmiş veri analizi ve trendler
- [ ] **Social Media Integration**: Twitter hesabı açıklamaları için bot

---

## 📝 Lisans

Bu proje **[MIT](https://opensource.org/licenses/MIT)** lisansı altında lisanslanmıştır. 