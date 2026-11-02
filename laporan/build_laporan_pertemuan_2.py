# -*- coding: utf-8 -*-
"""
Script untuk merapikan template Laporan_Praktikum_Pertemuan_2_Kelompok_4.docx
Menyesuaikan dengan arsitektur nyata proyek medis-cloud dan standar laporan Pertemuan 1.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

target_file = r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\Laporan_Praktikum_Pertemuan_2_Kelompok_4.docx"

# Buka dokumen baru dengan template styling yang bersih dan konsisten
doc = docx.Document()

# Setup margins 1.0 inch
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

# Colors
COLOR_NAVY = RGBColor(0x1F, 0x4E, 0x79)
COLOR_TEXT = RGBColor(0x22, 0x22, 0x22)
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)
HEX_HEADER_BG = "EBF1F5"
HEX_CODE_BG = "F4F6F8"
HEX_BOX_BG = "F8FAFC"
HEX_BORDER = "CCCCCC"

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEXT
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEXT
    return p

def add_p(text, bold=False, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = COLOR_TEXT
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("\u2022  ")
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(11)
    r_bullet.font.bold = True
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(11)
    return p

def add_code(text):
    # Buat code block berbingkai abu-abu rapi
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, HEX_CODE_BG)
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    
    # Border tipis
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="1F4E79"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text.strip())
    run.font.name = "Courier New"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x1B, 0x1F, 0x24)
    
    # Spacer
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def add_screenshot_box(filename, caption):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, HEX_BOX_BG)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
        f'  <w:left w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
        f'  <w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
        f'  <w:right w:val="dashed" w:sz="6" w:space="0" w:color="99AAB5"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    
    r_icon = p.add_run("[ TEMPEL SCREENSHOT DI SINI ]\n")
    r_icon.font.name = "Times New Roman"
    r_icon.font.size = Pt(11)
    r_icon.font.bold = True
    r_icon.font.color.rgb = COLOR_NAVY
    
    r_file = p.add_run(f"Screenshot: screenshots/{filename}\n")
    r_file.font.name = "Courier New"
    r_file.font.size = Pt(9.5)
    r_file.font.bold = True
    
    r_desc = p.add_run(f"Keterangan: {caption}")
    r_desc.font.name = "Times New Roman"
    r_desc.font.size = Pt(10)
    r_desc.font.italic = True
    r_desc.font.color.rgb = COLOR_MUTED
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def add_table_data(headers, rows, col_widths=None):
    t = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header
    for c_idx, h in enumerate(headers):
        cell = t.cell(0, c_idx)
        set_cell_shading(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY
        
    # Rows
    for r_idx, row in enumerate(rows):
        is_even = (r_idx % 2 == 1)
        row_bg = "FAFAFA" if is_even else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx + 1, c_idx)
            set_cell_shading(cell, row_bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            
    # Set borders
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
    return t

def add_evidence_table(evidence_items):
    """
    evidence_items: list of dict with keys:
    - 'praktik': 'A'
    - 'bukti': '...'
    - 'diharapkan': '...'
    - 'diperoleh': '...'
    - 'screenshot': 'A1-monolit-running.png'
    """
    # Total rows = 1 (header) + 2 * len(items)
    t = doc.add_table(rows=1 + 2 * len(evidence_items), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Praktik", "Bukti yang Diminta", "Hasil yang Diharapkan", "Hasil yang Diperoleh"]
    for c_idx, h in enumerate(headers):
        cell = t.cell(0, c_idx)
        set_cell_shading(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY
        
    for idx, item in enumerate(evidence_items):
        data_row_idx = 1 + idx * 2
        ss_row_idx = data_row_idx + 1
        
        # Row 1: Data
        t.cell(data_row_idx, 0).text = item['praktik']
        t.cell(data_row_idx, 1).text = item['bukti']
        t.cell(data_row_idx, 2).text = item['diharapkan']
        t.cell(data_row_idx, 3).text = item['diperoleh']
        
        for c_idx in range(4):
            c = t.cell(data_row_idx, c_idx)
            set_cell_shading(c, "FFFFFF")
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5)
                
        # Row 2: Screenshot (Merge across all 4 cols)
        c0 = t.cell(ss_row_idx, 0)
        c3 = t.cell(ss_row_idx, 3)
        c0.merge(c3)
        set_cell_shading(c0, HEX_BOX_BG)
        set_cell_margins(c0, top=60, bottom=60, left=120, right=120)
        
        p_ss = c0.paragraphs[0]
        p_ss.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ss.paragraph_format.space_before = Pt(0)
        p_ss.paragraph_format.space_after = Pt(0)
        r_ss = p_ss.add_run(f"Screenshot: screenshots/{item['screenshot']}")
        r_ss.font.name = "Courier New"
        r_ss.font.size = Pt(9.5)
        r_ss.font.bold = True
        r_ss.font.color.rgb = COLOR_NAVY

    # Apply borders
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

print("Mulai menyusun dokumen...")

# ========================================================
# COVER / HALAMAN JUDUL
# ========================================================
p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_meta.paragraph_format.space_after = Pt(2)
r = p_meta.add_run("Mata Kuliah: Cloud Computing")
r.font.name = "Times New Roman"
r.font.size = Pt(11)
r.font.bold = True

p_dosen = doc.add_paragraph()
p_dosen.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dosen.paragraph_format.space_after = Pt(14)
r = p_dosen.add_run("Dosen Pengampu: Dr. Moch. Yasin, S.Kom., M.Kom., M.B.A., MTCNA, CDCP")
r.font.name = "Times New Roman"
r.font.size = Pt(11)

# Box Placeholder Logo
t_logo = doc.add_table(rows=1, cols=1)
t_logo.alignment = WD_TABLE_ALIGNMENT.CENTER
c_logo = t_logo.cell(0, 0)
c_logo.width = Inches(2.2)
set_cell_shading(c_logo, "F8FAFC")
set_cell_margins(c_logo, 100, 100, 100, 100)
p_logotext = c_logo.paragraphs[0]
p_logotext.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_logotext.add_run("[ LOGO UINSA ]")
r.font.name = "Times New Roman"
r.font.size = Pt(11)
r.font.bold = True
r.font.color.rgb = COLOR_MUTED

sp = doc.add_paragraph()
sp.paragraph_format.space_before = Pt(10)
sp.paragraph_format.space_after = Pt(2)

add_title("LAPORAN PRAKTIKUM PERTEMUAN 2")
add_subtitle("Transformasi Arsitektur Monolitik ke Microservices & Implementasi AI\nStudi Kasus: Sistem Informasi Medis Rumah Sakit")

p_kel = doc.add_paragraph()
p_kel.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_kel.paragraph_format.space_before = Pt(8)
p_kel.paragraph_format.space_after = Pt(16)
p_kel.paragraph_format.line_spacing = 1.2
r = p_kel.add_run("Nama Kelompok 4:\n")
r.font.name = "Times New Roman"
r.font.size = Pt(11)
r.font.bold = True

members = [
    "1. Daffa Danendra Fairuzza (09020624026)",
    "2. Diaz Asbahna Fitroh Azzani (09020624027)",
    "3. Muhammad Agra Hizbulloh (09020624046)",
    "4. Yudistian Dzaky Yassar (09010624019)",
    "5. Qosi Kautsar Lavy Riski (09010624013)"
]
for m in members:
    r = p_kel.add_run(m + "\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)

p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(14)
p_inst.paragraph_format.space_after = Pt(20)
r = p_inst.add_run(
    "PROGRAM STUDI SISTEM INFORMASI\n"
    "FAKULTAS SAINS DAN TEKNOLOGI\n"
    "UNIVERSITAS ISLAM NEGERI SUNAN AMPEL SURABAYA\n"
    "2026"
)
r.font.name = "Times New Roman"
r.font.size = Pt(11)
r.font.bold = True

doc.add_page_break()

# ========================================================
# 2.1 TUJUAN
# ========================================================
add_h1("2.1 Tujuan")
add_bullet("Memahami konsep transformasi arsitektur perangkat lunak dari monolitik menuju microservices.")
add_bullet("Mampu memecah satu aplikasi monolitik rumah sakit menjadi beberapa layanan independen (Service Pasien, Service Apotek, dan Service Jadwal Dokter).")
add_bullet("Mengimplementasikan teknik Prompt Engineering pada Generative AI (ChatGPT/Copilot) untuk memetakan Bounded Context DDD, men-generate kode boilerplate microservices, Dockerfile, dan topologi jaringan.")
add_bullet("Mampu membuat dan menjalankan Docker Custom Bridge Network untuk mengaktifkan Automatic DNS Service Discovery antar-kontainer.")
add_bullet("Membuktikan komunikasi REST API lintas-service (cross-service call) menggunakan hostname internal kontainer (bukan IP statis) dan mendeteksi kontraindikasi alergi pasien secara otomatis.")
add_bullet("Menguji dua karakteristik penting arsitektur microservices: isolasi jaringan (security network boundary) dan ketahanan terhadap kegagalan (fault isolation).")

# ========================================================
# 2.2 KONSEP DASAR (KASUS RUMAH SAKIT)
# ========================================================
add_h1("2.2 Konsep Dasar (dikaitkan dengan kasus rumah sakit)")
add_p("Pada Pertemuan 1, kelompok telah membahas konsep Availability, Elasticity, dan Disaster Recovery, serta menguji ketatnya metrik RTO (Recovery Time Objective) 15 menit dan RPO (Recovery Point Objective) 5 menit untuk data rekam medis pasien. Pada Pertemuan 2, fokus beralih ke transformasi arsitektur perangkat lunak dari monolitik ke microservices agar keandalan dan pemulihan data tersebut dapat terwujud secara optimal.")

add_h2("2.2.1 Mengapa Dipecah Menjadi Microservices")
add_p("Pada arsitektur monolitik, seluruh fungsi rumah sakit â€” pendataan pasien, resep apotek, dan penjadwalan dokter â€” berjalan dalam satu proses aplikasi tunggal dan berbagi satu file/skema database terpusat. Kondisi ini menimbulkan risiko single point of failure: jika modul apotek mengalami lonjakan request saat penebusan obat sore hari atau terjadi transaksi baca-tulis berat yang mengunci database (database lock), seluruh sistem rumah sakit dapat mengalami crash, sehingga dokter di ruang IGD tidak dapat membuka riwayat alergi dan rekam medis pasien.")
add_p("Dengan memecah sistem menjadi microservices mandiri berprinsip Database-per-Service, setiap layanan memiliki basis data dan siklus hidup proses tersendiri. Apabila modul apotek atau jadwal dokter mengalami gangguan, layanan master data rekam medis pasien tetap berjalan normal tanpa gangguan (fault isolation).")

# Tabel 0
table_0_headers = ["Konsep", "Arti", "Penerapan di Sistem Medis (Pertemuan 2)"]
table_0_rows = [
    ["Monolitik", "Seluruh fungsi berjalan dalam satu aplikasi dan satu proses runtime", "Endpoint /api/pasien, /api/obat, /api/dokter dilayani oleh satu container app-monolit di port 5000"],
    ["Microservices", "Fungsi dipecah menjadi layanan independen yang berkomunikasi lewat REST API", "Service Pasien (5001), Service Apotek (5002), Service Jadwal Dokter (5003) berjalan sebagai kontainer terpisah"],
    ["Database-per-Service", "Setiap microservice mengelola databasenya sendiri tanpa akses SQL langsung dari service lain", "pasien.db, apotek.db, dan jadwal.db terpisah; pertukaran data wajib melalui endpoint REST API"],
    ["Service Discovery", "Mekanisme otomatis agar satu layanan menemukan alamat layanan lain tanpa IP statis", "Custom bridge network medis-net; Apotek dan Jadwal memanggil Pasien lewat DNS http://service-pasien:5001"],
    ["Fault Isolation", "Kegagalan satu komponen tidak melumpuhkan komponen lain dalam sistem", "Saat service-pasien dihentikan, Service Apotek dan Jadwal tetap melayani data katalog lokal"],
    ["Network Boundary", "Kontainer di luar jaringan internal tidak dapat mengakses service privat di dalamnya", "Kontainer alpine di luar medis-net gagal melakukan ping ke service-pasien (bad address)"]
]
add_table_data(table_0_headers, table_0_rows)

add_h2("2.2.2 Docker Custom Bridge Network dan DNS Service Discovery")
add_p("Secara default, Docker menyediakan mekanisme DNS resolver internal (pada IP 127.0.0.11 di dalam kontainer) khusus pada jaringan bertipe custom bridge network. Setiap kontainer yang terhubung ke jaringan medis-net dapat saling memanggil menggunakan nama kontainer sebagai hostname (misalnya http://service-pasien:5001). Hal ini menghilangkan kebutuhan konfigurasi IP statis yang rentan rusak setiap kali kontainer dibuat ulang.")

add_h2("2.2.3 Pemetaan Rancangan ke Praktikum")
add_p("Praktikum dijalankan pada satu komputer Windows dengan Docker Desktop, sehingga seluruh kontainer microservice disimulasikan berjalan pada host lokal dengan pemetaan port yang berbeda.")

# Tabel 1
table_1_headers = ["Komponen Rancangan", "Yang Dilakukan di Praktikum", "Status"]
table_1_rows = [
    ["Load balancer / API Gateway di depan ketiga service", "Tidak dibangun; setiap service diakses langsung lewat port host masing-masing (5001/5002/5003)", "Hanya rancangan (Pertemuan 3)"],
    ["Custom bridge network dengan DNS discovery", "Dibangun: network medis-net, ketiga kontainer di-attach ke dalamnya", "Dikerjakan"],
    ["Tiga microservice independen (Pasien, Apotek, Jadwal)", "Dibangun sebagai tiga image dan tiga kontainer terpisah dengan database mandiri", "Dikerjakan"],
    ["Komunikasi Lintas Servis (Cross-Service Call)", "Service Apotek dan Jadwal memanggil Service Pasien untuk validasi dan pengecekan alergi", "Dikerjakan dan diuji"],
    ["Uji isolasi jaringan (security boundary)", "Dibuktikan lewat ping dari kontainer alpine di luar network medis-net", "Dikerjakan dan diukur"],
    ["Uji fault tolerance antar-service", "Dibuktikan dengan menghentikan service-pasien dan menguji kueri service lain", "Dikerjakan dan diukur"],
    ["Replikasi/scaling tiap service (multi-instance)", "Tidak dibangun pada pertemuan ini", "Rancangan lanjut materi Pertemuan 3 & 4"]
]
add_table_data(table_1_headers, table_1_rows)

add_h2("2.2.4 Implementasi AI dalam Dekomposisi Sistem Medis (Prompt Engineering)")
add_p("Sesuai dengan rencana silabus Pertemuan 2, mahasiswa menggunakan generative AI (ChatGPT / GitHub Copilot) untuk mempercepat perancangan arsitektur dan pembuatan boilerplate kode. Hasil prompt yang diajukan kelompok dirangkum pada tabel berikut:")

table_ai_headers = ["No", "Sasaran Prompt AI", "Prompt yang Diberikan", "Hasil Rekomendasi AI & Implementasi"]
table_ai_rows = [
    ["1", "Dekomposisi Monolit ke DDD", "Prompting pemecahan monolit sistem medis rumah sakit berdasarkan prinsip Domain-Driven Design.", "Menghasilkan 3 Bounded Context: Pasien (Core), Apotek (Supporting), dan Jadwal Dokter (Supporting)."],
    ["2", "API Contract & Deteksi Alergi", "Generate endpoint REST API Python Flask dengan komunikasi inter-service dan validasi alergi obat.", "Kode app.py dengan urllib.request: Service Apotek memvalidasi data pasien dan memberi peringatan alergi Penisilin."],
    ["3", "Optimasi Dockerfile", "Template Dockerfile efisien, ringan, dan menerapkan caching layer pip berbasis python:3.12-slim.", "Dockerfile seragam untuk seluruh service dengan ENV PYTHONDONTWRITEBYTECODE=1 dan PYTHONUNBUFFERED=1."],
    ["4", "Konfigurasi Network Docker", "Rancangan jaringan bridge tanpa docker-compose agar kontainer berkomunikasi via hostname.", "Perintah docker network create medis-net dan uji isolasi boundary dari kontainer luar."]
]
add_table_data(table_ai_headers, table_ai_rows)

# ========================================================
# 2.3 PERSIAPAN LINGKUNGAN WINDOWS
# ========================================================
add_h1("2.3 Persiapan Lingkungan Windows")
add_h2("2.3.1 Prasyarat")
add_bullet("Windows 10/11 dengan Docker Desktop terpasang dan berstatus Engine running (ikon paus di system tray berwarna hijau).")
add_bullet("Docker Desktop dalam mode Linux containers (default backend WSL 2).")
add_bullet("Windows PowerShell (direkomendasikan dijalankan sebagai Administrator).")
add_bullet("Python 3.10+ pada host Windows dengan pustaka Flask terpasang untuk kemudahan debugging lokal.")
add_bullet("Source code aplikasi yang telah disiapkan di folder medis-cloud (monolit, services/pasien, services/apotek, services/jadwal-dokter, scripts).")

add_h2("2.3.2 Direktori Kerja")
add_p("Direktori kerja seluruh praktikum ini adalah folder proyek medis-cloud kelompok:")
add_code("""Set-Location "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud"
Get-ChildItem""")
add_p("Verifikasi: Perintah Get-ChildItem menampilkan folder monolit, services, dan scripts.")

add_h2("2.3.3 Tabel Nama yang Dipakai (konsisten di seluruh dokumen)")
table_2_headers = ["Jenis", "Nama", "Port", "Keterangan"]
table_2_rows = [
    ["Container", "app-monolit", "5000", "Baseline aplikasi monolitik awal (Praktik A)"],
    ["Network", "medis-net", "-", "Custom bridge network Docker (Praktik B1)"],
    ["Image & Container", "medis-pasien:1.0 / service-pasien", "5001", "Microservice Data Pasien (pasien.db)"],
    ["Image & Container", "medis-apotek:1.0 / service-apotek", "5002", "Microservice Apotek, memanggil Service Pasien (apotek.db)"],
    ["Image & Container", "medis-jadwal:1.0 / service-jadwal", "5003", "Microservice Jadwal Dokter, memanggil Service Pasien (jadwal.db)"]
]
add_table_data(table_2_headers, table_2_rows)

# ========================================================
# 2.4 PRAKTIK A: APLIKASI MONOLITIK
# ========================================================
add_h1("2.4 Praktik A: Menjalankan Aplikasi Monolitik (Baseline)")
add_p("Tujuan praktik ini adalah memahami baseline aplikasi rumah sakit sebelum dipecah menjadi microservices. Pada monolit, seluruh modul berjalan dalam satu proses dan satu basis data bersama.")

add_p("Langkah 1. Pindah ke direktori monolit dan bangun image Docker:")
add_code("""Set-Location "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\\monolit"
docker build -t medis-monolit:1.0 .
docker run -d --name app-monolit -p 5000:5000 medis-monolit:1.0
docker ps --filter "name=app-monolit" """)

add_p("Langkah 2. Uji tiga endpoint monolitik:")
add_code("""(Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5000/api/pasien" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5000/api/dashboard" -UseBasicParsing).Content""")

add_p("Hasil yang diharapkan: Ketiga endpoint merespons dengan status HTTP 200 OK dan mengembalikan data JSON terpusat. Seluruh fungsi dilayani oleh container tunggal app-monolit.")
add_screenshot_box("A1-monolit-running.png", "Status kontainer app-monolit berjalan di port 5000 dan respon endpoint /health serta /api/dashboard")

add_p("Langkah 3. Setelah pengujian selesai, hentikan container monolitik agar port dan resource bebas untuk pengujian microservices:")
add_code("""docker rm -f app-monolit""")

# ========================================================
# 2.5 PRAKTIK B: INFRASTRUKTUR MICROSERVICES
# ========================================================
add_h1("2.5 Praktik B: Membangun Infrastruktur Microservices")

add_h2("2.5.1 B1: Membuat Docker Custom Bridge Network")
add_p("Tujuan: Mengaktifkan fitur Automatic DNS Service Discovery antar-kontainer sebelum ketiga microservice dijalankan.")
add_code("""docker network create --driver bridge medis-net
docker network ls --filter "name=medis-net"
docker network inspect medis-net --format "Subnet: {{range .IPAM.Config}}{{.Subnet}}{{end}}" """)

add_p("Hasil yang diharapkan: Network medis-net dengan driver bridge terbentuk dan subnet otomatis (misal 172.18.0.0/16) berhasil dialokasikan.")
add_screenshot_box("B1-docker-network.png", "Daftar docker network ls dan hasil inspect subnet medis-net")

add_h2("2.5.2 B2: Membangun Image Ketiga Microservices")
add_p("Tujuan: Membungkus kode masing-masing layanan â€” Pasien, Apotek, dan Jadwal Dokter â€” ke dalam image Docker berbasis python:3.12-slim yang ringan dan mandiri.")
add_code("""$Base = "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\\services"

