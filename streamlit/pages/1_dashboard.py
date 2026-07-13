import streamlit as st

st.set_page_config(
    page_title="Crop Recommendation System",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Crop Recommendation System")
st.markdown("### Machine Learning Application for Crop Prediction")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Accuracy",
        value="99.55%"
    )

with col2:
    st.metric(
        label="F1-score",
        value="99.55%"
    )

with col3:
    st.metric(
        label="AUC-ROC",
        value="1.0000"
    )

with col4:
    st.metric(
        label="Model",
        value="Random Forest"
    )

st.divider()

left, right = st.columns([2,1])

with left:
    st.subheader("📖 Project Overview")

    st.write("""
This application predicts the most suitable crop based on soil nutrients
and environmental conditions using a Random Forest machine learning model.

### Input Features
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH
- Rainfall

### Output
- Predicted Crop
- Prediction Confidence
""")

with right:
    st.info("""
### Model Information

- Algorithm: Random Forest
- Number of Features: 7
- Number of Crop Classes: 22
- Deployment: FastAPI + Streamlit
- Database: SQLite
""")

st.success("✅ System is ready for prediction.")