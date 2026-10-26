import os
import sqlite3
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "medis_monolit.db")
PORT = int(os.environ.get("PORT", 5000))

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pasien (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nik TEXT NOT NULL UNIQUE,
                nama TEXT NOT NULL,
                tgl_lahir TEXT NOT NULL,
                riwayat_alergi TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS obat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode TEXT NOT NULL UNIQUE,
                nama_obat TEXT NOT NULL,
                stok INTEGER NOT NULL,
                satuan TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pasien_id INTEGER NOT NULL,
                obat_id INTEGER NOT NULL,
                jumlah INTEGER NOT NULL,
                aturan_pakai TEXT NOT NULL,
                tgl_resep TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pasien_id) REFERENCES pasien(id),
                FOREIGN KEY (obat_id) REFERENCES obat(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dokter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                spesialisasi TEXT NOT NULL,
                hari_praktik TEXT NOT NULL,
                jam_praktik TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS janji_temu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pasien_id INTEGER NOT NULL,
                dokter_id INTEGER NOT NULL,
                tgl_periksa TEXT NOT NULL,
                keluhan TEXT,
                status TEXT DEFAULT 'TERDAFTAR',
                FOREIGN KEY (pasien_id) REFERENCES pasien(id),
                FOREIGN KEY (dokter_id) REFERENCES dokter(id)
            )
        """)
        conn.commit()

        # Seed data jika masih kosong
        cursor.execute("SELECT COUNT(*) FROM pasien")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO pasien (nik, nama, tgl_lahir, riwayat_alergi)
                VALUES (?, ?, ?, ?)
            """, [
                ("3578010101900001", "Pasien Contoh 01", "1990-05-12", "Penisilin"),
                ("3578010202920002", "Pasien Contoh 02", "1992-08-20", "Tidak Ada"),
                ("3578010303850003", "Pasien Contoh 03", "1985-11-15", "Aspirin")
            ])
            cursor.executemany("""
                INSERT INTO obat (kode, nama_obat, stok, satuan)
                VALUES (?, ?, ?, ?)
            """, [
                ("OBT-001", "Paracetamol 500mg", 150, "Tablet"),
                ("OBT-002", "Amoxicillin 500mg", 80, "Kapsul"),
                ("OBT-003", "Cetirizine 10mg", 60, "Tablet")
            ])
            cursor.executemany("""
                INSERT INTO dokter (nama, spesialisasi, hari_praktik, jam_praktik)
                VALUES (?, ?, ?, ?)
            """, [
                ("dr. Budi Santoso, Sp.A", "Poli Anak", "Senin - Kamis", "08:00 - 12:00"),
                ("dr. Siti Rahma, Sp.JP", "Poli Jantung", "Selasa & Jumat", "13:00 - 16:00"),
                ("dr. Rian Pratama, Sp.THT", "Poli THT", "Rabu - Sabtu", "09:00 - 13:00")
            ])
            conn.commit()

init_db()

@app.route("/")
def index():
    return jsonify({
        "app": "Sistem Informasi Medis Rumah Sakit (Aplikasi Awal)",
        "arsitektur": "Monolitik",
        "hostname": socket.gethostname(),
        "status": "Running",
        "endpoints": [
            "/health",
            "/api/pasien",
            "/api/obat",
            "/api/resep",
            "/api/dokter",
            "/api/janji-temu",
            "/api/dashboard"
        ]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "arsitektur": "Monolitik",
        "database": "SQLite Embedded (medis_monolit.db)",
        "hostname": socket.gethostname()
    })

# --- DOMAIN PASIEN ---
@app.route("/api/pasien", methods=["GET"])
def get_pasien():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM pasien ORDER BY id ASC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/pasien/<int:id>", methods=["GET"])
def get_detail_pasien(id):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM pasien WHERE id = ?", (id,)).fetchone()
        if not row:
            return jsonify({"error": "Pasien tidak ditemukan"}), 404
        return jsonify(dict(row))

