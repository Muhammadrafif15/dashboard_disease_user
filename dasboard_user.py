import numpy as np
import streamlit as st
import joblib

class PregnancyDiseasePredictor:
    def __init__(self, model):
        self.model = model
        self.symptoms = {
            'G1': 'Usia hamil 7 bulan / lebih',
            'G2': 'Mual',
            'G3': 'Muntah',
            'G4': 'Kejang',
            'G5': 'Proteinuria lebih dari 3g/liter',
            'G6': 'Tekanan darah >=160/110 mmHg',
            'G7': 'Pusing',
            'G8': 'Nyeri ulu hati',
            'G9': 'Nyeri perut bagian bawah',
            'G10': 'Nyeri perut pada satu sisi kanan/kiri',
            'G11': 'Nyeri hebat tiba - tiba',
            'G12': 'Perdarahan dari jalan lahir',
            'G13': 'Perdarahan dari jalan lahir warna kehitaman',
            'G14': 'Kematian janin',
            'G15': 'Syok',
            'G16': 'Pemeriksaan dinding rahim',
            'G17': 'Tampak pucat',
            'G18': 'Air kencing berwarna kemerahan',
            'G19': 'Tekanan darah turun sampai dibawah 90/60 mmHg',  
            'G20': 'Nadi cepat',
            'G21': 'Kontraksi dari rahim',
            'G22': 'Jumlah perdarahan sedikit',
            'G23': 'Produksi urin sedikit',
            'G24': 'Kontraksi Rahim yang hilang',
            'G25': 'Kesadaran menurun'
        }

        self.symptom_details = {
            'G1': 'Kehamilan sudah memasuki usia 7 bulan atau lebih, mendekati masa persalinan',
            'G2': 'Perasaan ingin muntah yang sering terjadi, terutama pada trimester pertama',
            'G3': 'Mengeluarkan isi perut melalui mulut, dapat terjadi akibat berbagai kondisi',
            'G4': 'Gerakan otot yang tidak terkontrol, bisa menandakan kondisi serius',
            'G5': 'Adanya protein berlebih dalam urin, bisa menjadi tanda preeklampsia',
            'G6': 'Tekanan darah tinggi yang berbahaya, membutuhkan perhatian medis segera',
            'G7': 'Rasa berputar atau tidak seimbang di kepala',
            'G8': 'Rasa sakit atau tidak nyaman di area ulu hati',
            'G9': 'Nyeri atau rasa sakit di bagian bawah perut',
            'G10': 'Nyeri yang terlokalisir di satu sisi perut kanan atau kiri',
            'G11': 'Rasa sakit yang tiba-tiba dan sangat intens',
            'G12': 'Keluarnya darah dari jalan lahir di luar masa haid atau persalinan',
            'G13': 'Perdarahan dengan warna gelap atau kehitaman, bisa menandakan masalah serius',
            'G14': 'Tidak adanya tanda-tanda kehidupan pada janin',
            'G15': 'Kondisi kritis akibat penurunan aliran darah ke organ vital',
            'G16': 'Pemeriksaan fisik pada dinding rahim oleh tenaga medis',
            'G17': 'Wajah terlihat pucat, bisa menandakan anemia atau kondisi lain',
            'G18': 'Urin berwarna kemerahan, bisa menandakan adanya darah',
            'G19': 'Tekanan darah turun drastis, berbahaya bagi ibu hamil',
            'G20': 'Detak jantung yang lebih cepat dari normal',
            'G21': 'Gerakan berkontraksi pada otot rahim',
            'G22': 'Jumlah perdarahan yang relatif sedikit',
            'G23': 'Produksi urin yang menurun',
            'G24': 'Hilangnya kontraksi rahim yang normal',
            'G25': 'Penurunan tingkat kesadaran atau responsivitas'
        }
    
        self.disease_mapping = {
            0: 'P001 Abortus (keluarnya janin sebelum masa visibilitas)',
            1: 'P002 Hamil ekstrauteri ektopik terganggu (hamil yang berkembang diluar rahim)',
            2: 'P003 Solusio plasenta (lepasnya plasenta dari dinding rahim)',
            3: 'P004 Preekslampsia berat (suatu komplikasi ditandai dengan hipertensi)',
            4: 'P005 Rupture uteri (robeknya dinding rahim)'
        }

    def predict_disease(self, symptoms_input):
        # mengecek apakah ini dictionary
        if isinstance(symptoms_input, dict):
            input_array = [symptoms_input.get(sym, 0) for sym in self.symptoms]
        # jika tidak mengecek apakah ini berupa list
        elif isinstance(symptoms_input, list):
            if len(symptoms_input) != len(self.symptoms):
                raise ValueError(f"Input must have {len(self.symptoms)} symptoms")
            input_array = symptoms_input
        # jika buka keduanya maka inputan error
        else :
            raise TypeError("Imput  msut be a list or dictionary of symptoms")
        # mengubah bentuk array menjadi matrik tunggal
        # 1 berarti 1 baris, -1 meratakan semua isi array agar menjadi satu barisq

        input_array = np.array(input_array).reshape(1, -1)

        # menyimpan model hasil prediksi yang dihasilkan dari inputanm gejala
        # [0] untuk mengambil pada probabilitas penyakit pertama
        prediction = self.model.predict(input_array)[0]

        return self.disease_mapping.get(prediction, "Tidak dapat melakukan prediksi")
    
