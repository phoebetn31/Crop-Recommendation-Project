import streamlit as st

st.set_page_config(
    page_title="Crop Recommendation",
    page_icon="🌱",
    layout="wide"
)

with open("style.css",encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.switch_page("pages/1_📊_Dashboard.py")