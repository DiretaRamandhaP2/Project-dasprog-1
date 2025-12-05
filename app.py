from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Inisialisasi aplikasi Flask
app = Flask(__name__)

"""
ALUR SISTEM DIAGNOSIS PENYAKIT:
1. User mengisi form data pasien dan gejala di frontend
2. Data dikirim ke endpoint /diagnosis via POST request
3. Sistem membandingkan gejala dengan database penyakit
4. Menghitung persentase kecocokan untuk setiap penyakit
5. Menentukan status dan rekomendasi berdasarkan persentase
6. Menyimpan riwayat diagnosis ke dalam list RIWAYAT_PASIEN
7. Mengembalikan hasil diagnosis ke frontend
8. User bisa melihat riwayat semua pasien di halaman /riwayat-pasien
"""

# Database pengetahuan penyakit dan gejalanya
# Struktur: Dictionary dengan key sebagai ID penyakit dan value berisi informasi lengkap
PENYAKIT_DATABASE = {
    "flu": {
        "nama": "Influenza (Flu)",
        "gejala": ["demam", "batuk", "pilek", "sakit tenggorokan", "sakit kepala", "nyeri otot"],
        "deskripsi": "Infeksi virus pada sistem pernapasan",
        "penanganan": "Istirahat, banyak minum air, obat penurun demam"
    },
    "demam_berdarah": {
        "nama": "Demam Berdarah Dengue (DBD)",
        "gejala": ["demam tinggi", "sakit kepala parah", "nyeri belakang mata", "nyeri otot", "mual", "muntah", "ruam kulit"],
        "deskripsi": "Penyakit yang ditularkan melalui nyamuk Aedes",
        "penanganan": "Segera ke rumah sakit, istirahat total, banyak cairan"
    },
    "tipus": {
        "nama": "Tifus (Typhoid Fever)",
        "gejala": ["demam tinggi", "sakit perut", "sakit kepala", "lemas", "hilang nafsu makan", "diare atau sembelit"],
        "deskripsi": "Infeksi bakteri Salmonella typhi",
        "penanganan": "Antibiotik, istirahat, makanan lunak"
    },
    "maag": {
        "nama": "Gastritis (Maag)",
        "gejala": ["sakit perut", "mual", "muntah", "perut kembung", "nafsu makan menurun", "heartburn"],
        "deskripsi": "Peradangan pada lapisan lambung",
        "penanganan": "Hindari makanan pedas/berminyak, makan teratur, obat maag"
    },
    "diare": {
        "nama": "Gastroenteritis (Diare)",
        "gejala": ["diare", "mual", "muntah", "sakit perut", "demam ringan", "lemas"],
        "deskripsi": "Infeksi pada saluran pencernaan",
        "penanganan": "Banyak cairan, oralit, hindari makanan berat"
    }
}

# Database untuk menyimpan riwayat pasien
# Ini disimpan dalam memory (list), dalam production sebaiknya menggunakan database
RIWAYAT_PASIEN = []

def diagnosa_penyakit(gejala_pasien):
    """
    FUNGSI UTAMA UNTUK DIAGNOSIS PENYAKIT:
    
    Alur:
    1. Untuk setiap penyakit dalam database, bandingkan gejala pasien dengan gejala penyakit
    2. Hitung gejala yang cocok dan tidak cocok
    3. Hitung persentase kecocokan = (gejala cocok / total gejala penyakit) * 100
    4. Hanya tampilkan penyakit yang memiliki minimal 1 gejala cocok
    5. Urutkan berdasarkan persentase tertinggi
    
    Parameter:
    - gejala_pasien: list gejala yang diinput oleh user
    
    Return:
    - List hasil diagnosis yang sudah diurutkan
    """
    hasil_diagnosa = []
    
    # Loop melalui setiap penyakit dalam database
    for penyakit_id, info_penyakit in PENYAKIT_DATABASE.items():
        gejala_cocok = []
        gejala_tidak_cocok = []
        
        # Bandingkan setiap gejala pasien dengan gejala penyakit
        for gejala in gejala_pasien:
            if gejala.lower() in [g.lower() for g in info_penyakit["gejala"]]:
                gejala_cocok.append(gejala)  # Gejala cocok dengan penyakit
            else:
                gejala_tidak_cocok.append(gejala)  # Gejala tidak cocok
        
        # Hitung persentase kecocokan
        # Rumus: (jumlah gejala cocok / total gejala penyakit) * 100
        persentase = (len(gejala_cocok) / len(info_penyakit["gejala"])) * 100
        
        # Hanya tambahkan ke hasil jika ada minimal 1 gejala yang cocok
        if len(gejala_cocok) > 0:
            hasil_diagnosa.append({
                "penyakit": info_penyakit["nama"],
                "persentase": round(persentase, 1),  # Bulatkan 1 angka desimal
                "gejala_cocok": gejala_cocok,
                "gejala_tidak_cocok": gejala_tidak_cocok,
                "deskripsi": info_penyakit["deskripsi"],
                "penanganan": info_penyakit["penanganan"],
                "kecocokan": len(gejala_cocok)  # Jumlah gejala yang cocok
            })
    
    # Urutkan berdasarkan persentase tertinggi ke terendah
    hasil_diagnosa.sort(key=lambda x: x["persentase"], reverse=True)
    
    return hasil_diagnosa

@app.route('/')
def home():
    """
    ROUTE: Halaman Utama
    Menampilkan form input untuk diagnosis penyakit baru
    """
    return render_template('index.html')

