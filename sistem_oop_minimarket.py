import json
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# BAGIAN 1: PRODUK & TURUNANNYA (ABSTRACTION & INHERITANCE)
# ==========================================

class Produk(ABC):
    def __init__(self, nama: str, harga: int, stok: int):
        self.__nama = nama       # Private attribute (-)
        self.__harga = harga     # Private attribute (-)
        self.__stok = stok       # Private attribute (-)

    # Protected/Public property agar subclass bisa mengakses harga untuk hitung diskon
    @property
    def harga(self) -> int:
        return self.__harga

    @property
    def nama(self) -> str:
        return self.__nama
    
    @property
    def stok(self) -> int:
        return self.__stok

    @abstractmethod
    def hitung_diskon(self):
        """Method abstrak (Polymorphism)"""
        pass

    def harga_akhir(self) -> int:
        pass

    def cek_stok(self, n: int) -> bool:
        pass

    def kurangi_stok(self, n: int):
        pass

    def info(self) -> str:
        pass

    def to_dict(self) -> dict:
        """Kerangka untuk konversi ke JSON"""
        return {
            "kategori": self.__class__.__name__,
            "nama": self.__nama,
            "harga": self.__harga,
            "stok": self.__stok
        }

class Makanan(Produk):
    def __init__(self, nama: str, harga: int, stok: int, kadaluarsa: str):
        super().__init__(nama, harga, stok)
        self.__kadaluarsa = kadaluarsa

    def hitung_diskon(self):
        # Diskon 10%
        pass

    def info(self) -> str:
        pass

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["kadaluarsa"] = self.__kadaluarsa
        return data

class Mainan(Produk): 
    def __init__(self, nama: str, harga: int, stok: int, rekomendasi_umur: int):
        super().__init__(nama, harga, stok)
        self.__rekomendasi_umur = rekomendasi_umur 

    def hitung_diskon(self):
        # Diskon 5%
        pass

    def info(self) -> str:
        pass

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["rekomendasi_umur"] = self.__rekomendasi_umur
        return data

class Minuman(Produk): 
    def __init__(self, nama: str, harga: int, stok: int, ukuran_ml: int):
        super().__init__(nama, harga, stok)
        self.__ukuran_ml = ukuran_ml 

    def hitung_diskon(self):
        # Diskon 20%
        pass

    def info(self) -> str:
        pass

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["ukuran_ml"] = self.__ukuran_ml
        return data


# ==========================================
# BAGIAN 2: SISTEM TRANSAKSI & PENGGUNA (ENCAPSULATION)
# ==========================================

class Voucher:
    def __init__(self, kode: str, potongan: int):
        self.__kode = kode
        self.__potongan = potongan

    def berlaku(self, total: int) -> bool:
        pass

    def terapkan(self, total: int) -> int:
        pass

class Keranjang:
    def __init__(self):
        self.__item = [] # List of dict/tuples (Produk, qty)

    def tambah(self, produk: Produk, n: int):
        pass

    def hapus(self, produk: Produk):
        pass

    def total_harga(self) -> int:
        pass

    def get_items(self) -> list:
        return self.__item

class Pembeli:
    def __init__(self, nama: str, saldo: int):
        self.__nama = nama
        self.__saldo = saldo
        self.__keranjang = Keranjang() # Relasi Komposisi

    @property
    def keranjang(self) -> Keranjang:
        return self.__keranjang

    @property
    def nama(self) -> str:
        return self.__nama

    def tambah_ke_keranjang(self, produk: Produk, n: int):
        pass

    def kurangi_saldo(self, n: int):
        pass


#Format struk
def format_struk(s: dict) -> str:
    """Mengubah dict struk menjadi teks rapi (dipakai Toko dan RiwayatTransaksi)."""
    baris = [f"[{s['waktu']}] Pembeli: {s['pembeli']}"]
    for it in s["items"]:
        baris.append(f"  {it['nama']} x{it['qty']} @ Rp{it['harga_satuan']} = Rp{it['subtotal']}")
    baris.append(f"  Subtotal      : Rp{s['subtotal']}")
    if s["potongan"] > 0:
        baris.append(f"  Potongan      : -Rp{s['potongan']}")
    baris.append(f"  TOTAL BAYAR   : Rp{s['total_bayar']}")
    return "\n".join(baris)
 
