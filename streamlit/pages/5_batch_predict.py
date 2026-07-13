import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Batch Prediction",
    page_icon="📁",
    layout="wide"
)

st.title("📁 Batch Prediction")

st.markdown(
    "Upload a CSV file to predict crops for multiple samples."
)

st.divider()

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview")

    st.dataframe(df, use_container_width=True)

    if st.button("🌾 Predict All"):

        files = {
            "file": uploaded_file.getvalue()
        }

        response = requests.post(
            "http://127.0.0.1:8000/batch-predict",
            files=files
        )

        if response.status_code == 200:

            result = pd.DataFrame(response.json())

            st.success("Prediction completed!")

            st.subheader("📊 Result")

            st.dataframe(
                result,
                use_container_width=True
            )

            csv = result.to_csv(index=False)

            st.download_button(
                label="⬇ Download Result CSV",
                data=csv,
                file_name="prediction_result.csv",
                mime="text/csv"
            )

        else:

            st.error("Prediction failed.")