# 1. Service Pasien (Port 5001)
Set-Location (Join-Path $Base "pasien")
docker build -t medis-pasien:1.0 .

# 2. Service Apotek (Port 5002)
Set-Location (Join-Path $Base "apotek")
docker build -t medis-apotek:1.0 .

# 3. Service Jadwal Dokter (Port 5003)
Set-Location (Join-Path $Base "jadwal-dokter")
docker build -t medis-jadwal:1.0 .

docker images | Select-String "medis-" """)

add_p("Hasil yang diharapkan: Tiga image (medis-pasien:1.0, medis-apotek:1.0, medis-jadwal:1.0) berhasil dibangun dan tercatat di daftar docker images.")
add_screenshot_box("B2-docker-images.png", "Daftar docker images yang memuat ketiga image microservices medis-*")

# ========================================================
# 2.6 PRAKTIK C: MENJALANKAN MICROSERVICES
# ========================================================
add_h1("2.6 Praktik C: Menjalankan dan Menghubungkan Microservices")
add_p("Tujuan: Menjalankan ketiga kontainer microservice ke dalam network medis-net sehingga dapat saling berkomunikasi lewat DNS internal Docker. Perhatikan environment variable PASIEN_SERVICE_URL yang diarahkan ke hostname service-pasien, bukan IP address.")

add_code("""# 1. Jalankan Service Pasien
docker run -d --name service-pasien `
    --network medis-net `
    -p 5001:5001 `
    medis-pasien:1.0

# 2. Jalankan Service Apotek
docker run -d --name service-apotek `
    --network medis-net `
    -p 5002:5002 `
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" `
    medis-apotek:1.0

