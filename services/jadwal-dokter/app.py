import os
import sqlite3
import socket
import json
import urllib.request
import urllib.error
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "jadwal.db")
PORT = int(os.environ.get("PORT", 5003))
PASIEN_SERVICE_URL = os.environ.get("PASIEN_SERVICE_URL", "http://service-pasien:5001")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dokter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                spesialisasi TEXT NOT NULL,
                hari_praktik TEXT NOT NULL,
                jam_praktik TEXT NOT NULL,
                kuota_harian INTEGER DEFAULT 20
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS janji_temu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                no_antrean TEXT NOT NULL,
                pasien_id INTEGER NOT NULL,
                nama_pasien TEXT NOT NULL,
                dokter_id INTEGER NOT NULL,
                nama_dokter TEXT NOT NULL,
                spesialisasi TEXT NOT NULL,
                tgl_periksa TEXT NOT NULL,
                keluhan TEXT,
                status TEXT DEFAULT 'MENUNGGU',
                dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM dokter")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO dokter (nama, spesialisasi, hari_praktik, jam_praktik, kuota_harian)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("dr. Budi Santoso, Sp.A", "Poli Anak", "Senin - Kamis", "08:00 - 12:00", 25),
                ("dr. Siti Rahma, Sp.JP", "Poli Jantung", "Selasa & Jumat", "13:00 - 16:00", 15),
                ("dr. Rian Pratama, Sp.THT", "Poli THT", "Rabu - Sabtu", "09:00 - 13:00", 20)
            ])
            conn.commit()

init_db()

def fetch_patient_data(pasien_id):
    """Panggilan HTTP sinkron ke Layanan Data Pasien via Docker Network"""
    url = f"{PASIEN_SERVICE_URL}/api/pasien/{pasien_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "JadwalDokterService/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, (f"Pasien ID {pasien_id} tidak terdaftar di Layanan Pasien", 404)
        return None, (f"Galat HTTP dari Layanan Pasien: {e.reason}", e.code)
    except urllib.error.URLError as e:
        return None, (f"Gagal menghubungi Layanan Pasien di {PASIEN_SERVICE_URL} ({e.reason})", 503)
    return None, ("Galat tidak diketahui saat verifikasi pasien", 500)

@app.route("/")
def index():
    return jsonify({
        "service": "Layanan Jadwal Dokter & Poliklinik",
        "arsitektur": "Microservices (Bounded Context: Jadwal Dokter)",
        "hostname": socket.gethostname(),
        "status": "Running",
        "port": PORT,
        "pasien_service_url": PASIEN_SERVICE_URL,
        "endpoints": ["/health", "/api/dokter", "/api/janji-temu"]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "service-jadwal",
        "database": "SQLite (jadwal.db)",
        "hostname": socket.gethostname(),
        "pasien_service_target": PASIEN_SERVICE_URL
    })

@app.route("/api/dokter", methods=["GET"])
def list_dokter():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM dokter ORDER BY id ASC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/janji-temu", methods=["GET"])
def list_janji():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM janji_temu ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/janji-temu", methods=["POST"])
def buat_janji():
    data = request.get_json() or {}
    pasien_id = data.get("pasien_id")
    dokter_id = data.get("dokter_id")
    tgl_periksa = data.get("tgl_periksa")
    keluhan = data.get("keluhan", "")

    if not pasien_id or not dokter_id or not tgl_periksa:
        return jsonify({"error": "Field 'pasien_id', 'dokter_id', dan 'tgl_periksa' wajib diisi"}), 400

    # 1. Panggilan inter-service ke Service Pasien
    pasien, error_tuple = fetch_patient_data(pasien_id)
    if error_tuple:
        msg, status_code = error_tuple
        return jsonify({"error": msg}), status_code

    nama_pasien = pasien.get("nama")

    with get_db() as conn:
        dokter = conn.execute("SELECT * FROM dokter WHERE id = ?", (dokter_id,)).fetchone()
        if not dokter:
            return jsonify({"error": f"Dokter ID {dokter_id} tidak ditemukan"}), 404

        # Hitung nomor antrean berdasarkan pendaftaran pada dokter dan tanggal yang sama
        antrean_count = conn.execute("""
            SELECT COUNT(*) FROM janji_temu
            WHERE dokter_id = ? AND tgl_periksa = ?
        """, (dokter_id, tgl_periksa)).fetchone()[0]

        if antrean_count >= dokter["kuota_harian"]:
            return jsonify({
                "error": f"Kuota konsultasi {dokter['nama']} pada tanggal {tgl_periksa} sudah penuh ({dokter['kuota_harian']} pasien)"
            }), 400

        no_antrean = f"POLI-{dokter_id:02d}-{antrean_count + 1:03d}"

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO janji_temu (no_antrean, pasien_id, nama_pasien, dokter_id, nama_dokter, spesialisasi, tgl_periksa, keluhan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (no_antrean, pasien_id, nama_pasien, dokter_id, dokter["nama"], dokter["spesialisasi"], tgl_periksa, keluhan))
        conn.commit()

        return jsonify({
            "message": "Pendaftaran janji temu poliklinik berhasil",
            "janji_id": cursor.lastrowid,
            "no_antrean": no_antrean,
            "pasien": {
                "id": pasien_id,
                "nama": nama_pasien
            },
            "dokter": {
                "nama": dokter["nama"],
                "spesialisasi": dokter["spesialisasi"],
                "jadwal": f"{dokter['hari_praktik']} ({dokter['jam_praktik']})"
            },
            "tgl_periksa": tgl_periksa,
            "keluhan": keluhan
        }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
