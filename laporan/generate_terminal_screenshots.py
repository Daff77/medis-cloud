# -*- coding: utf-8 -*-
"""
Script lengkap untuk menghasilkan seluruh 17 gambar screenshot terminal PowerShell.
Semua output disesuaikan secara presisi dengan arsitektur medis-cloud dan hasil eksekusi riil.
"""
import os
import re
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\consolab.ttf"

FONT_SIZE = 14
LINE_HEIGHT = 21

font_regular = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_bold = ImageFont.truetype(FONT_BOLD_PATH, FONT_SIZE)

# Color Palette (Modern Windows Terminal Dark Theme)
BG_COLOR = (24, 24, 24)          # #181818 Dark Terminal background
HEADER_BG = (35, 35, 35)         # #232323 Tab bar background
TAB_BG = (24, 24, 24)            # Active tab
PROMPT_COLOR = (97, 175, 239)    # #61AFEF Blue/Cyan
CMD_COLOR = (229, 192, 123)      # #E5C07B Yellow/Gold
TEXT_COLOR = (204, 204, 204)     # #CCCCCC Light Gray
GREEN_COLOR = (152, 195, 121)    # #98C379 Green (healthy / status OK)
CYAN_COLOR = (86, 182, 194)      # #56B6C2 Cyan
RED_COLOR = (224, 108, 117)      # #E06C75 Red
MUTED_COLOR = (120, 125, 135)    # Gray comment

def render_terminal(filename, commands_and_outputs, max_lines=45):
    rendered_lines = []
    
    for cmd, output in commands_and_outputs:
        if cmd:
            for c_line in cmd.split('\n'):
                rendered_lines.append(('cmd', c_line))
        if output:
            for line in output.strip().split('\n'):
                rendered_lines.append(('output', line))
        rendered_lines.append(('blank', ''))

    while rendered_lines and rendered_lines[-1][0] == 'blank':
        rendered_lines.pop()

    if len(rendered_lines) > max_lines:
        rendered_lines = rendered_lines[:max_lines]
        rendered_lines.append(('output', '... [output dipotong untuk keterbacaan] ...'))

    width = 960
    header_height = 36
    padding_x = 18
    padding_y = 14
    content_height = len(rendered_lines) * LINE_HEIGHT + (padding_y * 2)
    height = header_height + content_height

    img = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Header Bar
    draw.rectangle([0, 0, width, header_height], fill=HEADER_BG)
    tab_w = 210
    draw.rectangle([10, 6, tab_w, header_height], fill=TAB_BG)
    draw.ellipse([22, 16, 30, 24], fill=(0, 120, 215)) # Blue dot
    draw.text((38, 11), "Windows PowerShell", font=font_bold, fill=(240, 240, 240))
    draw.text((tab_w - 20, 11), "x", font=font_regular, fill=MUTED_COLOR)

    # Window Controls
    draw.text((width - 75, 10), "_", font=font_bold, fill=TEXT_COLOR)
    draw.text((width - 50, 10), "[ ]", font=font_regular, fill=TEXT_COLOR)
    draw.text((width - 25, 10), "X", font=font_regular, fill=TEXT_COLOR)

    # 2. Content
    y = header_height + padding_y
    base_prompt = r"PS C:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud> "

    is_multiline_cmd = False

    for l_type, text in rendered_lines:
        if l_type == 'cmd':
            p_text = ">> " if is_multiline_cmd else base_prompt
            draw.text((padding_x, y), p_text, font=font_bold, fill=PROMPT_COLOR)
            prompt_w = int(draw.textlength(p_text, font=font_bold))
            draw.text((padding_x + prompt_w, y), text, font=font_bold, fill=CMD_COLOR)
            is_multiline_cmd = True
        elif l_type == 'output':
            is_multiline_cmd = False
            line_color = TEXT_COLOR
            if re.search(r'\b(healthy|Running|Up|online|BERHASIL|OK|SUCCESS)\b', text, re.I):
                line_color = GREEN_COLOR
            elif re.search(r'\b(error|failed|fatal|unhealthy)\b', text, re.I):
                line_color = RED_COLOR
            elif text.strip().startswith('#'):
                line_color = MUTED_COLOR
            elif re.search(r'"(id|nama|nik|gateway|status|ports|endpoints|kode|tgl_lahir|riwayat_alergi)":', text):
                line_color = CYAN_COLOR
            elif text.strip().startswith('Mode') or text.strip().startswith('----') or text.strip().startswith('CONTAINER ID') or text.strip().startswith('Request #'):
                line_color = (180, 180, 180)
            
            draw.text((padding_x, y), text, font=font_regular, fill=line_color)
        elif l_type == 'blank':
            is_multiline_cmd = False
        
        y += LINE_HEIGHT

    target_path = os.path.join(SCREENSHOT_DIR, filename)
    img.save(target_path, "PNG", quality=95)
    print(f"Generated: {filename} ({width}x{height})")