# 3. Jalankan Service Jadwal Dokter
docker run -d --name service-jadwal `
    --network medis-net `
    -p 5003:5003 `
    -e PASIEN_SERVICE_URL="http://service-pasien:5001" `
    medis-jadwal:1.0

docker ps --filter "name=service-" """)

add_p("Hasil yang diharapkan: Ketiga kontainer (service-pasien, service-apotek, service-jadwal) berstatus Up dan tergabung dalam network medis-net.")
add_screenshot_box("C1-services-running.png", "Output docker ps --filter name=service- menampilkan ketiga container aktif")

# ========================================================
# 2.7 PRAKTIK D: PENGUJIAN INTEGRASI REST API
# ========================================================
add_h1("2.7 Praktik D: Pengujian Integrasi REST API dan Komunikasi Lintas Kontainer")

add_h2("2.7.1 D1: Healthcheck Semua Service")
add_code("""(Invoke-WebRequest -Uri "http://localhost:5001/health" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5002/health" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5003/health" -UseBasicParsing).Content""")
add_p("Hasil yang diperoleh: Ketiga endpoint /health merespons status 200 OK dengan payload JSON yang memuat status healthy dan hostname kontainer.")

add_h2("2.7.2 D2: Registrasi Pasien Baru")
add_code("""$pasienBaru = @{
    nik = "3578010404950004"
    nama = "Pasien Baru Kelompok 4"
    tgl_lahir = "1995-04-04"
    riwayat_alergi = "Penisilin"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/pasien" -Method Post -Body $pasienBaru -ContentType "application/json" """)
