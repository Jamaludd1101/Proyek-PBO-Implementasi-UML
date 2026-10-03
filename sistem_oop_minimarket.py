import json
from abc import ABC, abstractmethod

# ==========================================
# BAGIAN 1: PRODUK & TURUNANNYA (ABSTRACTION & INHERITANCE)
# ==========================================


class Produk(ABC):
    def __init__(self, nama: str, harga: int, stok: int):
        self.__nama = nama  # Private attribute (-)
        self.__harga = harga  # Private attribute (-)
        self.__stok = stok  # Private attribute (-)

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

    def harga_akhir(self) -> int:
        return self.harga - self.hitung_diskon()

    def cek_stok(self, n: int) -> bool:
        return self.stok >= n

    def kurangi_stok(self, n: int):
        if self.cek_stok(n):
            self.__stok -= n

    def info(self) -> str:
        return f"{self.nama} - Rp{self.harga} (Stok: {self.stok})"

    def to_dict(self) -> dict:
        return {
            "kategori": self.__class__.__name__,
            "nama": self.__nama,
            "harga": self.__harga,
            "stok": self.__stok,
        }


class Makanan(Produk):
    def __init__(self, nama: str, harga: int, stok: int, kadaluarsa: str):
        super().__init__(nama, harga, stok)
        self.__kadaluarsa = kadaluarsa

    def hitung_diskon(self):
        return int((self.harga * 10) / 100)

    def info(self) -> str:
        return f"Makanan: {self.nama}, Harga: Rp{self.harga}, Stok: {self.stok}, Kadaluarsa: {self.__kadaluarsa}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["kadaluarsa"] = self.__kadaluarsa
        return data


class Mainan(Produk):
    def __init__(self, nama: str, harga: int, stok: int, rekomendasi_umur: int):
        super().__init__(nama, harga, stok)
        self.__rekomendasi_umur = rekomendasi_umur

    def hitung_diskon(self):
        return int((self.harga * 15) / 100)

    def info(self) -> str:
        return f"Mainan: {self.nama}, Harga: Rp{self.harga}, Stok: {self.stok}, Umur: {self.__rekomendasi_umur}+"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["rekomendasi_umur"] = self.__rekomendasi_umur
        return data


class Minuman(Produk):
    def __init__(self, nama: str, harga: int, stok: int, ukuran_ml: int):
        super().__init__(nama, harga, stok)
        self.__ukuran_ml = ukuran_ml

    def hitung_diskon(self):
        return int((self.harga * 20) / 100)

    def info(self) -> str:
        return f"Minuman: {self.nama}, Harga: Rp{self.harga}, Stok: {self.stok}, Ukuran: {self.__ukuran_ml}ml"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["ukuran_ml"] = self.__ukuran_ml
        return data


class Elektronik(Produk):
    def __init__(self, nama: str, harga: int, stok: int, garansi_bulan: int):
        super().__init__(nama, harga, stok)
        self.__garansi_bulan = garansi_bulan

    def hitung_diskon(self):
        return int((self.harga * 5) / 100)

    def info(self) -> str:
        return f"Elektronik: {self.nama}, Harga: Rp{self.harga}, Stok: {self.stok}, Garansi: {self.__garansi_bulan} bulan"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["garansi_bulan"] = self.__garansi_bulan
        return data


class Pakaian(Produk):
    def __init__(self, nama: str, harga: int, stok: int, ukuran: str, bahan: str):
        super().__init__(nama, harga, stok)
        self.__ukuran = ukuran
        self.__bahan = bahan

    def hitung_diskon(self):
        # Diskon 20%
        return int((self.harga * 20) / 100)

    def info(self) -> str:
        return f"Pakaian: {self.nama}, Harga: Rp{self.harga}, Stok: {self.stok}, Ukuran: {self.__ukuran}, Bahan: {self.__bahan}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["ukuran"] = self.__ukuran
        data["bahan"] = self.__bahan
        return data


# ==========================================
# BAGIAN 2: SISTEM TRANSAKSI & PENGGUNA (ENCAPSULATION)
# ==========================================


class Voucher:
    def __init__(self, kode: str, potongan: int):
        self.__kode = kode
        self.__potongan = potongan

    @property
    def kode(self) -> str:
        return self.__kode

    def berlaku(self, total: int) -> bool:
        # Voucher hanya bisa digunakan jika total belanja >= potongannya
        return total >= self.__potongan

    def terapkan(self, total: int) -> int:
        if self.berlaku(total):
            return total - self.__potongan
        return total


class Keranjang:
    def __init__(self):
        # List of dictionary agar mudah memisahkan produk & kuantitas
        self.__item = []

    def tambah(self, produk: Produk, n: int):
        # Cek dulu apakah produk sudah ada di keranjang
        for barang in self.__item:
            if barang["produk"].nama == produk.nama:
                if not produk.cek_stok(barang["jumlah"] + n):
                    print(f"Gagal: stok {produk.nama} tidak mencukupi.")
                    return
                barang["jumlah"] += n
                print(
                    f"Jumlah {produk.nama} di keranjang diperbarui menjadi {barang['jumlah']}."
                )
                return

        # Jika belum ada, cek stok lalu masukkan sebagai barang baru
        if not produk.cek_stok(n):
            print(f"Gagal: stok {produk.nama} tidak mencukupi.")
            return
        self.__item.append({"produk": produk, "jumlah": n})
        print(f"{produk.nama} sebanyak {n} dimasukkan ke keranjang.")

    def hapus(self, produk: Produk):
        for barang in self.__item:
            if barang["produk"].nama == produk.nama:
                self.__item.remove(barang)
                print(f"{produk.nama} berhasil dihapus dari keranjang.")
                return
        print(f"Gagal: {produk.nama} tidak ditemukan di keranjang.")

    def total_harga(self) -> int:
        total = 0
        for barang in self.__item:
            # Catatan: Saat ini menggunakan harga asli (produk.harga).
            # Jika teman Anda yang mengerjakan class Produk sudah menyelesaikan method harga_akhir()
            # (yang sudah dipotong diskon), Anda bisa menggantinya menjadi produk.harga_akhir()
            harga_satuan = barang["produk"].harga
            total += harga_satuan * barang["jumlah"]
        return total

    def get_items(self) -> list:
        return self.__item

    def kosongkan(self):
        self.__item = []