class Transaksi:
    def __init__(self, pembeli: Pembeli, voucher: Voucher = None):
        self.__pembeli = pembeli
        self.__keranjang = pembeli.keranjang  # Agregasi dari pembeli
        self.__voucher = voucher
        self.__struk = None                   # diisi setelah bayar() berhasil
 
    def hitung_total(self) -> int:
        total = self.__keranjang.total_harga()
        # Voucher hanya dipakai kalau ada DAN syaratnya terpenuhi
        if self.__voucher is not None and self.__voucher.berlaku(total):
            total = self.__voucher.terapkan(total)
        return total
 
    def cek_saldo(self) -> bool:
        return self.__pembeli.saldo >= self.hitung_total()
 
    def __buat_struk(self, total: int) -> dict:
        subtotal = self.__keranjang.total_harga()
        daftar_item = []
        for produk, qty in self.__keranjang.get_items():
            harga_satuan = produk.harga_akhir()
            daftar_item.append({
                "nama": produk.nama,
                "qty": qty,
                "harga_satuan": harga_satuan,
                "subtotal": harga_satuan * qty,
            })
        return {
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pembeli": self.__pembeli.nama,
            "items": daftar_item,
            "subtotal": subtotal,
            "potongan": subtotal - total,
            "total_bayar": total,
        }
 
    def bayar(self) -> bool:
        items = self.__keranjang.get_items()
 
        # 1) VALIDASI dulu semuanya, belum mengubah data apa pun
        if not items:
            print("Keranjang masih kosong.")
            return False
        for produk, qty in items:
            if not produk.cek_stok(qty):
                print(f"Stok {produk.nama} tidak cukup.")
                return False
        if not self.cek_saldo():
            print("Saldo tidak cukup.")
            return False
 
        # 2) Semua aman -> baru ubah data
        total = self.hitung_total()
        struk = self.__buat_struk(total)   # harus dibuat SEBELUM keranjang dikosongkan
        self.__pembeli.kurangi_saldo(total)
        for produk, qty in items:
            produk.kurangi_stok(qty)
        self.__struk = struk
        items.clear()                      # kosongkan keranjang (lihat catatan di chat)
        return True
 
    def cetak_struk(self) -> dict:
        """Struk final kalau sudah dibayar, atau pratinjau kalau belum."""
        if self.__struk is None:
            return self.__buat_struk(self.hitung_total())
        return self.__struk
 