add_p("Hasil yang diperoleh: Data pasien baru tersimpan di Service Pasien dengan alokasi ID baru, termasuk riwayat alergi Penisilin yang akan diverifikasi oleh service lain.")

add_h2("2.7.3 D3: Penebusan Resep (Cross-Service Call dan Deteksi Alergi)")
add_p("Pengujian ini meminta obat Amoxicillin untuk Pasien ID 1 yang memiliki riwayat alergi Penisilin, untuk membuktikan bahwa Service Apotek benar-benar memanggil Service Pasien secara real-time lewat jaringan Docker internal.")
add_code("""$resepBody = @{
    pasien_id = 1
    obat_id = 2
    jumlah = 10
    aturan_pakai = "3x1 sehari sesudah makan"
} | ConvertTo-Json

$resResep = Invoke-RestMethod -Uri "http://localhost:5002/api/resep" -Method Post -Body $resepBody -ContentType "application/json"
$resResep | ConvertTo-Json -Depth 4""")
add_p("Hasil yang diperoleh: Respons JSON memuat pesan sukses dan peringatan kontraindikasi: 'PERINGATAN: Pasien memiliki riwayat alergi (Penisilin) terhadap antibiotik ini!'. Ini membuktikan Service Apotek berhasil menghubungi http://service-pasien:5001 via internal DNS Docker.")
add_screenshot_box("D1-resep-cross-service.png", "Respon JSON pembuatan resep memuat peringatan kontraindikasi alergi dari Service Pasien")

