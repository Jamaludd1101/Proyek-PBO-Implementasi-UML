import json
from datetime import datetime

from pembeli import Pembeli, Voucher
from produk import Mainan, Makanan, Minuman, Produk

MENU_BELANJA = """
--- Menu Belanja ---
1. Lihat produk
2. Tambah ke keranjang
3. Lihat keranjang
4. Hapus dari keranjang
5. Pakai voucher
6. Bayar
0. Kembali"""


def format_struk(s: dict) -> str:
    """Ubah dict struk menjadi teks yang rapi."""
    baris = [f"[{s['waktu']}] Pembeli: {s['pembeli']}"]
    for it in s["items"]:
        baris.append(
            f"  {it['nama']} x{it['qty']} @ Rp{it['harga_satuan']} = Rp{it['subtotal']}"
        )
    baris.append(f"  Subtotal    : Rp{s['subtotal']}")
    if s["potongan"] > 0:
        baris.append(f"  Potongan    : -Rp{s['potongan']}")
    baris.append(f"  TOTAL BAYAR : Rp{s['total_bayar']}")
    return "\n".join(baris)


class Transaksi:
    def __init__(self, pembeli: Pembeli, voucher: Voucher = None):
        self.__pembeli = pembeli
        self.__keranjang = pembeli.keranjang  # Agregasi dari pembeli
        self.__voucher = voucher
        self.__struk = None  # terisi setelah bayar() berhasil

    def hitung_total(self) -> int:
        total = self.__keranjang.total_harga()
        if self.__voucher:
            total = self.__voucher.terapkan(
                total
            )  # terapkan() sudah mengecek syarat voucher
        return total

    def cek_saldo(self) -> bool:
        return self.__pembeli.saldo >= self.hitung_total()

    def bayar(self) -> bool:
        items = self.__keranjang.get_items()

        # 1) Cek semua syarat dulu (data belum diubah sama sekali)
        if not items:
            print("Keranjang masih kosong.")
            return False
        for barang in items:
            if not barang["produk"].cek_stok(barang["jumlah"]):
                print(f"Stok {barang['produk'].nama} tidak cukup.")
                return False
        if not self.cek_saldo():
            print("Saldo tidak cukup.")
            return False

        # 2) Semua syarat terpenuhi -> baru ubah data
        self.__struk = self.cetak_struk()  # simpan struk SEBELUM keranjang dikosongkan
        self.__pembeli.kurangi_saldo(self.hitung_total())
        for barang in items:
            barang["produk"].kurangi_stok(barang["jumlah"])
        self.__keranjang.kosongkan()
        return True

    def cetak_struk(self) -> dict:
        """Struk final kalau sudah dibayar, atau pratinjau kalau belum."""
        if self.__struk:
            return self.__struk
        daftar_item = []
        for barang in self.__keranjang.get_items():
            produk, qty = barang["produk"], barang["jumlah"]
            daftar_item.append(
                {
                    "nama": produk.nama,
                    "qty": qty,
                    "harga_satuan": produk.harga_akhir(),
                    "subtotal": produk.harga_akhir() * qty,
                }
            )
        subtotal = self.__keranjang.total_harga()
        total = self.hitung_total()
        return {
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pembeli": self.__pembeli.nama,
            "items": daftar_item,
            "subtotal": subtotal,
            "potongan": subtotal - total,
            "total_bayar": total,
        }