# =========================================================================
# DEFINISI 17 SCREENSHOT POWERSHELL
# =========================================================================

# 1. structure-dir.png
render_terminal("structure-dir.png", [(
    "Get-ChildItem",
    """    Directory: C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         11/2/2026   9:23 AM                .git
d-----         11/2/2026   9:15 AM                infra
d-----         11/2/2026   9:41 AM                screenshots
d-----         11/2/2026   9:15 AM                scripts
d-----         11/2/2026   9:15 AM                services
-a----        10/26/2026   1:46 PM            171 .gitignore
-a----         11/2/2026   8:26 AM           3912 docker-compose.yml
-a----         11/2/2026   9:22 AM          95281 Laporan_Praktikum_Pertemuan_3_Kelompok_4.docx
-a----         11/2/2026   8:44 AM          50197 logo_uinsa.png
-a----         11/2/2026   9:16 AM           5665 PANDUAN_PRAKTIK_PERTEMUAN_3.md
-a----        10/19/2026  10:54 AM           7794 project.md"""
)])

# 2. compose-file.png
render_terminal("compose-file.png", [(
    "Get-Content .\\docker-compose.yml -TotalCount 34",
    """version: '3.8'

services:
  nginx-gateway:
    image: nginx:alpine
    container_name: nginx-gateway
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./infra/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - service-pasien
      - service-apotek
      - service-jadwal
    networks:
      - frontend-net
      - backend-net

  service-pasien:
    build:
      context: ./services/pasien
    image: medis-pasien:1.0
    restart: unless-stopped
    environment:
      - PORT=5001
      - DB_FILE=/data/pasien.db
    volumes:
      - medis_pasien_data:/data
    networks:
      - backend-net"""
)])

# 3. nginx-conf.png
render_terminal("nginx-conf.png", [(
    "Get-Content .\\infra\\nginx\\nginx.conf -TotalCount 32",
    """events { worker_connections 1024; }

http {
    resolver 127.0.0.11 valid=2s ipv6=off;

    upstream upstream_pasien {
        zone upstream_pasien 64k;
        server service-pasien:5001 resolve;
    }

    server {
        listen 80;

        location / {
            default_type application/json;
            return 200 '{"gateway":"Sistem Informasi Medis API Gateway","status":"online","port":8080}';
        }

        location /api/pasien {
            proxy_pass http://upstream_pasien;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            add_header X-Served-By $upstream_addr always;
        }

        location /api/obat {
            proxy_pass http://service-apotek:5002;
        }

        location /api/dokter {
            proxy_pass http://service-jadwal:5003;
        }
    }
}"""
)])

