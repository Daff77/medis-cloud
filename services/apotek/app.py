import os
import sqlite3
import socket
import json
import urllib.request
import urllib.error
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "apotek.db")
PORT = int(os.environ.get("PORT", 5002))
PASIEN_SERVICE_URL = os.environ.get("PASIEN_SERVICE_URL", "http://service-pasien:5001")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
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
                nama_pasien TEXT NOT NULL,
                obat_id INTEGER NOT NULL,
                nama_obat TEXT NOT NULL,
                jumlah INTEGER NOT NULL,
                aturan_pakai TEXT NOT NULL,
                status TEXT DEFAULT 'SELESAI',
                tgl_resep TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM obat")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO obat (kode, nama_obat, stok, satuan)
                VALUES (?, ?, ?, ?)
            """, [
                ("OBT-001", "Paracetamol 500mg", 150, "Tablet"),
                ("OBT-002", "Amoxicillin 500mg", 80, "Kapsul"),
                ("OBT-003", "Cetirizine 10mg", 60, "Tablet"),
                ("OBT-004", "Antasida Doen", 100, "Tablet Kunyah")
            ])
            conn.commit()

init_db()

def fetch_patient_data(pasien_id):
    """Panggilan HTTP sinkron ke Layanan Data Pasien via Docker Network"""
    url = f"{PASIEN_SERVICE_URL}/api/pasien/{pasien_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "ApotekService/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, (f"Pasien ID {pasien_id} tidak ditemukan di Layanan Pasien", 404)
        return None, (f"Galat HTTP dari Layanan Pasien: {e.reason}", e.code)
    except urllib.error.URLError as e:
        return None, (f"Gagal menghubungi Layanan Pasien di {PASIEN_SERVICE_URL} ({e.reason})", 503)
    return None, ("Galat tidak diketahui saat verifikasi pasien", 500)

@app.route("/")
def index():
    return jsonify({
        "service": "Layanan Apotek & Farmasi",
        "arsitektur": "Microservices (Bounded Context: Apotek)",
        "hostname": socket.gethostname(),
        "status": "Running",
        "port": PORT,
        "pasien_service_url": PASIEN_SERVICE_URL,
        "endpoints": ["/health", "/api/obat", "/api/resep"]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "service-apotek",
        "database": "SQLite (apotek.db)",
        "hostname": socket.gethostname(),
        "pasien_service_target": PASIEN_SERVICE_URL
    })

@app.route("/api/obat", methods=["GET"])
def list_obat():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM obat ORDER BY id ASC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/resep", methods=["GET"])
def list_resep():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM resep ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/resep", methods=["POST"])
def terbitkan_resep():
    data = request.get_json() or {}
    pasien_id = data.get("pasien_id")
    obat_id = data.get("obat_id")
    jumlah = data.get("jumlah", 1)
    aturan_pakai = data.get("aturan_pakai", "3x1 sesudah makan")

    if not pasien_id or not obat_id:
        return jsonify({"error": "Field 'pasien_id' dan 'obat_id' wajib diisi"}), 400

    # 1. Panggilan inter-service ke Service Pasien
    pasien, error_tuple = fetch_patient_data(pasien_id)
    if error_tuple:
        msg, status_code = error_tuple
        return jsonify({"error": msg}), status_code

    nama_pasien = pasien.get("nama")
    alergi = pasien.get("riwayat_alergi", "Tidak Ada")

    with get_db() as conn:
        obat = conn.execute("SELECT * FROM obat WHERE id = ?", (obat_id,)).fetchone()
        if not obat:
            return jsonify({"error": f"Obat ID {obat_id} tidak ditemukan di apotek"}), 404

        if obat["stok"] < jumlah:
            return jsonify({
                "error": f"Stok obat '{obat['nama_obat']}' tidak mencukupi (sisa {obat['stok']}, diminta {jumlah})"
            }), 400

        # Cek peringatan alergi
        alergi_warning = None
        if "penisilin" in alergi.lower() and "amoxicillin" in obat["nama_obat"].lower():
            alergi_warning = f"PERINGATAN: Pasien memiliki riwayat alergi ({alergi}) terhadap antibiotik ini!"

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resep (pasien_id, nama_pasien, obat_id, nama_obat, jumlah, aturan_pakai)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pasien_id, nama_pasien, obat_id, obat["nama_obat"], jumlah, aturan_pakai))
        cursor.execute("UPDATE obat SET stok = stok - ? WHERE id = ?", (jumlah, obat_id))
        conn.commit()

        res = {
            "message": "Resep berhasil diproses dan obat disiapkan",
            "resep_id": cursor.lastrowid,
            "data_pasien": {
                "id": pasien_id,
                "nama": nama_pasien,
                "alergi": alergi
            },
            "data_obat": {
                "nama": obat["nama_obat"],
                "jumlah_keluar": jumlah,
                "sisa_stok": obat["stok"] - jumlah,
                "aturan_pakai": aturan_pakai
            }
        }
        if alergi_warning:
            res["peringatan_alergi"] = alergi_warning

        return jsonify(res), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