class RiwayatTransaksi:
    def __init__(self):
        self.__daftar = []  # isinya dict struk, bukan objek Transaksi

    def tambah_riwayat(self, t: Transaksi):
        self.__daftar.append(t.cetak_struk())

    def tampilkan(self):
        if not self.__daftar:
            print("Belum ada riwayat transaksi.")
        for i, struk in enumerate(self.__daftar, start=1):
            print(f"--- Transaksi #{i} ---")
            print(format_struk(struk))

    def simpan_ke_json(self, filename="riwayat.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.__daftar, f, indent=4, ensure_ascii=False)

    def muat_dari_json(self, filename="riwayat.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.__daftar = json.load(f)
        except FileNotFoundError:
            pass  # belum ada file = riwayat kosong


class Toko:
    def __init__(self, nama: str):
        self.__nama = nama
        self.__daftar_produk = []
        self.__riwayat = RiwayatTransaksi()
        self.__riwayat.muat_dari_json()
        # Voucher yang tersedia, tambahkan di sini
        self.__daftar_voucher = {"HEMAT5K": Voucher("HEMAT5K", 5000)}

    @property
    def nama(self) -> str:
        return self.__nama

    @property
    def daftar_produk(self):
        return self.__daftar_produk

    # ---------- Produk ----------
    def tambah_produk(self, p: Produk):
        self.__daftar_produk.append(p)

    def tambah_produk_interaktif(self):
        kategori = input("Kategori (makanan/mainan/minuman): ").strip().lower()
        if kategori not in ("makanan", "mainan", "minuman"):
            print("Kategori tidak dikenal.")
            return
        nama = input("Nama produk: ").strip()
        if nama == "" or self.cari_produk(nama):
            print("Nama kosong atau produk sudah ada.")
            return
        try:
            harga = int(input("Harga: "))
            stok = int(input("Stok: "))
            if harga <= 0 or stok < 0:
                print("Harga harus lebih dari 0 dan stok tidak boleh negatif.")
                return
            if kategori == "makanan":
                p = Makanan(nama, harga, stok, input("Tanggal kadaluarsa: "))
            elif kategori == "mainan":
                p = Mainan(nama, harga, stok, int(input("Rekomendasi umur: ")))
            else:
                p = Minuman(nama, harga, stok, int(input("Ukuran (ml): ")))
        except ValueError:
            print("Input angka tidak valid.")
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
            print("Belum ada produk.")
        for i, p in enumerate(self.__daftar_produk, start=1):
            # info() beda tiap jenis produk (polimorfisme)
            print(f"{i}. {p.info()} | Setelah diskon: Rp{p.harga_akhir()}")

    def __minta_produk(self):
        """Tanya nama produk ke pengguna, kembalikan produknya (atau None)."""
        produk = self.cari_produk(input("Nama produk: "))
        if produk is None:
            print("Produk tidak ditemukan.")
        return produk

    # ---------- Transaksi ----------
    def mulai_transaksi(self, pembeli: Pembeli):
        voucher = None
        while True:
            print(MENU_BELANJA)
            pilih = input("Pilih: ").strip()

            if pilih == "1":
                self.tampilkan_produk()

            elif pilih == "2":
                produk = self.__minta_produk()
                if produk:
                    try:
                        n = int(input("Jumlah: "))
                    except ValueError:
                        n = 0
                    if n > 0:
                        pembeli.tambah_ke_keranjang(
                            produk, n
                        )  # stok dicek di Keranjang.tambah()
                    else:
                        print("Jumlah harus angka lebih dari 0.")

            elif pilih == "3":
                items = pembeli.keranjang.get_items()
                if not items:
                    print("Keranjang kosong.")
                else:
                    for barang in items:
                        print(f"- {barang['produk'].nama} x{barang['jumlah']}")
                    print(
                        f"Total saat ini: Rp{Transaksi(pembeli, voucher).hitung_total()}"
                    )

            elif pilih == "4":
                produk = self.__minta_produk()
                if produk:
                    pembeli.keranjang.hapus(produk)

            elif pilih == "5":
                voucher_baru = self.__daftar_voucher.get(
                    input("Kode voucher: ").strip().upper()
                )
                if voucher_baru:
                    voucher = voucher_baru
                    print("Voucher dipasang.")
                else:
                    print("Voucher tidak ditemukan.")

            elif pilih == "6":
                transaksi = Transaksi(pembeli, voucher)
                if transaksi.bayar():
                    self.__riwayat.tambah_riwayat(transaksi)
                    self.__riwayat.simpan_ke_json()
                    self.simpan_database_json()  # simpan stok terbaru
                    print("\nPembayaran berhasil!")
                    print(format_struk(transaksi.cetak_struk()))
                    break

            elif pilih == "0":
                break

            else:
                print("Pilihan tidak valid.")

    def tampilkan_riwayat(self):
        self.__riwayat.tampilkan()

    # ---------- Database JSON ----------
    def simpan_database_json(self, filename="database_toko.json"):
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
        self.__daftar_produk = []
        for d in data:
            if d["kategori"] == "Makanan":
                p = Makanan(d["nama"], d["harga"], d["stok"], d["kadaluarsa"])
            elif d["kategori"] == "Mainan":
                p = Mainan(d["nama"], d["harga"], d["stok"], d["rekomendasi_umur"])
            elif d["kategori"] == "Minuman":
                p = Minuman(d["nama"], d["harga"], d["stok"], d["ukuran_ml"])
            else:
                continue
            self.__daftar_produk.append(p)
