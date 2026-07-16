import streamlit as st
import os

st.set_page_config(
    page_title="Crop Recommendation",
    page_icon="🌱",
    layout="wide"
)

css_path = os.path.join(
    os.path.dirname(__file__),
    "style.css"
)

with open(css_path, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.switch_page("pages/1_Dashboard.py")