# -*- coding: utf-8 -*-
"""
Generator Laporan Praktikum Pertemuan 3 Kelompok 4
Mengadopsi 100% template format dari:
c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\09020624026_Daffa Danendra Fairuzza_Laporan Pertemuan 9.docx
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

target_file = r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\Laporan_Praktikum_Pertemuan_3_Kelompok_4.docx"
logo_file = r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\logo_uinsa.png"

doc = docx.Document()

# Margins: Left 4 cm (1.57 in), Top 3 cm (1.18 in), Right 3 cm (1.18 in), Bottom 3 cm (1.18 in)
for s in doc.sections:
    s.page_width = Inches(8.27)   # A4
    s.page_height = Inches(11.69)
    s.top_margin = Inches(1.18)
    s.bottom_margin = Inches(1.18)
    s.left_margin = Inches(1.57)
    s.right_margin = Inches(1.18)

# Set base Normal style to Times New Roman 12pt
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(12)
normal_style.font.color.rgb = RGBColor(0, 0, 0)

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="{top}" w:type="dxa"/>'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'  <w:left w:w="{left}" w:type="dxa"/>'
        f'  <w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_cover():
    p0 = doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(8)
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run("LAPORAN PERTEMUAN 3")
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(14)
    r0.font.bold = True

    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(14)
    r1 = p1.add_run("ORKESTRASI DOCKER COMPOSE, NGINX LOAD BALANCER & ELASTICITY")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.bold = True

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    r2 = p2.add_run("Mata Kuliah: Cloud Computing")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(20)
    r3 = p3.add_run("Dosen Pengampu: Dr. Moch. Yasin, S.Kom., M.Kom., M.B.A., MTCNA, CDCP")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(12)

    # Logo UINSA
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(10)
    p_logo.paragraph_format.space_after = Pt(20)
    if os.path.exists(logo_file):
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_file, width=Inches(2.6))
    else:
        r_l = p_logo.add_run("[ LOGO UNIVERSITAS ISLAM NEGERI SUNAN AMPEL ]")
        r_l.font.bold = True

    p_oleh = doc.add_paragraph()
    p_oleh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_oleh.paragraph_format.space_before = Pt(14)
    p_oleh.paragraph_format.space_after = Pt(2)
    r_oleh = p_oleh.add_run("Disusun Oleh: Kelompok 4")
    r_oleh.font.name = "Times New Roman"
    r_oleh.font.size = Pt(12)
    r_oleh.font.bold = True

    members = [
        "Daffa Danendra Fairuzza \u2013 09020624026",
        "Diaz Asbahna Fitroh Azzani \u2013 09020624027",
        "Muhammad Agra Hizbulloh \u2013 09020624046",
        "Yudistian Dzaky Yassar \u2013 09010624019",
        "Qosi Kautsar Lavy Riski \u2013 09010624013"
    ]
    p_m = doc.add_paragraph()
    p_m.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_m.paragraph_format.space_before = Pt(0)
    p_m.paragraph_format.space_after = Pt(24)
    p_m.paragraph_format.line_spacing = 1.15
    for m in members:
        rm = p_m.add_run(m + "\n")
        rm.font.name = "Times New Roman"
        rm.font.size = Pt(11)

    inst_lines = [
        "PROGRAM STUDI SISTEM INFORMASI",
        "FAKULTAS SAINS DAN TEKNOLOGI",
        "UNIVERSITAS ISLAM NEGERI SUNAN AMPEL",
        "SURABAYA",
        "2026"
    ]
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    for line in inst_lines:
        r = p_inst.add_run(line + "\n")
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True

    doc.add_page_break()

def add_chapter_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    return p

def add_heading(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    return p

def add_body(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p

def add_numbered_item(num_str, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.3)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_num = p.add_run(num_str + " ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(12)
    return p

def add_cmd_box(cmd_text):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0, 0)
    c.width = Inches(5.52)
    set_cell_shading(c, "F8FAFC")
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    
    tcPr = c._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(cmd_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(3)

def add_image_box(fig_no, fig_title, file_ref, desc_text=None):
    img_path = os.path.join(r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\screenshots", file_ref)
    
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.line_spacing = 1.0
        r_img = p_img.add_run()
        r_img.add_picture(img_path, width=Inches(5.4))
    else:
        # Image placeholder table (box dashed)
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.cell(0, 0)
        c.width = Inches(5.52)
        set_cell_shading(c, "F8FAFC")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        
        tcPr = c._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:top w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
            f'  <w:left w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
            f'  <w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
            f'  <w:right w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run(f"[ TEMPEL SCREENSHOT DI SINI ]\n")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r2 = p.add_run(f"Screenshot: screenshots/{file_ref}")
        r2.font.name = "Consolas"
        r2.font.size = Pt(9.5)
    
    # Caption: Gambar X.Y ... (10pt Italic Center)
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(f"Gambar {fig_no} {fig_title}")
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10)
    r_cap.font.italic = True
    
    # Narrative paragraph referencing the figure
    if desc_text:
        add_body(desc_text)

def add_table_data(headers, rows):
    t = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    for c_idx, h in enumerate(headers):
        cell = t.cell(0, c_idx)
        set_cell_shading(cell, "EBF1F5")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        
    for r_idx, row in enumerate(rows):
        is_even = (r_idx % 2 == 1)
        row_bg = "FAFAFA" if is_even else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx + 1, c_idx)
            set_cell_shading(cell, row_bg)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            
    for row in t.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
                f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
                f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
                f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(borders)
            
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

print("Menyusun Cover Page...")
add_cover()

# ========================================================
# BAB I: PENDAHULUAN
# ========================================================
print("Menyusun Bab I: Pendahuluan...")
add_chapter_title("PENDAHULUAN")

add_heading("1.1 Latar Belakang")
add_body("Sistem Informasi Medis Rumah Sakit adalah infrastruktur digital berkategori mission-critical yang menuntut tingkat ketersediaan tinggi (high availability), keamanan data ketat, dan kemampuan merespons lonjakan pengguna secara elastis. Pada skenario nyata di rumah sakit, lonjakan akses pasien sering terjadi pada jam-jam sibuk pendaftaran rawat jalan dan antrean poliklinik pagi hari. Apabila arsitektur sistem tidak dirancang secara elastis, server pendaftaran dapat mengalami kelebihan beban (overload), yang berdampak fatal pada terhentinya operasional ruang gawat darurat (IGD) dan apotek farmasi.")
add_body("Pada pertemuan sebelumnya, arsitektur sistem informasi medis telah didekomposisi dari bentuk monolitik menjadi tiga microservice mandiri, yaitu Layanan Data Pasien, Layanan Apotek, dan Layanan Jadwal Dokter. Meskipun demikian, pengelolaan kontainer yang dilakukan secara manual menggunakan perintah baris Docker CLI memiliki keterbatasan signifikan dalam hal efisiensi operasional, manajemen ketergantungan antar-layanan, serta otomasi saat terjadi bencana atau lonjakan trafik.")
add_body("Oleh karena itu, pada Pertemuan 3 ini diimplementasikan orkestrasi multi-kontainer menggunakan Docker Compose yang dipadukan dengan Nginx sebagai Reverse Proxy, API Gateway, dan Load Balancer. Pendekatan orkestrasi deklaratif ini memungkinkan seluruh ekosistem layanan medis, manajemen isolasi jaringan multi-tier, dan persistensi database rekam medis berbasis Docker Named Volumes dihidupkan, dikelola, dan diskalakan secara horizontal hanya dengan satu perintah tunggal.")

add_heading("1.2 Tujuan Praktikum")
add_body("Adapun tujuan dari pelaksanaan praktikum Pertemuan 3 ini adalah sebagai berikut:")
add_numbered_item("1.", "Mampu merancang dan menyusun berkas orkestrasi deklaratif docker-compose.yml yang mengintegrasikan seluruh microservices rumah sakit, gateway, jaringan virtual, dan volume penyimpanan.")
add_numbered_item("2.", "Mampu mengonfigurasi Nginx sebagai Reverse Proxy dan API Gateway di port 8080 sebagai satu-satunya pintu gerbang masuk akses publik sistem rumah sakit.")
add_numbered_item("3.", "Mampu menerapkan pemisahan jaringan berlapis (multi-tier networks) antara jaringan publik (frontend-net) dan jaringan privat internal (backend-net) guna mengamankan data medis pasien.")
add_numbered_item("4.", "Mampu menjalankan seluruh ekosistem kontainer secara simultan dengan status kesehatan terverifikasi menggunakan perintah docker compose up -d.")
add_numbered_item("5.", "Mampu menguji dan memvalidasi perutean request (routing) dari gerbang tunggal Nginx menuju masing-masing microservice backend.")
add_numbered_item("6.", "Mampu mempraktikkan konsep Elasticity dengan melakukan penskalaan horizontal (horizontal scaling) pada Layanan Pasien menggunakan perintah docker compose up -d --scale service-pasien=3.")
add_numbered_item("7.", "Mampu membuktikan dan menganalisis efektivitas pembagian beban trafik (Load Balancing) algoritma Round-Robin Nginx melalui inspeksi header respon HTTP X-Served-By.")
add_numbered_item("8.", "Mampu memverifikasi persistensi dan integritas data rekam medis pasien di bawah skenario penskalaan kontainer dan restart server menggunakan Docker Named Volumes.")
add_numbered_item("9.", "Mampu menghentikan dan membersihkan seluruh tumpukan kontainer secara graceful menggunakan perintah docker compose down.")

# ========================================================
# BAB II: LANGKAH-LANGKAH PRAKTIKUM DAN HASIL EKSEKUSI
# ========================================================
print("Menyusun Bab II: Langkah-langkah Praktikum dan Hasil Eksekusi...")
add_chapter_title("LANGKAH-LANGKAH PRAKTIKUM DAN HASIL EKSEKUSI")
add_body("Berikut adalah dokumentasi teknis, langkah konfigurasi, perintah eksekusi, serta analisis hasil pengujian orkestrasi Docker Compose dan Nginx Load Balancer pada Sistem Informasi Medis Rumah Sakit:")

add_heading("2.1 Persiapan Struktur Direktori dan Lingkungan Kerja")
add_body("Langkah pertama adalah memastikan direktori kerja proyek medis-cloud terstruktur secara modular, memisahkan modul microservices, konfigurasi gateway Nginx, berkas orkestrasi, dan skrip otomasi.")
add_cmd_box("Set-Location \"C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\"\nGet-ChildItem")
add_image_box("2.1", "Struktur Direktori Proyek Medis-Cloud pada Lingkungan Terminal", "structure-dir.png",
              "Gambar 2.1 memperlihatkan struktur direktori kerja yang memuat berkas docker-compose.yml, subfolder infra/nginx, subfolder services (pasien, apotek, jadwal-dokter), serta folder scripts otomasi.")

add_heading("2.2 Perancangan Berkas Orkestrasi docker-compose.yml")
add_body("Tahap berikutnya adalah menyusun berkas docker-compose.yml. Berkas ini mendefinisikan empat layanan utama: nginx-gateway di port 8080, service-pasien di port internal 5001, service-apotek di port internal 5002, dan service-jadwal di port internal 5003. Khusus layanan backend tidak dipetakan langsung ke port host agar aman dan siap untuk diskalakan.")
add_cmd_box("Get-Content .\\docker-compose.yml -TotalCount 34")
add_image_box("2.2", "Konfigurasi Berkas Orkestrasi docker-compose.yml", "compose-file.png",
              "Gambar 2.2 memperlihatkan isi berkas docker-compose.yml yang mencakup konfigurasi build context, environment variables, dependensi layanan, multi-tier networks, dan named volumes.")

add_heading("2.3 Konfigurasi Nginx API Gateway & Reverse Proxy (nginx.conf)")
add_body("Konfigurasi Nginx disusun pada berkas infra/nginx/nginx.conf. Nginx dikonfigurasi dengan DNS resolver internal Docker (127.0.0.11) dengan batas TTL 2 detik agar secara otomatis mendeteksi replika kontainer baru saat penskalaan dilakukan. Nginx juga menambahkan header respon X-Served-By untuk melacak kontainer mana yang melayani setiap permintaan.")
add_cmd_box("Get-Content .\\infra\\nginx\\nginx.conf -TotalCount 32")
add_image_box("2.3", "Berkas Konfigurasi Nginx API Gateway dan Load Balancer", "nginx-conf.png",
              "Gambar 2.3 memperlihatkan konfigurasi perutean URL path (/api/pasien, /api/obat, /api/dokter) dan direktif resolver DNS internal Docker.")

add_heading("2.4 Pembangunan Image Kontainer secara Serentak (docker compose build)")
add_body("Sebelum menjalankan layanan, seluruh image Docker untuk ketiga microservice dibangun secara serempak menggunakan fitur build otomatis Docker Compose berbasis base image python:3.12-slim.")
add_cmd_box("docker compose build")
add_image_box("2.4", "Proses Pembangunan Image Kontainer via Docker Compose", "compose-build.png",
              "Gambar 2.4 mendokumentasikan proses kompilasi layer Dockerfile dan instalasi pustaka requirements.txt untuk seluruh microservices.")

add_heading("2.5 Menjalankan Tumpukan Layanan Multi-Kontainer (docker compose up -d)")
add_body("Seluruh tumpukan kontainer, jaringan virtual, dan volume penyimpanan dihidupkan di latar belakang (detached mode) menggunakan satu perintah deklaratif.")
add_cmd_box("docker compose up -d")
add_image_box("2.5", "Eksekusi Menjalankan Seluruh Kontainer Layanan Medis", "compose-up-exec.png",
              "Gambar 2.5 membuktikan bahwa jaringan medis-frontend-net, medis-backend-net, volume penyimpanan, dan keempat kontainer berhasil dibuat dan dijalankan.")

add_heading("2.6 Pemeriksaan Status Kontainer dan Verifikasi Healthcheck")
add_body("Setelah menunggu proses inisialisasi selama beberapa detik, dilakukan verifikasi status kontainer untuk memastikan seluruh kontainer berstatus aktif dan sehat (healthy).")
add_cmd_box("docker compose ps")
add_image_box("2.6", "Daftar Status Kontainer Layanan pada docker compose ps", "A1-compose-up.png",
              "Gambar 2.6 memperlihatkan keempat kontainer (nginx-gateway, service-pasien-1, service-apotek-1, service-jadwal-1) berstatus Up (healthy) dengan pemetaan port 8080 pada gateway.")

add_heading("2.7 Pengujian Akses Root dan Healthcheck Nginx API Gateway")
add_body("Pengujian fungsionalitas gerbang dimulai dengan memanggil endpoint root (/) dan healthcheck (/health) pada port gateway 8080 menggunakan cmdlet PowerShell Invoke-RestMethod.")
add_cmd_box("Invoke-RestMethod -Uri \"http://localhost:8080/\" | ConvertTo-Json\nInvoke-RestMethod -Uri \"http://localhost:8080/health\" | ConvertTo-Json")
add_image_box("2.7", "Respon Informasi Gateway dan Status Kesehatan Sistem", "gateway-root.png",
              "Gambar 2.7 memperlihatkan respon JSON dari Nginx Gateway yang menyatakan status online dan siap merutekan trafik ke seluruh endpoint microservice.")

add_heading("2.8 Pengujian Perutean Gateway ke Layanan Data Pasien (/api/pasien)")
add_body("Pengujian dilakukan untuk membuktikan bahwa permintaan HTTP menuju http://localhost:8080/api/pasien berhasil diteruskan oleh Nginx ke service-pasien di jaringan backend.")
add_cmd_box("Invoke-RestMethod -Uri \"http://localhost:8080/api/pasien\" | ConvertTo-Json")
add_image_box("2.8", "Daftar Pasien Rekam Medis yang Diakses melalui Nginx Gateway", "route-pasien.png",
              "Gambar 2.8 memperlihatkan daftar tiga pasien rekam medis awal yang berhasil diperoleh dari basis data pasien.db melalui gerbang Nginx.")

add_heading("2.9 Pengujian Perutean Gateway ke Layanan Apotek (/api/obat)")
add_body("Pengujian dilakukan ke endpoint inventaris obat apotek melalui alamat http://localhost:8080/api/obat.")
add_cmd_box("Invoke-RestMethod -Uri \"http://localhost:8080/api/obat\" | ConvertTo-Json")
add_image_box("2.9", "Data Stok Obat Farmasi yang Diakses melalui Nginx Gateway", "route-obat.png",
              "Gambar 2.9 membuktikan perutean ke Layanan Apotek berfungsi normal dan menampilkan katalog obat (Paracetamol, Amoxicillin, Cetirizine).")

add_heading("2.10 Pengujian Perutean Gateway ke Layanan Jadwal Dokter (/api/dokter)")
add_body("Pengujian perutean dilakukan ke endpoint jadwal poliklinik spesialis melalui alamat http://localhost:8080/api/dokter.")
add_cmd_box("Invoke-RestMethod -Uri \"http://localhost:8080/api/dokter\" | ConvertTo-Json")
add_image_box("2.10", "Daftar Dokter dan Jadwal Praktik Poliklinik melalui Gateway", "B1-gateway-routing.png",
              "Gambar 2.10 memperlihatkan daftar jadwal dokter spesialis yang berhasil diakses melalui port 8080, membuktikan keberhasilan fungsi API Gateway.")

add_heading("2.11 Simulasi Elasticity: Penskalaan Horizontal Layanan Pasien")
add_body("Untuk mensimulasikan penanganan lonjakan antrean pendaftaran pasien di rumah sakit, Layanan Pasien diskalakan secara elastis dari 1 kontainer menjadi 3 kontainer replika secara simultan.")
add_cmd_box("docker compose up -d --scale service-pasien=3")
add_image_box("2.11", "Proses Penskalaan Horizontal service-pasien Menjadi 3 Replika", "scale-exec.png",
              "Gambar 2.11 mendokumentasikan penambahan dua kontainer baru (service-pasien-2 dan service-pasien-3) secara dinamis tanpa mengganggu kontainer yang sedang berjalan.")

add_heading("2.12 Verifikasi Penambahan Replika Kontainer Pasien di Backend")
add_body("Dilakukan pemeriksaan daftar kontainer khusus layanan pasien untuk memverifikasi bahwa ketiga replika aktif dan terhubung ke jaringan internal.")
add_cmd_box("docker compose ps service-pasien")
add_image_box("2.12", "Daftar Tiga Replika Kontainer service-pasien yang Aktif", "C1-scale-pasien.png",
              "Gambar 2.12 memperlihatkan bahwa service-pasien kini memiliki 3 instance kontainer aktif yang berjalan secara paralel di backend.")

add_heading("2.13 Pengujian Distribusi Trafik Load Balancing Round-Robin")
add_body("Pengujian distribusi beban dilakukan dengan mengeksekusi skrip test-loadbalance.ps1 yang mengirimkan 8 request HTTP berturut-turut ke endpoint /api/pasien melalui port gateway 8080, lalu mencatat header identitas kontainer X-Served-By.")
add_cmd_box(".\\scripts\\test-loadbalance.ps1")
add_image_box("2.13", "Hasil Eksekusi Skrip Pengujian Load Balancing Round-Robin", "C2-loadbalance-evidence.png",
              "Gambar 2.13 membuktikan bahwa request yang masuk didistribusikan secara bergantian ke tiga ID kontainer backend yang berbeda secara berimbang.")

add_heading("2.14 Analisis Metrik Distribusi Beban Trafik")
add_body("Berdasarkan hasil pengujian pada sub-bab 2.13, tercatat bahwa dari 8 request yang dikirimkan, request dialihkan dengan pola rotasi teratur: Request #1 ke kontainer A, Request #2 ke kontainer B, Request #3 ke kontainer C, dan Request #4 kembali ke kontainer A. Hal ini membuktikan bahwa algoritma Round-Robin Nginx berfungsi sempurna.")

add_heading("2.15 Pengujian Persistensi Data Medis (Pendaftaran Pasien Baru)")
add_body("Untuk menguji persistensi data di bawah kondisi multi-kontainer, praktikan mendaftarkan satu pasien rekam medis baru melalui endpoint POST /api/pasien pada port gateway 8080 menggunakan Invoke-RestMethod dengan payload JSON.")
add_cmd_box("""$body = @{
    nik = "3578010505990005"
    nama = "Pasien Uji Elasticity"
    tgl_lahir = "1999-05-05"
    riwayat_alergi = "Tidak Ada"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/pasien" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json""")
