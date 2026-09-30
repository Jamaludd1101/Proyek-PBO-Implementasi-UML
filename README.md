# 🛒 Sistem Manajemen Minimarket (OOP Python)

Proyek ini adalah simulasi sistem manajemen minimarket yang dibangun menggunakan prinsip *Object-Oriented Programming* (OOP) dalam bahasa Python. Sistem ini dirancang untuk dapat melakukan serialisasi data ke dalam format JSON.

---

## 🗺️ Class Map & Access Modifiers (Visibilitas)

Dalam desain sistem ini, kami menerapkan aturan *Access Modifiers* yang ketat sesuai dengan standar OOP (Encapsulation). Di Python, visibilitas diatur menggunakan *naming convention*:
*   **Public (`+`)** : Dapat diakses dari mana saja (tanpa awalan garis bawah).
*   **Protected (`#`)** : Dapat diakses dalam class itu sendiri dan class turunannya (menggunakan awalan `@property` atau `_`).
*   **Private (`-`)** : Hanya dapat diakses di dalam class itu sendiri (menggunakan awalan ganda `__`).

Berikut adalah pemetaan ke-10 class yang digunakan dalam proyek ini:

### 1. Class Utama (Main Class / Controller)
Class ini bertindak sebagai pusat kendali program yang menghubungkan seluruh komponen.
*   **`Toko`** (Public Class)
    *   **Peran:** Mengelola daftar inventaris produk dan riwayat seluruh transaksi.
    *   **Atribut:** `-nama` (Private), `-daftar_produk` (Private), `-riwayat` (Private).
    *   **Method:** `+tambah_produk()`, `+cari_produk()`, `+mulai_transaksi()`, `+simpan_database_json()` (Semua Public).

### 2. Class Abstrak & Sub-Class (Produk)
Kumpulan class ini merepresentasikan barang yang dijual di minimarket.
*   **`Produk`** (Abstract / Base Class)
    *   **Peran:** Kerangka dasar (Blueprint) untuk semua jenis produk. Tidak bisa diinstansiasi secara langsung.
    *   **Atribut:** `-nama`, `-harga`, `-stok` (Semua Private).
    *   **Method/Property:** `#harga` (Protected access via `@property`), `+hitung_diskon()` (Abstract Public).

*   **`Makanan`**, **`Mainan`**, **`Minuman`** (Concrete Sub-Classes)
    *   **Peran:** Turunan dari class `Produk` dengan spesifikasi masing-masing.
    *   **Atribut Khusus:** `-kadaluarsa` (Makanan), `-rekomendasi_umur` (Mainan), `-ukuran_ml` (Minuman) -> (Semua Private).
    *   **Method:** Mengimplementasikan wajib (Override) method `+hitung_diskon()` (Public).

### 3. Class Transaksi & Pengguna
Kumpulan class yang mengatur alur bisnis jual-beli.
*   **`Pembeli`**
    *   **Peran:** Entitas pelanggan. Memiliki **Komposisi** terhadap `Keranjang` (Keranjang ada karena pembeli ada).
    *   **Atribut:** `-nama`, `-saldo`, `-keranjang` (Semua Private).
    *   **Method/Property:** `+keranjang` (Public getter), `+tambah_ke_keranjang()`.
*   **`Keranjang`**
    *   **Peran:** Menampung sementara barang yang akan dibeli.
    *   **Atribut:** `-item` (Private).
    *   **Method:** `+tambah()`, `+hapus()`, `+total_harga()` (Public).
*   **`Voucher`**
    *   **Peran:** Memberikan potongan harga jika syarat terpenuhi.
    *   **Atribut:** `-kode`, `-potongan` (Private).
*   **`Transaksi`**
    *   **Peran:** Mesin hitung dan validasi pembayaran.
    *   **Atribut:** `-pembeli`, `-keranjang`, `-voucher` (Private, mengambil referensi / Agregasi).
    *   **Method:** `+hitung_total()`, `+cek_saldo()`, `+bayar()`, `+cetak_struk()` (Public).
*   **`RiwayatTransaksi`**
    *   **Peran:** Menyimpan log struk yang berhasil dibayar.
    *   **Atribut:** `-daftar` (Private list).

---

## 🚀 Konsep OOP yang Diterapkan

1.  **Encapsulation (Pembungkusan):** Seluruh atribut penting seperti harga, stok, dan saldo diatur sebagai *Private* (`__`). Perubahan data hanya bisa dilakukan melalui *Public Method* (seperti `kurangi_stok` atau `kurangi_saldo`) untuk mencegah kebocoran/manipulasi data dari luar class.
2.  **Inheritance (Pewarisan):** Class `Makanan`, `Mainan`, dan `Minuman` mewarisi sifat dari class induk `Produk`.
3.  **Polymorphism (Banyak Bentuk):** Method `hitung_diskon()` memiliki nama yang sama, tetapi perilakunya berbeda di setiap anak class (Makanan diskon 10%, Mainan 5%, Minuman 20%).
4.  **Abstraction:** Penggunaan library `abc` pada class `Produk` menjadikannya *Abstract Class*. Memaksa setiap produk baru di masa depan untuk wajib memiliki implementasi `hitung_diskon()`.

---

## 💾 Integrasi JSON
Proyek ini disiapkan untuk *File Handling* menggunakan `json`. Setiap class produk memiliki method `+to_dict()` untuk mengubah struktur *Object* Python menjadi format *Dictionary* yang kompatibel agar mudah ditulis (*dump*) ke dalam file `.json` oleh Class `Toko`.