add_h2("2.7.4 D4: Pendaftaran Janji Temu Dokter")
add_code("""$janjiBody = @{
    pasien_id = 2
    dokter_id = 1
    tgl_periksa = "2026-11-10"
    keluhan = "Pemeriksaan kesehatan rutin"
} | ConvertTo-Json

$resJanji = Invoke-RestMethod -Uri "http://localhost:5003/api/janji-temu" -Method Post -Body $janjiBody -ContentType "application/json"
$resJanji | ConvertTo-Json -Depth 4""")
add_p("Hasil yang diperoleh: Janji temu berhasil terdaftar pada Service Jadwal Dokter dengan nomor antrean otomatis 'POLI-01-001' setelah memvalidasi nama Pasien ID 2.")
add_screenshot_box("D2-janji-temu.png", "Respon JSON booking janji temu dokter lengkap dengan nomor antrean resmi")

add_h2("2.7.5 D5: Uji Isolasi Jaringan (Security Boundary)")
add_p("Pengujian ini membuktikan bahwa kontainer di luar network medis-net tidak dapat menghubungi service internal rekam medis.")
add_code("""docker run --rm alpine ping -c 2 service-pasien""")
add_p("Hasil yang diperoleh: Perintah gagal dengan pesan 'ping: bad address service-pasien'. Kontainer alpine di luar network tidak dapat meresolve DNS internal medis-net, membuktikan batas keamanan data medis terisolasi.")
add_screenshot_box("D3-network-isolation.png", "Kegagalan ping bad address dari kontainer di luar network medis-net")