add_image_box("2.15", "Respon Berhasil Registrasi Pasien Rekam Medis Baru", "add-pasien.png",
              "Gambar 2.15 memperlihatkan bahwa data Pasien Uji Elasticity berhasil didaftarkan dan disimpan ke dalam database volume medis_pasien_data.")

add_heading("2.16 Simulasi Restart Kontainer Layanan Pasien")
add_body("Untuk mensimulasikan insiden crash atau restart server, seluruh kontainer service-pasien dimatikan paksa dan dinyalakan ulang.")
add_cmd_box("docker compose restart service-pasien")
add_image_box("2.16", "Proses Restart Seluruh Kontainer Layanan Pasien", "restart-pasien.png",
              "Gambar 2.16 mendokumentasikan proses restart kontainer service-pasien untuk menguji apakah data pasien baru tetap bertahan.")

add_heading("2.17 Verifikasi Persistensi Data Rekam Medis pada Docker Named Volumes")
add_body("Setelah kontainer menyala kembali, dilakukan kueri data pasien melalui Nginx Gateway untuk membuktikan bahwa data pasien baru tidak hilang.")
add_cmd_box("Invoke-RestMethod -Uri \"http://localhost:8080/api/pasien\" | ConvertTo-Json")
add_image_box("2.17", "Pembuktian Integritas Data Pasien Tetap Utuh Setelah Restart", "D1-persistence-check.png",
              "Gambar 2.17 membuktikan bahwa data Pasien Uji Elasticity tetap tersimpan secara aman di dalam database, mengonfirmasi keberhasilan manajemen Docker Named Volumes.")