class Pembeli:
    def __init__(self, nama: str, saldo: int):
        self.__nama = nama
        self.__saldo = saldo
        # Relasi Komposisi (Pembeli memiliki keranjang sepenuhnya)
        self.__keranjang = Keranjang()

    @property
    def keranjang(self) -> Keranjang:
        return self.__keranjang

    @property
    def nama(self) -> str:
        return self.__nama

    @property
    def saldo(self) -> int:
        return self.__saldo

    def tambah_ke_keranjang(self, produk: Produk, n: int):
        self.__keranjang.tambah(produk, n)

    def kurangi_saldo(self, n: int) -> bool:
        if self.__saldo >= n:
            self.__saldo -= n
            print(
                f"Saldo berhasil dipotong. Sisa saldo {self.__nama}: Rp{self.__saldo}"
            )
            return True
        print(
            f"Transaksi gagal: Saldo {self.__nama} tidak mencukupi! "
            f"(Saldo: Rp{self.__saldo}, Tagihan: Rp{n})"
        )
        return False


class Transaksi:
    def __init__(self, pembeli: Pembeli, voucher: Voucher = None):
        self.__pembeli = pembeli
        self.__keranjang = pembeli.keranjang  # Agregasi dari pembeli
        self.__voucher = voucher

    def hitung_total(self) -> int:
        total = self.__keranjang.total_harga()
        if self.__voucher:
            total = self.__voucher.terapkan(total)
        return total

    def cek_saldo(self) -> bool:
        return self.__pembeli.saldo >= self.hitung_total()

    def bayar(self) -> bool:
        items = self.__keranjang.get_items()
        if not items:
            print("Keranjang kosong.")
            return False

        total = self.hitung_total()
        if not self.__pembeli.kurangi_saldo(total):
            return False

        # Stok baru dikurangi setelah pembayaran berhasil
        for barang in items:
            barang["produk"].kurangi_stok(barang["jumlah"])
        return True

    def cetak_struk(self) -> dict:
        """Mengembalikan data struk untuk riwayat/JSON"""
        return {
            "pembeli": self.__pembeli.nama,
            "items": [
                (b["produk"].nama, b["jumlah"]) for b in self.__keranjang.get_items()
            ],
            "total": self.hitung_total(),
        }


class RiwayatTransaksi:
    def __init__(self):
        self.__daftar = []

    def tambah_riwayat(self, t: Transaksi):
        self.__daftar.append(t.cetak_struk())

    def tampilkan(self):
        for r in self.__daftar:
            print(r)

    def simpan_ke_json(self, filename="riwayat.json"):
        with open(filename, "w") as f:
            json.dump(self.__daftar, f, indent=4)


# ==========================================
# BAGIAN 3: CLASS UTAMA (MAIN CONTROLLER)
# ==========================================


class Toko:
    def __init__(self, nama: str):
        self.__nama = nama
        self.__daftar_produk = []
        self.__riwayat = RiwayatTransaksi()

    @property
    def nama(self):
        return self.__nama

    @property
    def riwayat(self) -> RiwayatTransaksi:
        return self.__riwayat

    def tambah_produk(self, p: Produk):
        self.__daftar_produk.append(p)

    def cari_produk(self, nama: str):
        for p in self.__daftar_produk:
            if p.nama.lower() == nama.lower():
                return p
        return None

    def mulai_transaksi(self, pembeli: Pembeli, voucher: Voucher = None):
        transaksi = Transaksi(pembeli, voucher)
        if transaksi.bayar():
            struk = transaksi.cetak_struk()  # cetak sebelum keranjang dikosongkan
            self.__riwayat.tambah_riwayat(transaksi)
            pembeli.keranjang.kosongkan()
            return struk
        return None

    def simpan_database_json(self, filename="database_toko.json"):
        data = [produk.to_dict() for produk in self.__daftar_produk]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def muat_database_json(self, filename="database_toko.json"):
        """Memuat data JSON menjadi Object kembali"""
        with open(filename, "r") as file:
            data = json.load(file)

        self.__daftar_produk = []
        for d in data:
            kategori = d["kategori"]
            if kategori == "Makanan":
                p = Makanan(d["nama"], d["harga"], d["stok"], d["kadaluarsa"])
            elif kategori == "Mainan":
                p = Mainan(d["nama"], d["harga"], d["stok"], d["rekomendasi_umur"])
            elif kategori == "Minuman":
                p = Minuman(d["nama"], d["harga"], d["stok"], d["ukuran_ml"])
            elif kategori == "Elektronik":
                p = Elektronik(d["nama"], d["harga"], d["stok"], d["garansi_bulan"])
            elif kategori == "Pakaian":
                p = Pakaian(d["nama"], d["harga"], d["stok"], d["ukuran"], d["bahan"])
            else:
                continue
            self.__daftar_produk.append(p)


# Blok Eksekusi Utama
if __name__ == "__main__":
    minimarket = Toko("Minimarket Kita")
    print(f"Sistem {minimarket.nama} Siap Dijalankan.")