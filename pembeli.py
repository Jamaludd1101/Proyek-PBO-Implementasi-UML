from produk import Produk


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
        if n <= 0:
            print("Jumlah barang harus lebih dari 0.")
            return

        # Cek dulu apakah produk sudah ada di keranjang
        for barang in self.__item:
            if barang["produk"].nama == produk.nama:
                # Cek stok MENGGUNAKAN TOTAL LAMA + BARU
                if not produk.cek_stok(barang["jumlah"] + n):
                    print(
                        f"Gagal: stok {produk.nama} tidak mencukupi. (Sisa stok: {produk.stok})"
                    )
                    return
                barang["jumlah"] += n
                print(
                    f"Jumlah {produk.nama} di keranjang diperbarui menjadi {barang['jumlah']}."
                )
                return

        # Jika belum ada, cek stok lalu masukkan sebagai barang baru
        if not produk.cek_stok(n):
            print(
                f"Gagal: stok {produk.nama} tidak mencukupi. (Sisa stok: {produk.stok})"
            )
            return
        self.__item.append({"produk": produk, "jumlah": n})
        print(f"{produk.nama} sebanyak {n} dimasukkan ke keranjang.")

    def hapus(self, produk: Produk):
        # Perlu mengecek apakah produk benar-benar ada di list
        ditemukan = False
        for barang in self.__item:
            if barang["produk"].nama == produk.nama:
                self.__item.remove(barang)
                ditemukan = True
                print(f"{produk.nama} berhasil dihapus dari keranjang.")
                break  # Segera keluar dari loop jika sudah ditemukan

        if not ditemukan:
            print(f"Gagal: {produk.nama} tidak ditemukan di keranjang.")

    def total_harga(self) -> int:
        total = 0
        for barang in self.__item:
            # harga_akhir() = harga setelah diskon produk (polimorfisme: beda tiap jenis produk)
            harga_satuan = barang["produk"].harga_akhir()
            total += harga_satuan * barang["jumlah"]
        return total

    def get_items(self) -> list:
        return self.__item

    def kosongkan(self):
        self.__item.clear()  # Lebih elegan menggunakan .clear() dari pada membuat list baru


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
