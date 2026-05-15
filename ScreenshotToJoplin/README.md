# Screenshot And Note (Joplin Version)

Aplikasi desktop yang memungkinkan Anda untuk mengambil tangkapan layar (screenshot), mencoret-coret/menandai gambar tersebut, menambahkan catatan, dan langsung menyimpannya ke aplikasi **Joplin** di komputer Anda. Aplikasi ini berjalan **100% secara lokal** tanpa memerlukan koneksi internet, menjadikannya sangat cepat, aman, dan tanpa batas penggunaan API.

## 🌟 Fitur

1. **Ambil Screenshot Fleksibel**: 
   - **📸 Full Screenshot**: Mengambil seluruh tampilan layar komputer Anda.
   - **✂️ Custom Screenshot**: Mengambil area tertentu dari layar (seperti Snipping Tool).
2. **Coret-Coret Gambar**: Fitur kanvas untuk menggambar secara langsung di atas screenshot.
3. **Deskripsi/Catatan Tambahan**: Kolom teks untuk penjelasan detail terkait gambar.
4. **Kirim Otomatis ke Joplin**: Gambar dan teks akan disimpan sebagai Note (Catatan) baru di aplikasi Joplin secara instan via Web Clipper API lokal.
5. **Simpan Konfigurasi Otomatis**: Cukup masukkan Token Web Clipper satu kali.

---

## 🚀 Cara Penggunaan

### 1. Menjalankan Aplikasi
1. Buka folder `ScreenshotToJoplin`.
2. Klik dua kali pada file **`run.bat`**.
3. Aplikasi akan otomatis menginstall kebutuhan (hanya saat pertama kali dijalankan) dan membuka antarmuka utama.

### 2. Mengaktifkan Joplin Web Clipper API (Wajib)
Agar aplikasi ini bisa mengirim data ke Joplin Anda, Anda harus mengaktifkan layanan Web Clipper di Joplin:
1. Buka aplikasi **Joplin** di komputer Anda.
2. Pergi ke menu **Tools -> Options -> Web Clipper** (Alat -> Pilihan -> Web Clipper).
3. Centang bagian **"Enable the Web Clipper service"** (Langkah 1).
4. Salin (Copy) kode panjang di bagian **"Authorization token"** (Langkah 2).

### 3. Cara Menyimpan Screenshot
1. Buka aplikasi **Screenshot And Note** yang sudah dijalankan.
2. Pilih tipe screenshot (**Full Screenshot** atau **Custom Screenshot**).
3. Tambahkan coretan pada gambar jika diperlukan.
4. Tulis deskripsi/catatan Anda.
5. Masukkan (Paste) **Joplin Web Clipper Token** yang sudah Anda salin.
6. *(Opsional)* Jika Anda ingin menyimpannya di buku catatan (Notebook) tertentu, masukkan **Notebook ID**. Jika dikosongkan, catatan akan disimpan di Notebook default Anda.
7. Klik **"🚀 2. Save to Joplin"**.
8. Cek aplikasi Joplin Anda, catatan baru beserta gambar akan langsung muncul!