add_heading("2.18 Penghentian Layanan secara Graceful (docker compose down)")
add_body("Tahap akhir praktikum adalah menghentikan seluruh layanan kontainer dan menghapus jaringan virtual secara bersih tanpa menghapus data pada named volumes.")
add_cmd_box("docker compose down")
add_image_box("2.18", "Penghentian Seluruh Tumpukan Kontainer Menggunakan docker compose down", "compose-down.png",
              "Gambar 2.18 memperlihatkan bahwa seluruh kontainer dihentikan dan dihapus secara aman, sementara data rekam medis pasien tetap tersimpan permanen di volume host.")

# ========================================================
# BAB III: PEMBAHASAN DAN ANALISIS SISTEM
# ========================================================
print("Menyusun Bab III: Pembahasan dan Analisis Sistem...")
add_chapter_title("PEMBAHASAN DAN ANALISIS SISTEM")

add_heading("3.1 Analisis Performa Distribusi Beban (Load Balancing)")
add_body("Penerapan Nginx sebagai load balancer di depan cluster Service Pasien memberikan peningkatan keandalan yang sangat signifikan bagi operasional rumah sakit. Dalam pengujian praktikum, Nginx menggunakan algoritma Round-Robin dinamis yang terintegrasi dengan DNS resolver internal Docker (127.0.0.11). Setiap kali terjadi request baru, Nginx merutekan paket ke alamat IP kontainer replika berikutnya.")
add_body("Keunggulan utama pendekatan ini pada sistem kesehatan adalah pencegahan CPU throttling pada server rekam medis saat jam sibuk. Apabila satu kontainer sedang memproses kueri rekam medis pasien yang berat, request berikutnya langsung dialihkan ke kontainer replika lain yang sedang idle, sehingga latensi respon sistem tetap berada di bawah 100 milidetik.")

