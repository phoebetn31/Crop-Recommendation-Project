import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Prediction History")

st.markdown("View the prediction history stored in the SQLite database.")

st.divider()

# Nút làm mới
if st.button("🔄 Refresh"):
    st.rerun()

try:
    response = requests.get(
        "http://127.0.0.1:8000/history?limit=100"
    )

    if response.status_code == 200:

        history = response.json()

        if len(history) == 0:
            st.info("No prediction history found.")

        else:

            df = pd.DataFrame(history)

            st.metric(
                "Total Predictions",
                len(df)
            )

            st.divider()

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.error("Cannot load prediction history.")

except:
    st.error("Cannot connect to FastAPI.")