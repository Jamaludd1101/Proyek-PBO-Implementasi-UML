import json
from abc import ABC, abstractmethod

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

class Transaksi:
    def __init__(self, pembeli: Pembeli, voucher: Voucher = None):
        self.__pembeli = pembeli
        self.__keranjang = pembeli.keranjang # Agregasi dari pembeli
        self.__voucher = voucher

    def hitung_total(self) -> int:
        pass

    def cek_saldo(self) -> bool:
        pass

    def bayar(self) -> bool:
        pass

    def cetak_struk(self) -> dict:
        """Mengembalikan data struk untuk riwayat/JSON"""
        pass

class RiwayatTransaksi:
    def __init__(self):
        self.__daftar = []

    def tambah_riwayat(self, t: Transaksi):
        pass

    def tampilkan(self):
        pass
    
    def simpan_ke_json(self, filename="riwayat.json"):
        pass

# ==========================================
# BAGIAN 3: CLASS UTAMA (MAIN CONTROLLER)
# ==========================================

class Toko:
    def __init__(self, nama: str):
        self.__nama = nama
        self.__daftar_produk = []
        self.__riwayat = RiwayatTransaksi()

    def tambah_produk(self, p: Produk):
        self.__daftar_produk.append(p)

    def cari_produk(self, nama: str):
        pass

    def mulai_transaksi(self, pembeli: Pembeli):
        pass
        
    def simpan_database_json(self, filename="database_toko.json"):
        """Menyimpan seluruh data produk toko ke JSON"""
        data = [produk.to_dict() for produk in self.__daftar_produk]
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def muat_database_json(self, filename="database_toko.json"):
        """Memuat data JSON menjadi Object kembali"""
        pass

# Blok Eksekusi Utama
if __name__ == "__main__":
    minimarket = Toko("Minimarket Kita")
    print(f"Sistem {minimarket._Toko__nama} Siap Dijalankan.")