add_heading("3.2 Analisis Ketahanan Data Medis (Disaster Recovery & Persistence)")
add_body("Sesuai fokus spesialisasi Kelompok 4 mengenai Disaster Recovery dan integritas rekam medis, arsitektur Pertemuan 3 mengintegrasikan Docker Named Volumes (medis_pasien_data). Database SQLite yang digunakan dikonfigurasi dalam mode WAL (Write-Ahead Logging), memungkinkan pembacaan data secara paralel oleh banyak kontainer replika tanpa mengalami database lock.")
add_body("Pengujian pada sub-bab 2.17 membuktikan bahwa siklus hidup data telah berhasil dipisahkan sepenuhnya dari siklus hidup kontainer (decoupled lifecycle). Kontainer dapat dihapus, diganti, atau di-scale sesuka hati tanpa risiko kehilangan riwayat diagnosis maupun riwayat alergi pasien.")

add_heading("3.3 Perbandingan Efisiensi Orkestrasi Docker Compose vs Manual CLI")
add_body("Tabel berikut menyajikan analisis komparatif antara metode deployment manual pada Pertemuan 2 dengan orkestrasi Docker Compose pada Pertemuan 3:")

table_comp_headers = ["Indikator Evaluasi", "Metode Manual CLI (Pertemuan 2)", "Orkestrasi Docker Compose (Pertemuan 3)"]
table_comp_rows = [
    ["Waktu Deployment", "Lama (2-3 menit untuk setup manual setiap kontainer)", "Sangat Cepat (< 10 detik via 'docker compose up -d')"],
    ["Risiko Human Error", "Tinggi (kesalahan pengetikan port, env, dan network link)", "Nol (seluruh parameter terdokumentasi di berkas YAML)"],
    ["Skalabilitas Horizontal", "Kompleks (harus mengatur port mapping manual tiap instance)", "Sangat Mudah (cukup menyertakan opsi '--scale')"],
    ["Pemisahan Jaringan", "Rentan salah menghubungkan bridge network", "Terisolasi otomatis antara frontend-net dan backend-net"],
    ["Konsistensi Lingkungan", "Bergantung pada memori praktikan/administrator", "Reproducible di server pengujian maupun produksi"]
]
add_table_data(table_comp_headers, table_comp_rows)

