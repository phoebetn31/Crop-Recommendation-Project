import streamlit as st
import requests

st.set_page_config(
    page_title="Crop Prediction",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Crop Prediction")

st.markdown("Enter soil and environmental information below.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    N = st.number_input("Nitrogen (N)", min_value=0.0, value=90.0)
    P = st.number_input("Phosphorus (P)", min_value=0.0, value=42.0)
    K = st.number_input("Potassium (K)", min_value=0.0, value=43.0)
    temperature = st.number_input("Temperature (°C)", value=20.8)

with col2:
    humidity = st.number_input("Humidity (%)", value=82.0)
    ph = st.number_input("pH", value=6.5)
    rainfall = st.number_input("Rainfall (mm)", value=202.0)

st.divider()

if st.button("🌾 Predict Crop", use_container_width=True):

    payload = {
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }

    try:

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction completed successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🌱 Predicted Crop",
                    result["prediction"]
                )

            with col2:
                st.metric(
                    "🎯 Confidence",
                    f"{result['confidence']*100:.2f}%"
                )

        else:
            st.error("Prediction failed.")

    except Exception:
        st.error("Cannot connect to FastAPI server.")