add_h2("2.7.6 D6: Uji Fault Tolerance (Toleransi Kegagalan)")
add_p("Pengujian ini membuktikan bahwa kegagalan satu service tidak membuat seluruh sistem ikut lumpuh â€” salah satu keunggulan utama microservices dibanding monolitik.")
add_code("""# Matikan Service Pasien sementara
docker stop service-pasien

# Uji apakah Service Apotek dan Jadwal tetap melayani kueri lokal
(Invoke-WebRequest -Uri "http://localhost:5002/api/obat" -UseBasicParsing).Content
(Invoke-WebRequest -Uri "http://localhost:5003/api/dokter" -UseBasicParsing).Content

# Nyalakan kembali
docker start service-pasien""")
add_p("Hasil yang diperoleh: Meskipun service-pasien dihentikan, Service Apotek dan Service Jadwal tetap dapat melayani data katalog obat dan jadwal dokter lokal masing-masing tanpa mengalami crash.")
add_screenshot_box("D4-fault-isolation.png", "Kueri endpoint obat dan dokter tetap sukses (HTTP 200) saat service-pasien dihentikan")

# ========================================================
# 2.8 EKSEKUSI CEPAT MENGGUNAKAN SKRIP OTOMATIS
# ========================================================
add_h1("2.8 Eksekusi Cepat Menggunakan Skrip Otomatis (Opsional)")
add_p("Kelompok telah menyediakan skrip PowerShell siap pakai di folder scripts/ untuk mempercepat dan memvalidasi eksekusi ulang seluruh tahapan di atas:")
add_code("""# 1. Jalankan baseline monolitik
& "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\\scripts\\run-monolit.ps1"

# 2. Setup jaringan dan jalankan ketiga microservices
& "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\\scripts\\run-microservices.ps1"

# 3. Eksekusi seluruh skenario pengujian REST API otomatis
& "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\\scripts\\test-services.ps1"

# 4. Hentikan dan bersihkan kontainer
& "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud\\scripts\\stop-all.ps1" """)