@app.route("/api/pasien", methods=["POST"])
def tambah_pasien():
    data = request.get_json() or {}
    nama = data.get("nama")
    nik = data.get("nik")
    tgl_lahir = data.get("tgl_lahir", "2000-01-01")
    riwayat_alergi = data.get("riwayat_alergi", "Tidak Ada")

    if not nama or not nik:
        return jsonify({"error": "Field 'nama' dan 'nik' wajib diisi"}), 400

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pasien (nik, nama, tgl_lahir, riwayat_alergi)
                VALUES (?, ?, ?, ?)
            """, (nik, nama, tgl_lahir, riwayat_alergi))
            conn.commit()
            new_id = cursor.lastrowid
            return jsonify({"message": "Pasien berhasil ditambahkan", "id": new_id, "nama": nama}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": f"NIK {nik} sudah terdaftar"}), 409

# --- DOMAIN APOTEK ---
@app.route("/api/obat", methods=["GET"])
def get_obat():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM obat ORDER BY id ASC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/resep", methods=["POST"])
def buat_resep():
    data = request.get_json() or {}
    pasien_id = data.get("pasien_id")
    obat_id = data.get("obat_id")
    jumlah = data.get("jumlah", 1)
    aturan_pakai = data.get("aturan_pakai", "1x1 sesudah makan")

    with get_db() as conn:
        # Monolit: Melakukan query langsung antar tabel yang saling terikat
        pasien = conn.execute("SELECT * FROM pasien WHERE id = ?", (pasien_id,)).fetchone()
        if not pasien:
            return jsonify({"error": "Pasien tidak valid"}), 404

        obat = conn.execute("SELECT * FROM obat WHERE id = ?", (obat_id,)).fetchone()
        if not obat:
            return jsonify({"error": "Obat tidak valid"}), 404

        if obat["stok"] < jumlah:
            return jsonify({"error": "Stok obat tidak mencukupi"}), 400

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resep (pasien_id, obat_id, jumlah, aturan_pakai)
            VALUES (?, ?, ?, ?)
        """, (pasien_id, obat_id, jumlah, aturan_pakai))
        cursor.execute("UPDATE obat SET stok = stok - ? WHERE id = ?", (jumlah, obat_id))
        conn.commit()

        return jsonify({
            "message": "Resep obat berhasil diterbitkan",
            "resep_id": cursor.lastrowid,
            "pasien": pasien["nama"],
            "obat": obat["nama_obat"],
            "jumlah": jumlah,
            "aturan_pakai": aturan_pakai
        }), 201

# --- DOMAIN JADWAL DOKTER ---
@app.route("/api/dokter", methods=["GET"])
def get_dokter():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM dokter ORDER BY id ASC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/janji-temu", methods=["POST"])
def buat_janji():
    data = request.get_json() or {}
    pasien_id = data.get("pasien_id")
    dokter_id = data.get("dokter_id")
    tgl_periksa = data.get("tgl_periksa")
    keluhan = data.get("keluhan", "")

    if not pasien_id or not dokter_id or not tgl_periksa:
        return jsonify({"error": "Field pasien_id, dokter_id, dan tgl_periksa wajib diisi"}), 400

    with get_db() as conn:
        pasien = conn.execute("SELECT * FROM pasien WHERE id = ?", (pasien_id,)).fetchone()
        if not pasien:
            return jsonify({"error": "Pasien tidak valid"}), 404

        dokter = conn.execute("SELECT * FROM dokter WHERE id = ?", (dokter_id,)).fetchone()
        if not dokter:
            return jsonify({"error": "Dokter tidak valid"}), 404

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO janji_temu (pasien_id, dokter_id, tgl_periksa, keluhan)
            VALUES (?, ?, ?, ?)
        """, (pasien_id, dokter_id, tgl_periksa, keluhan))
        conn.commit()

        return jsonify({
            "message": "Janji temu berhasil dijadwalkan",
            "id": cursor.lastrowid,
            "pasien": pasien["nama"],
            "dokter": dokter["nama"],
            "spesialisasi": dokter["spesialisasi"],
            "tgl_periksa": tgl_periksa
        }), 201

# --- DOMAIN DASHBOARD & AGREGASI ---
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    with get_db() as conn:
        total_pasien = conn.execute("SELECT COUNT(*) FROM pasien").fetchone()[0]
        total_obat = conn.execute("SELECT COUNT(*) FROM obat").fetchone()[0]
        total_dokter = conn.execute("SELECT COUNT(*) FROM dokter").fetchone()[0]
        total_resep = conn.execute("SELECT COUNT(*) FROM resep").fetchone()[0]
        total_janji = conn.execute("SELECT COUNT(*) FROM janji_temu").fetchone()[0]
        return jsonify({
            "arsitektur": "Monolitik",
            "ringkasan": {
                "total_pasien": total_pasien,
                "total_obat": total_obat,
                "total_dokter": total_dokter,
                "total_resep": total_resep,
                "total_janji_temu": total_janji
            }
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