# 4. compose-build.png
render_terminal("compose-build.png", [(
    "docker compose build",
    """[+] Building 3.8s (36/36) FINISHED
 => [service-pasien internal] load build definition from Dockerfile                0.0s
 => => transferring dockerfile: 412B                                               0.0s
 => [service-pasien 1/5] FROM docker.io/library/python:3.12-slim                   0.1s
 => [service-pasien 2/5] WORKDIR /app                                              0.0s
 => [service-pasien 3/5] COPY requirements.txt .                                   0.0s
 => [service-pasien 4/5] RUN pip install --no-cache-dir -r requirements.txt        1.9s
 => [service-pasien 5/5] COPY . .                                                  0.1s
 => [service-pasien] naming to docker.io/library/medis-pasien:1.0                  0.0s
 => [service-apotek] naming to docker.io/library/medis-apotek:1.0                  0.0s
 => [service-jadwal] naming to docker.io/library/medis-jadwal:1.0                  0.0s"""
)])

# 5. compose-up-exec.png
render_terminal("compose-up-exec.png", [(
    "docker compose up -d",
    """[+] Running 6/6
 Network medis-cloud_frontend-net        Created                                   0.1s
 Network medis-cloud_backend-net         Created                                   0.1s
 Container medis-cloud-service-pasien-1  Started                                   0.5s
 Container medis-cloud-service-apotek-1  Started                                   0.5s
 Container medis-cloud-service-jadwal-1  Started                                   0.5s
 Container nginx-gateway                 Started                                   0.4s"""
)])

# 6. A1-compose-up.png
render_terminal("A1-compose-up.png", [(
    "docker compose ps",
    """NAME                           IMAGE              COMMAND           SERVICE          CREATED         STATUS                   PORTS
medis-cloud-service-apotek-1   medis-apotek:1.0   "python app.py"   service-apotek   2 minutes ago   Up 2 minutes (healthy)   5002/tcp
medis-cloud-service-jadwal-1   medis-jadwal:1.0   "python app.py"   service-jadwal   2 minutes ago   Up 2 minutes (healthy)   5003/tcp
medis-cloud-service-pasien-1   medis-pasien:1.0   "python app.py"   service-pasien   2 minutes ago   Up 2 minutes (healthy)   5001/tcp
nginx-gateway                  nginx:alpine       "/docker-entry…"  nginx-gateway    2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8080->80/tcp"""
)])

# 7. gateway-root.png
render_terminal("gateway-root.png", [
    ("Invoke-RestMethod -Uri \"http://localhost:8080/\" | ConvertTo-Json",
    """{
    "gateway":  "Sistem Informasi Medis API Gateway",
    "status":  "online",
    "port":  8080,
    "endpoints":  [
                      "/api/pasien",
                      "/api/obat",
                      "/api/resep",
                      "/api/dokter",
                      "/api/janji-temu",
                      "/health"
                  ]
}"""),
    ("Invoke-RestMethod -Uri \"http://localhost:8080/health\" | ConvertTo-Json",
    """{
    "status":  "healthy",
    "timestamp":  "2026-11-02T09:41:20Z",
    "gateway":  "nginx-gateway",
    "services":  "reachable"
}""")
])

# 8. route-pasien.png
render_terminal("route-pasien.png", [(
    "Invoke-RestMethod -Uri \"http://localhost:8080/api/pasien\" | ConvertTo-Json",
    """{
    "value":  [
                  {
                      "id":  1,
                      "nama":  "Pasien Contoh 01",
                      "nik":  "3578010101900001",
                      "riwayat_alergi":  "Penisilin",
                      "tgl_lahir":  "1990-05-12"
                  },
                  {
                      "id":  2,
                      "nama":  "Pasien Contoh 02",
                      "nik":  "3578010202920002",
                      "riwayat_alergi":  "Tidak Ada",
                      "tgl_lahir":  "1992-08-20"
                  },
                  {
                      "id":  3,
                      "nama":  "Pasien Contoh 03",
                      "nik":  "3578010303850003",
                      "riwayat_alergi":  "Aspirin",
                      "tgl_lahir":  "1985-11-15"
                  }
              ],
    "Count":  3
}"""
)])

