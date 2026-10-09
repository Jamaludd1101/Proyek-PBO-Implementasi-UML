from pembeli import Pembeli
from toko import Toko


def input_angka(pesan: str) -> int:
    """Minta input sampai pengguna mengisi angka bulat >= 0."""
    while True:
        try:
            nilai = int(input(pesan))
            if nilai >= 0:
                return nilai
            print("Angka tidak boleh negatif.")
        except ValueError:
            print("Masukkan angka yang valid.")


# Blok Eksekusi Utama
if __name__ == "__main__":
    minimarket = Toko("Minimarket Kita")
    minimarket.muat_database_json()
    print(f"Sistem {minimarket.nama} siap dijalankan.")

    nama = input("Nama pembeli: ").strip()
    saldo = input_angka("Saldo awal: ")
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

        if pilihan == "1":
            minimarket.tambah_produk_interaktif()
        elif pilihan == "2":
            minimarket.tampilkan_produk()
        elif pilihan == "3":
            p = minimarket.cari_produk(input("Cari produk: "))
            print(p.info() if p else "Produk tidak ditemukan.")
        elif pilihan == "4":
            minimarket.mulai_transaksi(pembeli)
        elif pilihan == "5":
            minimarket.tampilkan_riwayat()
        elif pilihan == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")
