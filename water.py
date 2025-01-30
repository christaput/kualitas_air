import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model CatBoost
model = joblib.load("catboost_model.pkl")

# Tambahkan CSS untuk tampilan lebih menarik
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
        max-width: 900px;
        margin: 2rem auto;
        color: white;
    }
    h1 {
        color: #ffffff;
        text-align: center;
    }
    label {
        font-weight: bold;
        color: white;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-size: 16px;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #d43f3f;
    }
    </style>
""", unsafe_allow_html=True)

#judul
st.title('Prediksi Kualitas Air dan kelayakan konsumsi')
st.write('Gunakan web ini untuk memprediksi kualitas air.')

# Tata letak dua kolom
col1, col2 = st.columns(2)

with col1:
    ph = st.number_input('Input nilai pH', min_value=0.0, max_value=14.0, step=0.1)
    hardness = st.number_input('Input nilai Hardness', min_value=0.0, step=1.0)
    solids = st.number_input('Input nilai Solids', min_value=0.0, step=100.0)
    chloramines = st.number_input('Input nilai Chloramines', min_value=0.0, step=0.1)
    sulfate = st.number_input('Input nilai Sulfate', min_value=0.0, step=10.0)

with col2:
    conductivity = st.number_input('Input nilai Conductivity', min_value=0.0, step=10.0)
    organic_carbon = st.number_input('Input nilai Organic Carbon', min_value=0.0, step=0.5)
    trihalomethanes = st.number_input('Input nilai Trihalomethanes', min_value=0.0, step=1.0)
    turbidity = st.number_input('Input nilai Turbidity', min_value=0.0, step=0.1)

# Membuat tombol untuk prediksi
if st.button('Test Prediksi Kualitas Air'):
    try:
       # Konversi input menjadi float
        input_values = [float(ph), float(hardness), float(solids), float(chloramines), float(sulfate), float(conductivity), float(organic_carbon), float(trihalomethanes), float(turbidity)]
        
        # Data fitur untuk prediksi
        feature_names = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate', 'conductivity', 'organic_carbon', 'trihalomethanes', 'turbidity']
        input_data = pd.DataFrame([input_values], columns=feature_names)
        
        # Lakukan prediksi
        water_quality_prediction = model.predict(input_data)
        
        # Tampilkan hasil prediksi
        if int(water_quality_prediction[0] == 1):
            water_quality_diagnosis = 'HATI-HATI!! Air tidak layak dikonsumsi.'
            st.error(water_quality_diagnosis)
        else:
            water_quality_diagnosis = 'SELAMAT!! Air layak dikonsumsi.'
            st.success(water_quality_diagnosis)
    except ValueError:
        st.error("Mohon masukkan angka yang valid pada semua input.")
