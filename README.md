# Screenshot And Note System

Selamat datang di ekosistem **Screenshot And Note**! 

Sistem ini adalah kumpulan aplikasi desktop berbasis Python yang dirancang untuk mempercepat alur kerja Anda: menangkap gambar layar (screenshot), memberikan coretan/anotasi visual, menulis catatan terkait, dan langsung mengirimkannya ke platform Note favorit Anda.

Saat ini sistem memiliki beberapa modul integrasi yang bisa Anda gunakan sesuai kebutuhan:

### 1. 🟢 Screenshot And Note (Joplin Version)
*(Sangat Direkomendasikan!)*
- **Folder:** `ScreenshotToJoplin/`
- **Fitur:** Terhubung ke aplikasi Joplin menggunakan API Lokal (Web Clipper).
- **Kelebihan:** 100% Offline, privasi terjamin, sangat cepat, dan gratis selamanya tanpa batasan limit API internet.

### 2. 🔵 Screenshot And Note (Notion Version)
- **Folder:** `ScreenshotToNotion/`
- **Fitur:** Terhubung ke Notion Workspace Anda.
- **Kelebihan:** Catatan Anda langsung tersinkronisasi ke cloud Notion, dapat dibagikan dengan tim atau diakses dari mana saja. (Catatan: Mungkin memiliki limitasi pada API Notion gratis untuk unggahan gambar eksternal, aplikasi menggunakan Catbox.moe sebagai penyimpan gambar sementara).

### 3. 🟣 Screenshot And Note (Discord Version)
- **Folder:** `ScreenshotToDiscord/`
- **Fitur:** (Dalam pengembangan) Terhubung ke Private Channel Discord Anda.
- **Kelebihan:** Praktis untuk menjadikannya sebagai log catatan singkat layaknya mengirim pesan.

---

## 🛠️ Persyaratan Sistem Umum
- **OS:** Windows (Telah dites di Windows)
- **Python:** Python 3.8 ke atas.
- Masing-masing aplikasi menggunakan Virtual Environment (`venv`) untuk memastikan instalasi modul rapi dan tidak mengganggu sistem Anda.

## 🚀 Cara Menjalankan
Pilih folder aplikasi yang ingin Anda gunakan, masuk ke dalamnya, dan klik dua kali pada file **`run.bat`**. 
Script tersebut akan otomatis menyiapkan kebutuhan Python dan menjalankan antarmuka aplikasinya.

Masing-masing folder memiliki file `README.md` tersendiri untuk panduan setup yang lebih spesifik.
