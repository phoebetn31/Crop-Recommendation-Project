import streamlit as st
import requests

st.set_page_config(
    page_title="Model Information",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Model Information")

st.markdown("Information about the deployed machine learning model.")

st.divider()

try:

    response = requests.get("http://127.0.0.1:8000/model-info")

    if response.status_code == 200:

        model = response.json()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Model Name", model["model_name"])
            st.metric("Version", model["version"])

        with col2:
            st.metric("Algorithm", model["algorithm"])
            st.metric("Number of Features", len(model["features"]))

        st.subheader("📋 Input Features")

        st.table(model["features"])

        st.subheader("📄 API Response")

        st.json(model)

    else:
        st.error("Cannot load model information.")

except:
    st.error("Cannot connect to FastAPI.")