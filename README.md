# Inventory Management App

![CI](https://github.com/erikaangeliaaaaa/inventory-app/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)

## Deskripsi Aplikasi

Aplikasi ini merupakan sistem manajemen inventori sederhana berbasis web yang dibuat menggunakan Flask dan SQLite. Aplikasi ini memungkinkan pengguna untuk menambahkan, mengedit, melihat, dan menghapus data barang.

Aplikasi ini dikembangkan sebagai bagian dari tugas implementasi automated testing dan Continuous Integration (CI).

## Fitur Utama

- Menambahkan item baru (Add Item)
- Mengedit data item (Edit Item)
- Menghapus item (Delete Item)
- Menampilkan daftar item (View Items)
- Validasi input (nama tidak boleh kosong, stok harus angka dan tidak negatif)

## Teknologi yang Digunakan

- Python (Flask)
- SQLite
- SQLAlchemy
- Pytest
- GitHub Actions (CI/CD)

## Cara Menjalankan Aplikasi

1. Clone repository:

```
git clone <https://github.com/erikaangeliaaaaa/inventory-app.git>
cd inventory-app
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```
python app.py
```

4. Buka browser:

```
http://127.0.0.1:5000
```

## Cara Menjalankan Testing

Menjalankan semua test:

```
python -m pytest
```

Menjalankan test dengan coverage:

```
python -m pytest --cov=services --cov=models --cov-report=html
```

Hasil coverage dapat dilihat di:

```
htmlcov/index.html
```

## Strategi Pengujian

### Unit Testing

- Menguji logika bisnis pada `InventoryService`
- Validasi input (nama kosong, stok negatif, tipe data)
- Operasi CRUD (Add, Update, Delete, Get)

### Integration Testing

- Menguji endpoint Flask:
  - `/` (index)
  - `/add`
  - `/edit/<id>`
  - `/delete/<id>`

- Menguji interaksi dengan database

## Test Coverage

Aplikasi ini memiliki coverage sebesar "98%", yang menunjukkan bahwa hampir seluruh kode telah diuji.

## Continuous Integration (CI)

Project ini menggunakan GitHub Actions untuk:

- Install dependencies
- Menjalankan test otomatis
- Menghasilkan laporan coverage

CI akan berjalan setiap:

- Push ke repository
- Pull request

## Kesimpulan

Aplikasi ini berhasil mengimplementasikan automated testing, integration testing, serta CI/CD dengan coverage tinggi, sesuai dengan praktik modern software development.