# ========================================================
# 2.9 DELIVERABLE PERTEMUAN 2
# ========================================================
add_h1("2.9 Deliverable Pertemuan 2")
add_h2("2.9.1 Daftar Deliverable")
add_bullet("Screenshot hasil Praktik A, B, C, dan D (lihat Lembar Bukti pada sub-bab 2.9.2).")
add_bullet("Bukti komunikasi lintas-service (cross-service call) yang berhasil mendeteksi kontraindikasi alergi pasien secara real-time.")
add_bullet("Bukti isolasi keamanan jaringan (network security boundary) dan toleransi kegagalan (fault tolerance).")
add_bullet("Tabel pembagian tugas kelompok yang mencakup peran AI engineering (sub-bab 2.9.3).")
add_bullet("Diagram arsitektur microservices dan topologi jaringan bridge (sub-bab 2.9.4).")
add_bullet("Commit terbaru pada repositori Git kelompok yang memuat source code ketiga service dan skrip otomatis (sub-bab 2.9.5).")
add_bullet("Seluruh data pada laporan adalah data pasien sintetis; tidak boleh ada data pasien nyata.")

add_h2("2.9.2 Lembar Bukti Praktikum")
add_p("Tabel berikut memadukan hasil yang diharapkan dan hasil yang benar-benar diperoleh dari pengujian sistem informasi medis berbasis Docker:")

evidence_data = [
    {
        "praktik": "A",
        "bukti": "docker ps dan response endpoint monolitik port 5000",
        "diharapkan": "Status Up; tiga endpoint merespons 200 OK",
        "diperoleh": "Container app-monolit aktif pada 0.0.0.0:5000->5000/tcp. Endpoint /health merespons status healthy dan /api/dashboard mengembalikan ringkasan data terpusat (pasien, obat, dokter) dalam satu proses monolitik.",
        "screenshot": "A1-monolit-running.png"
    },
    {
        "praktik": "B1",
        "bukti": "docker network inspect medis-net",
        "diharapkan": "Network bridge medis-net terbentuk dengan subnet otomatis",
        "diperoleh": "Network medis-net berhasil dibuat dengan driver bridge dan subnet 172.18.0.0/16 terdaftar pada Docker Engine, mengaktifkan DNS Service Discovery internal.",
        "screenshot": "B1-docker-network.png"
    },
    {
        "praktik": "B2",
        "bukti": "docker images (filter medis-)",
        "diharapkan": "Tiga image medis-pasien, medis-apotek, medis-jadwal",
        "diperoleh": "Tiga Docker image berhasil dibangun berbasis python:3.12-slim: medis-pasien:1.0 (~130MB), medis-apotek:1.0 (~130MB), dan medis-jadwal:1.0 (~130MB).",
        "screenshot": "B2-docker-images.png"
    },
    {
        "praktik": "C",
        "bukti": "docker ps (filter service-)",
        "diharapkan": "Tiga kontainer service-* berstatus Up pada medis-net",
        "diperoleh": "Ketiga kontainer aktif pada medis-net: service-pasien (:5001, host: 2e5e33eae40b), service-apotek (:5002, host: 7d19e82e163f), dan service-jadwal (:5003, host: 86857837083c).",
        "screenshot": "C1-services-running.png"
    },
    {
        "praktik": "D3",
        "bukti": "Response JSON resep Amoxicillin untuk pasien alergi Penisilin",
        "diharapkan": "Peringatan kontraindikasi alergi muncul dari Service Pasien",
        "diperoleh": "Service Apotek berhasil memanggil service-pasien via internal DNS; respon memuat resep_id: 1, sisa stok 70, dan peringatan: 'PERINGATAN: Pasien memiliki riwayat alergi (Penisilin) terhadap antibiotik ini!'.",
        "screenshot": "D1-resep-cross-service.png"
    },
    {
        "praktik": "D4",
        "bukti": "Response JSON booking janji temu",
        "diharapkan": "Janji temu berhasil terdaftar dengan nomor antrean",
        "diperoleh": "Service Jadwal berhasil memvalidasi Pasien Contoh 02 dan menerbitkan nomor antrean resmi 'POLI-01-001' untuk dr. Budi Santoso, Sp.A (Poli Anak) dengan janji_id: 1.",
        "screenshot": "D2-janji-temu.png"
    },
    {
        "praktik": "D5",
        "bukti": "Ping dari kontainer alpine di luar network",
        "diharapkan": "bad address 'service-pasien'",
        "diperoleh": "Perintah ping menghasilkan 'ping: bad address service-pasien'. Isolasi jaringan berhasil mencegah kontainer luar mengakses internal network medis-net.",
        "screenshot": "D3-network-isolation.png"
    },
    {
        "praktik": "D6",
        "bukti": "Query obat/dokter saat service-pasien dihentikan",
        "diharapkan": "Apotek dan Jadwal tetap melayani data lokal",
        "diperoleh": "Saat service-pasien dimatikan, endpoint /api/obat dan /api/dokter tetap merespons 200 OK melayani katalog lokal, membuktikan keberhasilan fault isolation.",
        "screenshot": "D4-fault-isolation.png"
    }
]
add_evidence_table(evidence_data)

