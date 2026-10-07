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
        return int((self.harga * 5) / 100)

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