def main():
    # load model machine learning
    try :
        model = joblib.load('modelterbaru.pkl')
    except FileExistsError:
        st.error("Model tidak ditemukan pastikan nama file benar !!")
        return
    
    #insialisasi fungsi
    predictor = PregnancyDiseasePredictor(model)

    #UI
    #Deskription program
    st.title('Pregnancy Disease Predictor')
    st.write('Masukkan gejala untuk memprediksi kemungkinan penyakit pada kehamilan')

    #insialisai itempat menyimpan inputan
    symptoms_input = {}

    #layout untuk tampilan input gejala dari user
    cols = st.columns(2)

    for i, (symptom_code, symptom_name) in enumerate(predictor.symptoms.items()):
        col = cols[i % 2]
        with col:
            symptoms_input[symptom_code] = st.checkbox(f' {symptom_code} : {symptom_name}', key=symptom_code)

            # detail gejala yang dialami 
            st.caption(predictor.symptom_details[symptom_code])

    # mengubah inputan, jika ada input maka bernilai 1, jika tidak ada maka 0
    # menyerderhanakan struktur data menjadi list, pada key di dictionary
    symptoms_array = [1 if symptoms_input[sym] else 0 for sym in predictor.symptoms.keys()]

    # tomabol untuk menentukan penyakit
    if st.button('Prediksi Penyakit'):
        try:
            prediction = predictor.predict_disease(symptoms_array)

            # Meanmpilkan hasil
            st.markdown('### Hasil Prediksi')
            st.markdown(f"**{prediction}**", unsafe_allow_html=True)

            # menambahkanm keterangan bahwa ini hanya prediksi program komputer
            st.info("Catatan: Ini adalah prediksi awal dari komputer. Selalu konsultasikan dengan tenaga medis profesional.")

        except Exception as e:
            st.error(f"Terjadi kesalahan prediksi: {str(e)}")

    # Informational sidebar
    st.sidebar.title('Tentang Aplikasi')
    st.sidebar.info('''
    ## Petunjuk Penggunaan
    1. Centang kotak untuk gejala yang dialami
    2. Tekan tombol "Prediksi Penyakit"
    3. Lihat hasil prediksi penyakit
    
    ### Disclaimer
    Aplikasi ini hanya untuk tujuan informasi dan tidak menggantikan 
    KONSULTASI MEDIS PROFESIONAL.
    ''')

# menginisialisasi dan menjalankan program 

if __name__ == '__main__':
    main()