class RiwayatTransaksi:
    def __init__(self):
        self.__daftar = []

    def tambah_riwayat(self, t: Transaksi):
        self.__daftar.append(t.cetak_struk())


    def tampilkan(self):
        if not self.__daftar:
            print("Belum ada riwayat transaksi")
            return
        for i, struk in enumerate(self.__daftar, start=1):
            print(f"--- Transaksu #{i} ---")
            print(format_struk(struk))
    
    
    def simpan_ke_json(self, filename="riwayat.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.__daftar, f, indent=4, ensure_ascii=False)
 
    def muat_dari_json(self, filename="riwayat.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.__daftar = json.load(f)
        except FileNotFoundError:
            pass   # belum ada file = riwayat kosong, tidak masalah
 

# ==========================================
# BAGIAN 3: CLASS UTAMA (MAIN CONTROLLER)
# ==========================================

class Toko:
    def __init__(self, nama: str):
        self.__nama = nama
        self.__daftar_produk = []
        self.__riwayat = RiwayatTransaksi()
        self.__riwayat.muat_dari_json()

        #voucher yang tersedia bisa tambahkan disini
        self.__daftar_voucher = {
            "HEMAT5K": Voucher("HEMAT5K", 5000)
        }

    @property
    def nama(self) -> str:
        return self.__nama

    def tambah_produk(self, p: Produk):
        self.__daftar_produk.append(p)

    def tambah_produk_interaktif(self):
        kategori = input("Kategori (makanan/mainan/minuman): ").strip().lower()

        nama  = input("Nama produk: ").strip()
        try:
            harga = int(input("Harga: "))
            stok = int(input("Stok: "))
            if kategori == "makanan":
                p = Makanan(nama, harga, stok, input("Tanggal kadaluarsa: "))

            elif kategori == "mainan":
                p = Mainan(nama, harga, stok, int("Rekomendasi umur: "))

            elif kategori == "minuman":
                p = Minuman(nama, harga, stok, int(input("Ukuran (ml): ")))
            else:
                print("Kategori tidak dikenal")
                return
        except ValueError:
            print("Input angka tidak valid")
            return
        self.tambah_produk(p)
        self.simpan_database_json()
        print(f"Produk '{nama}' ditambahkan.")


    def cari_produk(self, nama: str):
        for p in self.__daftar_produk:
            if p.nama.lower() == nama.strip().lower():
                return p
        return None

    def tampilkan_produk(self):
        if not self.__daftar_produk:
            print("belum ada produk.")
            return
        for i, p in enumerate(self.__daftar_produk, start=1):
            print(f"{i}. {p.nama} - Rp(p.harga) (stok{p.stok})")

    def __tampilkan_keranjang(self, pembeli: Pembeli, voucher):
        items = pembeli.keranjang.get_items()
        if not items:
            print("Keranjang kosong.")
            return
        for produk, qty in items:
            print(f"- {produk.nama} x{qty}")
        print(f"Total saat ini: Rp{Transaksi(pembeli, voucher).hitung_total()}")


    def mulai_transaksi(self, pembeli: Pembeli):
        voucher = None;
        while True:
            print("\n--- Menu Belanja ---")
            print("1. Lihat produk")
            print("2. Tambah ke keranjang")
            print("3. Lihat keranjang")
            print("4. Pakai voucher")
            print("5. Bayar")
            print("0. Kembali")
            pilih = input("Pilih: ").strip()

            if pilih == "1":
                self.tampilkan_produk()

            elif pilih == "2":
                produk = self.cari_produk(input("Nam produk: "))
                if produk is None:
                    print("Produk tidak ditemukan.")
                    continue
                try:
                    n = int(input("Jumlah: "))
                except ValueError:
                    print("Jumlah harus angka.")
                    continue
                if n <= 0 or not produk.cek_stok(n):
                    print("Jumlah tidak valid atau stok tidak cukup.")
                    continue
                pembeli.tambah_ke_keranjang(produk, n)
                print(f"{produk.nama} x{n} masuk keranjang")

            elif pilih == "3":
                self.__tampilkan_keranjang(pembeli, voucher)

            elif pilih == "4":
                kode = input("Kode voucher: ").strip().upper()
                v = self.__daftar_voucher.get(kode)
                if v is None:
                    print("Voucher tidak ditemukan.")
                else:
                    voucher = v
                    print("voucher dipasang.")

            elif pilih == "5":
                transaksi = Transaksi(pembeli, voucher)
                if transaksi.bayar():
                    self.__riwayat.tambah_riwayat(transaksi)
                    self.__riwayat.simpan_ke_json()
                    self.simpan_database_json()
                    print("\nPembayarn berhasil!")
                    print(format_struk(transaksi.cetak_struk()))

            elif pilih == "0":
                break

            else:
                print("Pilihan tidak valid.")

    def tampilkan_riwayat(self):
        self.__riwayat.tampilkan()

    def simpan_database_json(self, filename="database_toko.json"):
        """Menyimpan seluruh data produk toko ke JSON"""
        data = [produk.to_dict() for produk in self.__daftar_produk]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
 
    def muat_database_json(self, filename="database_toko.json"):
        """Memuat data JSON menjadi objek Produk kembali"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Database belum ada, mulai dari kosong.")
            return
        self.__daftar_produk.clear()
        for d in data:
            kategori = d["kategori"]
            if kategori == "Makanan":
                p = Makanan(d["nama"], d["harga"], d["stok"], d["kadaluarsa"])
            elif kategori == "Mainan":
                p = Mainan(d["nama"], d["harga"], d["stok"], d["rekomendasi_umur"])
            elif kategori == "Minuman":
                p = Minuman(d["nama"], d["harga"], d["stok"], d["ukuran_ml"])
            else:
                print(f"Kategori '{kategori}' tidak dikenal, dilewati.")
                continue
            self.__daftar_produk.append(p)
 

# Blok Eksekusi Utama
if __name__ == "__main__":
    minimarket = Toko("Minimarket Kita")
    minimarket.muat_database_json()
    print(f"Sistem {minimarket.nama} siap dijalankan.")
 
    nama = input("Nama pembeli: ")
    saldo = int(input("Saldo awal: "))
    pembeli = Pembeli(nama, saldo)
 
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Tambah produk")
        print("2. Lihat produk")
        print("3. Cari produk")
        print("4. Mulai belanja")
        print("5. Riwayat transaksi")
        print("0. Keluar")
        pilihan = input("Pilih opsi: ").strip()
 
        match pilihan:
            case "1":
                minimarket.tambah_produk_interaktif()
            case "2":
                minimarket.tampilkan_produk()
            case "3":
                p = minimarket.cari_produk(input("Cari produk: "))
                print(f"{p.nama} - Rp{p.harga} (stok: {p.stok})" if p else "Produk tidak ditemukan.")
            case "4":
                minimarket.mulai_transaksi(pembeli)
            case "5":
                minimarket.tampilkan_riwayat()
            case "0":
                print("Terima kasih!")
                break
            case _:
                print("Pilihan tidak valid.")