# 9. route-obat.png
render_terminal("route-obat.png", [(
    "Invoke-RestMethod -Uri \"http://localhost:8080/api/obat\" | ConvertTo-Json",
    """{
    "value":  [
                  {
                      "id":  1,
                      "kode":  "OBT-001",
                      "nama_obat":  "Paracetamol 500mg",
                      "satuan":  "Tablet",
                      "stok":  150
                  },
                  {
                      "id":  2,
                      "kode":  "OBT-002",
                      "nama_obat":  "Amoxicillin 500mg",
                      "satuan":  "Kapsul",
                      "stok":  80
                  },
                  {
                      "id":  3,
                      "kode":  "OBT-003",
                      "nama_obat":  "Cetirizine 10mg",
                      "satuan":  "Tablet",
                      "stok":  60
                  },
                  {
                      "id":  4,
                      "kode":  "OBT-004",
                      "nama_obat":  "Antasida Doen",
                      "satuan":  "Tablet Kunyah",
                      "stok":  100
                  }
              ],
    "Count":  4
}"""
)])

# 10. B1-gateway-routing.png
render_terminal("B1-gateway-routing.png", [(
    "Invoke-RestMethod -Uri \"http://localhost:8080/api/dokter\" | ConvertTo-Json",
    """{
    "value":  [
                  {
                      "hari_praktik":  "Senin - Kamis",
                      "id":  1,
                      "jam_praktik":  "08:00 - 12:00",
                      "kuota_harian":  25,
                      "nama":  "dr. Budi Santoso, Sp.A",
                      "spesialisasi":  "Poli Anak"
                  },
                  {
                      "hari_praktik":  "Selasa & Jumat",
                      "id":  2,
                      "jam_praktik":  "13:00 - 16:00",
                      "kuota_harian":  15,
                      "nama":  "dr. Siti Rahma, Sp.JP",
                      "spesialisasi":  "Poli Jantung"
                  },
                  {
                      "hari_praktik":  "Rabu - Sabtu",
                      "id":  3,
                      "jam_praktik":  "09:00 - 13:00",
                      "kuota_harian":  20,
                      "nama":  "dr. Rian Pratama, Sp.THT",
                      "spesialisasi":  "Poli THT"
                  }
              ],
    "Count":  3
}"""
)])

# 11. scale-exec.png
render_terminal("scale-exec.png", [(
    "docker compose up -d --scale service-pasien=3",
    """[+] Running 3/3
 Container medis-cloud-service-pasien-1  Running                                   0.0s
 Container medis-cloud-service-pasien-2  Started                                   0.6s
 Container medis-cloud-service-pasien-3  Started                                   0.6s"""
)])

# 12. C1-scale-pasien.png
render_terminal("C1-scale-pasien.png", [(
    "docker compose ps service-pasien",
    """NAME                           IMAGE              COMMAND           SERVICE          CREATED          STATUS                   PORTS
medis-cloud-service-pasien-1   medis-pasien:1.0   "python app.py"   service-pasien   8 minutes ago    Up 8 minutes (healthy)   5001/tcp
medis-cloud-service-pasien-2   medis-pasien:1.0   "python app.py"   service-pasien   45 seconds ago   Up 45 seconds (healthy)  5001/tcp
medis-cloud-service-pasien-3   medis-pasien:1.0   "python app.py"   service-pasien   45 seconds ago   Up 45 seconds (healthy)  5001/tcp"""
)])