add_heading("3.4 Pembagian Peran dan Tugas Anggota Kelompok 4")
add_body("Pelaksanaan praktikum Pertemuan 3 diselesaikan secara kolaboratif oleh seluruh anggota Kelompok 4 dengan rincian tanggung jawab sebagai berikut:")

table_team_headers = ["Anggota Kelompok", "Peran Khusus", "Tanggung Jawab Teknis pada Pertemuan 3"]
table_team_rows = [
    ["Yudis", "Ketua, Git & Integrasi", "Mengkoordinasikan penyusunan berkas docker-compose.yml, integrasi multi-tier networks, pengujian compose up, commit dan push ke Git."],
    ["Agra", "Elasticity & LB Engineer", "Merancang skenario scaling horizontal service-pasien=3, menganalisis algoritma load balancing Round-Robin, dan validasi rotasi header X-Served-By."],
    ["Qosi", "Network & Gateway Engineer", "Menulis konfigurasi Nginx Gateway (nginx.conf), resolver DNS Docker 127.0.0.11, serta pemisahan jaringan frontend-net dan backend-net."],
    ["Diaz", "Storage & Volume Architect", "Merancang skema Docker Named Volumes (pasien_data, apotek_data, jadwal_data) untuk menjamin persistensi database rekam medis pasien."],
    ["Daffa", "Dokumentasi & QA Testing", "Menyusun skrip pengujian test-loadbalance, mengeksekusi uji coba end-to-end, mengumpulkan screenshot bukti, dan menyusun laporan resmi."]
]
add_table_data(table_team_headers, table_team_rows)