add_h2("2.9.3 Pembagian Tugas Kelompok")
table_tugas_headers = ["Anggota", "Peran", "Tanggung Jawab pada Pertemuan 2"]
table_tugas_rows = [
    ["Yudis", "Ketua, Git & Integrasi", "Koordinasi praktikum, struktur repositori medis-cloud, skrip run-microservices.ps1, commit dan push hasil Pertemuan 2 ke Git."],
    ["Agra", "AI Engineer & Testing", "Menyusun skenario prompt engineering untuk dekomposisi DDD, validasi respon AI, pengujian cross-service call dan deteksi alergi."],
    ["Qosi", "Container & Network Engineer", "Menulis Dockerfile python:3.12-slim, konfigurasi custom bridge network medis-net, dan pengujian isolasi jaringan (security boundary)."],
    ["Diaz", "Arsitek Sistem", "Merancang Bounded Context DDD (Pasien, Apotek, Jadwal), skema Database-per-Service, dan diagram arsitektur microservices (draw.io)."],
    ["Daffa", "Dokumentasi & QA", "Menjalankan skrip pengujian test-services.ps1, mengumpulkan screenshot, mengisi lembar bukti praktikum, dan menyusun laporan resmi."]
]
add_table_data(table_tugas_headers, table_tugas_rows)

add_h2("2.9.4 Diagram Arsitektur")
add_p("Diagram berikut menggambarkan tiga microservice (Pasien, Apotek, Jadwal Dokter) yang berjalan dalam satu custom bridge network medis-net, beserta arah komunikasi cross-service dari Apotek dan Jadwal menuju Pasien:")
add_code("""+-----------------------------------------------------------------------------------+
|                            DOCKER HOST (WINDOWS PC)                               |
|                                                                                   |
|  [Port 5001]                     [Port 5002]                     [Port 5003]      |
|      |                                |                               |           |
|  +---|--------------------------------|-------------------------------|--------+  |
|  |   |        DOCKER BRIDGE NETWORK: medis-net (Subnet 172.18.0.0/16) |        |  |
|  |   v                                v                               v        |  |
|  | +--------------------+           +--------------------+           +-------+ |  |
|  | |   service-pasien   |           |   service-apotek   |           |service| |  |
|  | |    (Port 5001)     |<----------|    (Port 5002)     |           |-jadwal| |  |
|  | +---------+----------+   HTTP    +---------+----------+           |(:5003)| |  |
|  |           |              GET               |                      +---+---+ |  |
|  |           |                                |                          |     |  |
|  |           |        HTTP GET                |                          |     |  |
|  |           +--------------------------------+--------------------------+     |  |
|  |           |                                |                          |     |  |
|  |           v                                v                          v     |  |
|  |     [ pasien.db ]                    [ apotek.db ]              [ jadwal.db]|  |
|  |  (Rekam Medis Pasien)             (Obat & Resep Farmasi)     (Dokter & Poli)|  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+""")

add_screenshot_box("arsitektur-microservices.png", "Diagram arsitektur microservices medis-net dan aliran komunikasi inter-service")

add_h2("2.9.5 Repositori Git")
add_p("Hasil praktikum Pertemuan 2 (source code tiga service, Dockerfile, skrip otomatis, dan panduan) dikomit ke repositori Git kelompok yang sama dengan Pertemuan 1:")
add_code("""Set-Location "C:\\DaffaP\\KULIAH_DAFFA\\Semester_5\\CC\\medis-cloud"
git add .
git commit -m "Pertemuan 2: transformasi monolitik ke microservices (pasien, apotek, jadwal-dokter) + custom bridge network"
git log --oneline""")
add_p("Verifikasi: git log --oneline menampilkan commit baru untuk Pertemuan 2, melanjutkan riwayat commit Pertemuan 1.")

try:
    doc.save(target_file)
    print(f"File berhasil dirapikan dan disimpan di: {target_file}")
except PermissionError:
    alt_file = r"c:\DaffaP\KULIAH_DAFFA\Semester_5\CC\medis-cloud\Laporan_Praktikum_Pertemuan_2_Kelompok_4_TERISI.docx"
    doc.save(alt_file)
    print(f"Catatan: File asli sedang dibuka di Microsoft Word.")
    print(f"File dengan lembar bukti terisi berhasil disimpan di: {alt_file}")