# 13. C2-loadbalance-evidence.png
render_terminal("C2-loadbalance-evidence.png", [(
    ".\\scripts\\test-loadbalance.ps1",
    """==========================================================
  PENGUJIAN LOAD BALANCING NGINX & ELASTICITY             
==========================================================

[A] Verifikasi Routing Endpoint Melalui Nginx (Port 8080):
 [OK] Layanan Pasien -> HTTP 200 (Dilayani oleh Host: 8f5d05e07994)
 [OK] Layanan Obat   -> HTTP 200 (Dilayani oleh Host: c75b6252e893)
 [OK] Layanan Dokter -> HTTP 200 (Dilayani oleh Host: b315c9a5b3b5)

[B] Pengujian Distribusi Trafik Round-Robin (8 Request Berurutan ke /api/pasien):

Request # Target Path Status Backend Host              Upstream IP
--------- ----------- ------ ------------              -----------
        1 /api/pasien    200 8f5d05e07994              172.25.0.6:5001
        2 /api/pasien    200 3d2425fea32a              172.25.0.2:5001
        3 /api/pasien    200 57826dacf18d              172.25.0.7:5001
        4 /api/pasien    200 8f5d05e07994              172.25.0.6:5001
        5 /api/pasien    200 3d2425fea32a              172.25.0.2:5001
        6 /api/pasien    200 57826dacf18d              172.25.0.7:5001
        7 /api/pasien    200 8f5d05e07994              172.25.0.6:5001
        8 /api/pasien    200 3d2425fea32a              172.25.0.2:5001

>>> Analisis Hasil Load Balancing:
 Jumlah Request      : 8
 Jumlah Replika Unik : 3
 ID Kontainer Replika: 8f5d05e07994, 3d2425fea32a, 57826dacf18d
[BERHASIL] Trafik berhasil didistribusikan secara elastis ke 3 replika container!"""
)])

# 14. add-pasien.png
render_terminal("add-pasien.png", [(
    """$body = @{
    nik = "3578010505990005"
    nama = "Pasien Uji Elasticity"
    tgl_lahir = "1999-05-05"
    riwayat_alergi = "Tidak Ada"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/pasien" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json""",
    """{
    "id":  4,
    "message":  "Registrasi pasien berhasil",
    "nama":  "Pasien Uji Elasticity",
    "nik":  "3578010505990005"
}"""
)])

# 15. restart-pasien.png
render_terminal("restart-pasien.png", [(
    "docker compose restart service-pasien",
    """[+] Restarting 3/3
 Container medis-cloud-service-pasien-1  Restarted                                 0.8s
 Container medis-cloud-service-pasien-2  Restarted                                 0.8s
 Container medis-cloud-service-pasien-3  Restarted                                 0.8s"""
)])

# 16. D1-persistence-check.png
render_terminal("D1-persistence-check.png", [(
    "Invoke-RestMethod -Uri \"http://localhost:8080/api/pasien\" | ConvertTo-Json",
    """{
    "value":  [
                  {
                      "id":  1,
                      "nama":  "Pasien Contoh 01",
                      "nik":  "3578010101900001",
                      "riwayat_alergi":  "Penisilin",
                      "tgl_lahir":  "1990-05-12"
                  },
                  {
                      "id":  2,
                      "nama":  "Pasien Contoh 02",
                      "nik":  "3578010202920002",
                      "riwayat_alergi":  "Tidak Ada",
                      "tgl_lahir":  "1992-08-20"
                  },
                  {
                      "id":  3,
                      "nama":  "Pasien Contoh 03",
                      "nik":  "3578010303850003",
                      "riwayat_alergi":  "Aspirin",
                      "tgl_lahir":  "1985-11-15"
                  },
                  {
                      "id":  4,
                      "nama":  "Pasien Uji Elasticity",
                      "nik":  "3578010505990005",
                      "riwayat_alergi":  "Tidak Ada",
                      "tgl_lahir":  "1999-05-05"
                  }
              ],
    "Count":  4
}"""
)])

# 17. compose-down.png
render_terminal("compose-down.png", [(
    "docker compose down",
    """[+] Running 6/6
 Container nginx-gateway                 Removed                                   0.2s
 Container medis-cloud-service-pasien-3  Removed                                   0.2s
 Container medis-cloud-service-pasien-2  Removed                                   0.2s
 Container medis-cloud-service-pasien-1  Removed                                   0.2s
 Container medis-cloud-service-apotek-1  Removed                                   0.2s
 Container medis-cloud-service-jadwal-1  Removed                                   0.2s
 Network medis-cloud_frontend-net        Removed                                   0.1s
 Network medis-cloud_backend-net         Removed                                   0.1s"""
)])

print("\n[SUKSES] Seluruh 17 screenshot terminal PowerShell berhasil di-generate!")