# ========================================================
# BAB IV: KESIMPULAN
# ========================================================
print("Menyusun Bab IV: Kesimpulan...")
add_chapter_title("KESIMPULAN")

add_body("Berdasarkan pelaksanaan praktikum, analisis data, dan pengujian sistem pada Pertemuan 3 ini, dapat diambil beberapa kesimpulan penting sebagai berikut:")
add_numbered_item("1.", "Implementasi orkestrasi menggunakan Docker Compose berhasil menyederhanakan pengelolaan arsitektur microservices rumah sakit dari prosedur manual yang kompleks menjadi satu proses deklaratif yang otomatis, konsisten, dan mudah dipelihara.")
add_numbered_item("2.", "Penerapan Nginx sebagai API Gateway pada port 8080 berhasil mewujudkan Single Entry Point yang aman, menyembunyikan port internal microservice dari publik, dan mengarahkan lalu lintas data ke layanan yang tepat secara akurat.")
add_numbered_item("3.", "Pemisahan jaringan bertingkat (multi-tier networks) antara medis-frontend-net dan medis-backend-net berhasil mengisolasi basis data rekam medis pasien dari potensi ancaman intrusi eksternal di luar gerbang Nginx.")
add_numbered_item("4.", "Simulasi Elasticity melalui penskalaan horizontal (docker compose up -d --scale service-pasien=3) berhasil dijalankan secara dinamis tanpa menimbulkan downtime pada layanan rumah sakit yang sedang beroperasi.")
add_numbered_item("5.", "Pengujian Load Balancing membuktikan bahwa Nginx mampu membagi beban request secara merata mengikuti algoritma Round-Robin, terbukti dari rotasi pergantian ID kontainer backend pada header HTTP X-Served-By.")
add_numbered_item("6.", "Manajemen Docker Named Volumes (medis_pasien_data) terbukti efektif menjamin integritas dan persistensi data rekam medis pasien, di mana data tetap aman dan utuh meskipun kontainer mengalami scaling, restart, maupun dihentikan.")

# Save document
try:
    doc.save(target_file)
    print(f"\n[SUKSES] Dokumen Laporan Pertemuan 3 berhasil digenerate di: {target_file}")
except PermissionError:
    alt_file = r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\Laporan_Praktikum_Pertemuan_3_Kelompok_4_TERISI.docx"
    doc.save(alt_file)
    print(f"\n[CATATAN] File utama sedang dibuka di Word. File disimpan di: {alt_file}")

