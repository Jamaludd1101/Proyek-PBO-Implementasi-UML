from flask import Flask, jsonify, render_template, request

# TAMBAHKAN IMPORT INI
from produk import Mainan, Makanan, Minuman
from toko import Toko

app = Flask(__name__)

toko = Toko("Minimarket OOP")
toko.muat_database_json("database_toko.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/produk", methods=["GET"])
def get_produk():
    data_produk = []
    for produk in toko.daftar_produk:
        item = produk.to_dict()
        item["id_produk"] = produk.nama
        data_produk.append(item)
    return jsonify(data_produk)


@app.route("/api/checkout", methods=["POST"])
def checkout():
    data_transaksi = request.json
    keranjang_frontend = data_transaksi.get("keranjang", [])

    for item in keranjang_frontend:
        nama_produk = item.get("id_produk")
        jumlah_beli = item.get("jumlah", 1)
        produk = toko.cari_produk(nama_produk)
        if produk:
            produk.kurangi_stok(jumlah_beli)

    toko.simpan_database_json("database_toko.json")

    return jsonify({"status": "sukses", "pesan": "Transaksi berhasil diproses."})


# --- TAMBAHKAN BLOK API BARU INI UNTUK MENERIMA PRODUK DARI WEB ---
@app.route("/api/tambah_produk", methods=["POST"])
def tambah_produk():
    data = request.json
    kategori = data.get("kategori")
    nama = data.get("nama")

    try:
        harga = int(data.get("harga", 0))
        stok = int(data.get("stok", 0))
    except ValueError:
        return jsonify({"status": "gagal", "pesan": "Harga dan Stok harus angka."})

    if not nama or harga <= 0 or stok < 0:
        return jsonify({"status": "gagal", "pesan": "Data tidak lengkap/valid."})

    if toko.cari_produk(nama):
        return jsonify(
            {"status": "gagal", "pesan": "Produk dengan nama tersebut sudah ada."}
        )

    # Membuat object sesuai kategorinya (Polymorphism)
    if kategori == "makanan":
        p = Makanan(nama, harga, stok, data.get("extra", ""))
    elif kategori == "mainan":
        p = Mainan(nama, harga, stok, int(data.get("extra", 0)))
    elif kategori == "minuman":
        p = Minuman(nama, harga, stok, int(data.get("extra", 0)))
    else:
        return jsonify({"status": "gagal", "pesan": "Kategori tidak dikenal."})

    # Masukkan ke object toko dan simpan ke JSON
    toko.tambah_produk(p)
    toko.simpan_database_json("database_toko.json")

    return jsonify(
        {"status": "sukses", "pesan": f"Produk {nama} berhasil ditambahkan!"}
    )


if __name__ == "__main__":
    app.run(debug=True)
