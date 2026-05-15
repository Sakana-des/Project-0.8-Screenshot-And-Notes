# Screenshot And Note (Notion Version)

Aplikasi desktop sederhana yang memungkinkan Anda untuk mengambil tangkapan layar (screenshot), mencoret-coret/menandai gambar tersebut, menambahkan catatan, dan langsung menyimpannya ke halaman Notion yang Anda tentukan. Aplikasi ini sepenuhnya berjalan secara lokal tanpa memerlukan bantuan AI buatan, sehingga sangat ringan dan dapat dikontrol sepenuhnya oleh Anda.

## 🌟 Fitur

1. **Ambil Screenshot Fleksibel**: 
   - **📸 Full Screenshot**: Mengambil seluruh tampilan layar komputer Anda.
   - **✂️ Custom Screenshot**: Mengambil area tertentu dari layar (seperti Snipping Tool). Anda bisa drag dari ujung ke ujung untuk memilih area yang ingin disimpan.
2. **Coret-Coret Gambar**: Terdapat fitur kanvas yang memungkinkan Anda menggambar secara langsung di atas screenshot, lengkap dengan pengaturan warna pena, untuk menandai bagian informasi penting.
3. **Deskripsi/Catatan Tambahan**: Kolom teks disediakan agar Anda dapat menulis penjelasan detail terkait gambar tersebut.
4. **Kirim Otomatis ke Notion**: Gambar beserta teks penjelasan akan terunggah secara rapi dalam satu susunan format blok (Gambar di atas, Teks di bawah) ke halaman Notion yang ditentukan.
5. **Simpan Konfigurasi Otomatis**: Anda hanya perlu memasukkan Token Notion dan URL Halaman satu kali. Aplikasi akan mengingatnya untuk penggunaan selanjutnya.

---

## 🚀 Cara Penggunaan

### 1. Menjalankan Aplikasi
1. Buka folder `ScreenshotToNotion`.
2. Klik dua kali pada file **`run.bat`**.
3. Aplikasi akan otomatis menginstall kebutuhan (hanya saat pertama kali dijalankan) dan membuka antarmuka utama.

### 2. Mengatur Akses Notion (Wajib untuk Penggunaan Pertama)
Agar aplikasi ini diizinkan untuk menulis dan menambahkan gambar ke Notion Anda, Anda harus membuat sebuah **Integration Token** dan menghubungkannya dengan halaman Notion Anda. Ikuti langkah mudah berikut:

#### A. Membuat Integration Token
1. Buka [Notion Integrations](https://www.notion.so/my-integrations) di browser Anda (pastikan Anda sudah login ke Notion).
2. Klik tombol **"New integration"** (Integrasi Baru).
3. Beri nama bebas (misalnya: "Aplikasi Screenshot") dan klik **"Submit"**.
4. Di halaman selanjutnya, di bawah bagian **Secrets**, klik tombol **"Show"** lalu **Copy** kode tersebut (Token ini biasanya diawali dengan tulisan `secret_`).

#### B. Memberi Izin pada Halaman Notion
1. Buka aplikasi Notion Anda dan masuk ke Halaman (Page) yang ingin Anda jadikan tempat menyimpan gambar.
2. Klik ikon **titik tiga (...)** di pojok kanan atas halaman.
3. Gulir ke bawah, lalu klik menu **"Add connections"**.
4. Cari nama integrasi yang baru saja Anda buat di langkah A (misal: "Aplikasi Screenshot").
5. Klik nama integrasi tersebut dan pilih **"Confirm"**.

### 3. Cara Menyimpan Screenshot ke Notion
1. Di aplikasi **Screenshot to Notion**, pilih tipe screenshot yang Anda inginkan:
   - Klik **"📸 Full Screenshot"** untuk menangkap seluruh layar.
   - Atau klik **"✂️ Custom Screenshot"** untuk menyeleksi hanya bagian tertentu saja dengan cara klik, tahan, dan geser (drag).
2. Coret gambar atau gunakan tombol **"🎨 Change Pen Color"** untuk mengubah warna stabilo/pena, jika dibutuhkan.
3. Di bagian **Description**, ketikkan penjelasan terkait gambar yang akan disimpan.
4. Masukkan **Link URL Halaman Notion** Anda di kolom yang tersedia (Bisa didapat dengan klik `Share -> Copy link` di Notion).
5. Masukkan **Token Notion** (yang Anda dapatkan dari langkah A) di kolom Token.
6. Terakhir, klik **"🚀 2. Save to Notion"**.
7. Tunggu beberapa saat, dan notifikasi sukses akan muncul. Gambar dan teks Anda akan langsung tersedia di halaman Notion!