@app.route('/riwayat-pasien')
def riwayat_pasien():
    """
    ROUTE: Halaman Riwayat Pasien
    Menampilkan semua data pasien yang pernah didiagnosis
    """
    return render_template('riwayat_pasien.html')

@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    """
    ROUTE: Endpoint Diagnosis (POST)
    
    Alur Proses:
    1. Menerima data JSON dari frontend (nama, umur, tinggi, gejala)
    2. Memproses diagnosis dengan fungsi diagnosa_penyakit()
    3. Menentukan status berdasarkan persentase kecocokan
    4. Memberikan rekomendasi sesuai status
    5. Menyimpan riwayat ke database sementara
    6. Mengembalikan hasil diagnosis dalam format JSON
    
    Kriteria Status:
    - >70%: Kemungkinan tinggi -> Rekomendasi ke dokter
    - 40-70%: Kemungkinan sedang -> Observasi lanjutan
    - <40%: Kemungkinan rendah -> Jaga kesehatan
    - 0%: Tidak terdeteksi -> Konsultasi dokter
    """
    # Ambil data dari request JSON
    data = request.json
    nama = data['nama']
    umur = data['umur']
    tinggi = data['tinggi']
    gejala_list = data['gejala']
    
    # Diagnosa penyakit berdasarkan gejala menggunakan fungsi utama
    hasil_diagnosa = diagnosa_penyakit(gejala_list)
    
    # Tentukan status dan rekomendasi berdasarkan hasil diagnosa
    if hasil_diagnosa:
        penyakit_utama = hasil_diagnosa[0]  # Ambil penyakit dengan persentase tertinggi
        
        if penyakit_utama["persentase"] > 70:
            status = "Kemungkinan tinggi"
            rekomendasi = f"Disarankan untuk segera memeriksakan diri ke dokter untuk {penyakit_utama['penyakit']}"
        elif penyakit_utama["persentase"] > 40:
            status = "Kemungkinan sedang"
            rekomendasi = f"Perlu observasi lebih lanjut untuk {penyakit_utama['penyakit']}"
        else:
            status = "Kemungkinan rendah"
            rekomendasi = "Tetap jaga kesehatan dan observasi gejala"
    else:
        # Jika tidak ada penyakit yang cocok
        status = "Tidak terdeteksi"
        rekomendasi = "Gejala tidak cocok dengan penyakit yang dikenal. Konsultasi dokter jika gejala berlanjut."
    
    # Simpan ke riwayat pasien untuk akses future
    riwayat = {
        "id": len(RIWAYAT_PASIEN) + 1,  # ID auto increment
        "nama": nama,
        "umur": umur,
        "tinggi": tinggi,
        "gejala": gejala_list,
        "jumlah_gejala": len(gejala_list),
        "status": status,
        "rekomendasi": rekomendasi,
        "hasil_diagnosa": hasil_diagnosa[:3],  # Simpan hanya 3 penyakit teratas
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
    }
    RIWAYAT_PASIEN.append(riwayat)
    
    # Return response JSON ke frontend
    return jsonify({
        'nama': nama,
        'umur': umur,
        'tinggi': tinggi,
        'gejala': gejala_list,
        'jumlah_gejala': len(gejala_list),
        'status': status,
        'rekomendasi': rekomendasi,
        'hasil_diagnosa': hasil_diagnosa[:3]  # Hanya kirim 3 teratas ke frontend
    })

@app.route('/api/riwayat-pasien', methods=['GET'])
def get_riwayat_pasien():
    """
    API ENDPOINT: Get All Riwayat Pasien
    Mengembalikan semua data riwayat pasien dalam format JSON
    Digunakan oleh halaman riwayat-pasien untuk mengambil data
    """
    return jsonify({
        'total_pasien': len(RIWAYAT_PASIEN),
        'riwayat': RIWAYAT_PASIEN
    })

@app.route('/api/hapus-riwayat/<int:pasien_id>', methods=['DELETE'])
def hapus_riwayat(pasien_id):
    """
    API ENDPOINT: Hapus Riwayat Pasien by ID
    Menghapus data pasien tertentu berdasarkan ID
    Menggunakan list comprehension untuk filter
    """
    global RIWAYAT_PASIEN
    # Filter: simpan hanya pasien yang ID-nya tidak sama dengan yang dihapus
    RIWAYAT_PASIEN = [p for p in RIWAYAT_PASIEN if p['id'] != pasien_id]
    return jsonify({'status': 'success', 'message': 'Data pasien berhasil dihapus'})

@app.route('/api/hapus-semua-riwayat', methods=['DELETE'])
def hapus_semua_riwayat():
    """
    API ENDPOINT: Hapus Semua Riwayat
    Mengosongkan seluruh data riwayat pasien
    """
    global RIWAYAT_PASIEN
    RIWAYAT_PASIEN = []  # Reset ke list kosong
    return jsonify({'status': 'success', 'message': 'Semua riwayat berhasil dihapus'})

if __name__ == '__main__':
    """
    MAIN EXECUTION - Menjalankan Server Flask
    """
    print("""
=======================================================================
              SISTEM DIAGNOSIS PENYAKIT - FLASK      
=======================================================================
Server berjalan di: http://localhost:5000
    """)
    
    # Tampilkan daftar penyakit yang bisa didiagnosa
    print("Penyakit yang bisa didiagnosa:")
    for penyakit in PENYAKIT_DATABASE.values():
        print(f"- {penyakit['nama']}")
    print()
    
    # Jalankan server Flask
    app.run(host='0.0.0.0', port=5000, debug=True)