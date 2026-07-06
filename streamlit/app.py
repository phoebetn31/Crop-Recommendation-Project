import streamlit as st
import requests

st.set_page_config(
    page_title="Crop Recommendation",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 Crop Recommendation System - Trợ lý dự đoán cây trồng")

st.markdown(
    "Dự đoán cây trồng phù hợp nhất dựa trên điều kiện đất và khí hậu"
)

col1, col2 = st.columns(2)

#cột trái
with col1:

    N = st.number_input(
        "Nitrogen (N) - Nitơ",
        min_value=0.0
    )

    K = st.number_input(
        "Potassium (K) - Kali",
        min_value=0.0
    )

    humidity = st.number_input(
        "Humidity - Độ ẩm không khí",
        min_value=0.0
    )

    rainfall = st.number_input(
        "Rainfall - Lượng mưa",
        min_value=0.0
    )

#cột phải
with col2:

    P = st.number_input(
        "Phosphorus (P) - Photpho",
        min_value=0.0
    )

    temperature = st.number_input(
        "Temperature - Nhiệt độ",
        min_value=-20.0
    )

    ph = st.number_input(
        "pH - Nồng độ pH",
        min_value=0.0,
        max_value=14.0
    )

ph = st.number_input(
    "pH",
    min_value=0.0,
    max_value=14.0,
    value=6.5,
    step=0.1,
    help="Soil pH value (0–14)"
)

if st.button("🚀 Dự đoán"):

    data = {
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        st.success(
            f"🌾 Cây trồng đề xuất: {result['prediction']}"
        )
    else:
        st.error("Dự đoán thất bại!")