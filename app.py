from flask import Flask, jsonify, render_template, request

from toko import Toko

app = Flask(__name__)

# Inisialisasi sistem toko
toko = Toko("Minimarket OOP")
toko.muat_database_json("database_toko.json")


@app.route("/")
def index():
    # Sesuai dengan nama asli file HTML
    return render_template("index.html")


@app.route("/api/produk", methods=["GET"])
def get_produk():
    # Menggunakan to_dict() bawaan dari class Produk agar atribut
    # khusus (kadaluarsa, ukuran_ml, umur) otomatis ikut terbaca
    data_produk = []
    for produk in toko.daftar_produk:
        item = produk.to_dict()
        # Frontend JS membutuhkan properti id_produk, kita gunakan namanya saja
        item["id_produk"] = produk.nama
        data_produk.append(item)
    return jsonify(data_produk)


@app.route("/api/checkout", methods=["POST"])
def checkout():
    data_transaksi = request.json
    keranjang_frontend = data_transaksi.get("keranjang", [])

    # Logika sinkronisasi: Kurangi stok langsung dari object produk di memory
    for item in keranjang_frontend:
        nama_produk = item.get(
            "id_produk"
        )  # Di JS kita menggunakan nama sebagai id_produk
        jumlah_beli = item.get("jumlah", 1)

        # Cari produk dan kurangi stoknya
        produk = toko.cari_produk(nama_produk)
        if produk:
            produk.kurangi_stok(jumlah_beli)

    # Simpan perubahan stok ke database asli
    toko.simpan_database_json("database_toko.json")

    return jsonify({"status": "sukses", "pesan": "Transaksi berhasil diproses."})


if __name__ == "__main__":
    app.run(debug=True)
