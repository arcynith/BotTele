## Bot Telegram Menu Angka

Bot Telegram sederhana berbasis **Python** dan **python-telegram-bot**.
Saat pengguna mengirim `/start`, bot menampilkan menu utama dengan tiga tombol:
`1`, `2`, dan `3`. Setiap tombol akan membalas dengan pesan yang berbeda.

Bot ini menggunakan:

- **ReplyKeyboardMarkup** untuk menampilkan tombol.
- **Polling** untuk menerima update dari Telegram.
- **Environment variable** `BOT_TOKEN` untuk menyimpan token bot (aman untuk GitHub dan deployment).

---

## Fitur

- **Perintah `/start`**
  - Menampilkan teks: `Menu Utama - Pilih tombol di bawah`.
  - Menampilkan keyboard dengan tombol `1`, `2`, `3`.

- **Respon tombol**
  - Tekan `1` → balasan: `Anda menekan tombol 1`.
  - Tekan `2` → balasan: `Anda menekan tombol 2`.
  - Tekan `3` → balasan: `Anda menekan tombol 3`.
  - Jika user mengetik teks lain → bot mengingatkan untuk memilih salah satu tombol.

---

## Struktur Proyek

```text
BotTele/
├─ bot.py           # Kode utama bot Telegram
├─ requirements.txt # Dependency Python
├─ Procfile         # Command untuk deploy di Render (worker)
├─ .env.example     # Contoh file environment lokal
└─ README.md        # Dokumentasi proyek
```

---

## Persiapan

1. **Pastikan Python sudah terpasang**

   Cek dengan:

   ```bash
   python --version
   ```

2. **Buat bot di Telegram**

   - Buka aplikasi Telegram.
   - Cari akun `BotFather`.
   - Kirim `/start`.
   - Kirim `/newbot` dan ikuti instruksi:
     - Beri nama bot (bebas).
     - Beri username bot (harus berakhiran `bot`, misalnya `menu_angka_bot`).
   - Di akhir, BotFather akan mengirim **token bot** (format kurang lebih `123456789:XXXX...`).

   **Jangan pernah commit token asli ke GitHub.** Simpan di environment variable saja.

---

## Instalasi Dependency (Lokal)

Semua perintah dijalankan di folder proyek (yang berisi `bot.py`).

1. (Opsional, tapi disarankan) Buat virtual environment:

   ```bash
   python -m venv venv
   ```

2. Aktifkan virtual environment (Windows):

   ```bash
   venv\Scripts\activate
   ```

3. Install dependency:

   ```bash
   pip install -r requirements.txt
   ```

---

## Konfigurasi Environment Variable

Bot membaca token dari environment variable bernama **`BOT_TOKEN`**.

### 1. Konfigurasi di lokal (file `.env`)

Untuk memudahkan, Anda bisa menyalin file contoh:

```bash
copy .env.example .env
```

Lalu buka file `.env` dan isi:

```env
BOT_TOKEN=TOKEN_BOT_ANDA_DI_SINI
```

Untuk menjalankan dengan file `.env`, ada dua opsi:

- **Opsi sederhana**: set environment variable langsung di shell sebelum menjalankan:

  ```bash
  set BOT_TOKEN=TOKEN_BOT_ANDA_DI_SINI
  python bot.py
  ```

  (Di PowerShell, gunakan `setx` atau `$env:BOT_TOKEN="..."`.)

- **Opsi lebih rapi**: gunakan library tambahan seperti `python-dotenv` dan load `.env` di dalam `bot.py`.  
  (Belum di-include di proyek ini agar tetap sederhana.)

### 2. Konfigurasi di server (Render, Railway, dll.)

Di dashboard layanan hosting Anda, cari bagian **Environment / Environment Variables** dan tambahkan:

- **Key**: `BOT_TOKEN`
- **Value**: token bot dari BotFather

---

## Menjalankan Bot Secara Lokal

Dengan asumsi:

- Dependency sudah terinstall.
- Environment variable `BOT_TOKEN` sudah di-set.

Jalankan:

```bash
python bot.py
```

Jika berhasil, di terminal akan muncul:

```text
Bot sedang berjalan... Tekan Ctrl+C untuk menghentikan.
```

Lalu:

1. Buka Telegram.
2. Cari username bot Anda.
3. Tekan `Start` atau kirim `/start`.
4. Coba tekan tombol `1`, `2`, dan `3`.

Untuk menghentikan bot, tekan:

- `Ctrl + C` di terminal.

---

## Deploy ke Render

Contoh ini menggunakan **Render** sebagai worker/background service (bukan web server HTTP).

1. **Push proyek ini ke GitHub**

   - Pastikan **tidak ada token asli** di dalam source code.
   - File `.env` sebaiknya **tidak** ikut di-push (tambahkan ke `.gitignore` jika perlu).

2. **Buat layanan baru di Render**

   - Masuk ke Render.
   - Pilih **New** → **Background Worker** (atau service sejenis).
   - Hubungkan ke repository GitHub yang berisi proyek ini.

3. **Set command dan environment**

   - **Start command**:

     ```bash
     python bot.py
     ```

   - Tambahkan environment variable:
     - `BOT_TOKEN` dengan nilai token bot dari BotFather.

4. **Deploy**

   - Render akan meng-clone repo, menginstall dependency dari `requirements.txt`,
     lalu menjalankan `python bot.py` sesuai `Procfile`/konfigurasi worker.

Jika layanan sudah berjalan tanpa error, bot akan aktif 24/7 selama service di Render aktif.

---

## Catatan Keamanan

- Jangan commit token bot asli ke GitHub.
- Jika token sudah terlanjur tersebar publik, segera:
  - Buka BotFather.
  - Pilih bot Anda.
  - Gunakan opsi **/revoke** token untuk mengganti token lama dengan yang baru.
- Setelah itu, update nilai `BOT_TOKEN` di environment server Anda.

