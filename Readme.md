# Proyek API Akademik (FastAPI & MySQL)

Proyek ini adalah implementasi RESTful API untuk mengelola data Mahasiswa menggunakan **FastAPI** dan **MySQL**. Proyek ini merupakan hasil pengerjaan dari **Tugas 3 - Struktur Router CRUD**, yang menerapkan pemecahan kode ke dalam modul (Router) agar struktur proyek lebih rapi dan mudah di-*maintenance*.

## 🛠️ Persyaratan (Prerequisites)

Sebelum menjalankan aplikasi, pastikan Anda sudah menginstal library Python berikut:

```bash
pip install fastapi uvicorn mysql-connector-python pydantic email-validator
```

Pastikan juga Anda sudah memiliki *local server* (seperti XAMPP atau Laragon) yang berjalan dengan database MySQL bernama `db_kampus`.

## 📁 Struktur Folder

Proyek ini menggunakan struktur modular dengan memisahkan konfigurasi database, main aplikasi, dan router:

```text
/proyek_api
├── main.py                # Entry point aplikasi (Mendaftarkan Router)
├── database.py            # Menyimpan logika koneksi ke database MySQL
└── routers/
    └── mahasiswa.py       # Berisi semua endpoint CRUD khusus Mahasiswa & Validasi Pydantic
```

## 🚀 Cara Menjalankan Aplikasi

1. Nyalakan MySQL di XAMPP/Laragon.
2. Buka terminal di dalam folder `/proyek_api`.
3. Jalankan server Uvicorn dengan perintah berikut:
   ```bash
   uvicorn main:app --reload
   ```
4. Buka browser dan akses **Swagger UI** untuk menguji API di:
   [http://localhost:8000/docs](http://localhost:8000/docs)

## 📡 Daftar Endpoint (API Routes)

Semua endpoint mahasiswa menggunakan *prefix* `/mahasiswa`.

| Method | Endpoint | Deskripsi | Keterangan |
| :--- | :--- | :--- | :--- |
| `GET` | `/mahasiswa/` | Mengambil semua data mahasiswa. | Menggunakan query `JOIN` untuk menampilkan `nama_prodi`. |
| `POST` | `/mahasiswa/` | Menambah data mahasiswa baru. | Membutuhkan *request body* (JSON). Dilengkapi validasi Pydantic. Menggunakan `%s` (Parameterized Query) untuk mencegah *SQL Injection*. |
| `PUT` | `/mahasiswa/{nim}` | Mengubah data mahasiswa. | Membutuhkan parameter `nim` pada URL dan *request body* (JSON) untuk data yang diubah. |
| `DELETE` | `/mahasiswa/{nim}` | Menghapus data mahasiswa. | Membutuhkan parameter `nim` pada URL. |

## 🛡️ Validasi Data (Pydantic)

Aplikasi ini menggunakan Pydantic sebagai "Satpam" (*Validator*) untuk memastikan format input JSON dari client sudah benar sebelum masuk ke database. Skema input yang dibutuhkan saat melakukan POST dan PUT adalah sebagai berikut:

```json
{
  "nim": "152024139",
  "nama": "Aditya Luthfi",
  "email": "aditya.luthfi@mhs.itenas.ac.id",
  "id_prodi": 1
}
```
*   `nim`: Minimal 4 karakter, maksimal 10 karakter.
*   `nama`: Minimal 3 karakter.
*   `email`: Harus berformat email yang valid.
*   `id_prodi`: ID dari program studi (integer).