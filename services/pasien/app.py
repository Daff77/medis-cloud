import os
import sqlite3
import socket
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "pasien.db")
PORT = int(os.environ.get("PORT", 5001))

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
        conn.commit()

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
            conn.commit()

init_db()

@app.route("/")
def index():
    return jsonify({
        "service": "Layanan Data Pasien & Rekam Medis",
        "arsitektur": "Microservices (Bounded Context: Pasien)",
        "hostname": socket.gethostname(),
        "status": "Running",
        "port": PORT,
        "endpoints": ["/health", "/api/pasien", "/api/pasien/<id>"]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "service-pasien",
        "database": "SQLite (pasien.db)",
        "hostname": socket.gethostname()
    })

@app.route("/api/pasien", methods=["GET"])
def list_pasien():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM pasien ORDER BY id ASC").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/pasien/<int:id>", methods=["GET"])
def get_pasien(id):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM pasien WHERE id = ?", (id,)).fetchone()
        if not row:
            return jsonify({"error": f"Pasien dengan ID {id} tidak ditemukan"}), 404
        return jsonify(dict(row))

@app.route("/api/pasien", methods=["POST"])
def register_pasien():
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
            return jsonify({
                "message": "Registrasi pasien berhasil",
                "id": cursor.lastrowid,
                "nama": nama,
                "nik": nik
            }), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": f"NIK {nik} sudah terdaftar"}), 409

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
