import streamlit as st

st.set_page_config(
    page_title="Trang chủ",
    layout="wide"
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""
<div class="header">
<div class="logo">
🌱 <span>Crop Recommendation System</span>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-title">
HỆ THỐNG DỰ ĐOÁN CÂY TRỒNG
</div>
<div class="description">
Ứng dụng Machine Learning giúp lựa chọn loại cây trồng phù hợp
dựa trên đặc điểm đất và điều kiện môi trường.
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown("""
<div class="stat-card">
    <div class="stat-icon">🎯</div>
    <div class="stat-title">Độ chính xác</div>
    <div class="stat-value">99.55%</div>
</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="stat-card">
    <div class="stat-icon">📊</div>
    <div class="stat-title">F1-score</div>
    <div class="stat-value">99.55%</div>
</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="stat-card">
    <div class="stat-icon">📈</div>
    <div class="stat-title">AUC-ROC</div>
    <div class="stat-value">1.000</div>
</div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
<div class="stat-card">
    <div class="stat-icon">🌳</div>
    <div class="stat-title">Mô hình</div>
    <div class="stat-value">Random Forest</div>
</div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown("""
<div class="content-card">
    <h2 style="color:#2E7D32; margin-bottom:15px;">🌱 Giới thiệu hệ thống</h2>
    <p style="font-size:18px; color:#555; line-height:2; text-align:justify;">
    Hệ thống dự đoán cây trồng được xây dựng nhằm hỗ trợ người dùng
    xác định loại cây trồng phù hợp dựa trên các đặc trưng của đất và
    điều kiện môi trường.
    <br><br>
    Ứng dụng sử dụng mô hình Machine Learning Random Forest để phân
    tích dữ liệu đầu vào gồm Nitơ (N), Photpho (P), Kali (K),
    nhiệt độ, độ ẩm, độ pH và lượng mưa.
    <br><br>
    Sau khi phân tích, hệ thống sẽ đưa ra dự đoán về loại cây trồng
    thích hợp cùng với độ tin cậy của mô hình.
    </p>
</div>
    """, unsafe_allow_html=True)

with right:
    # Mở khối div làm khung card
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    
    # Hiển thị ảnh bằng hàm chuẩn của streamlit (lùi ra 1 cấp thư mục để vào assets)
    st.image("../streamlit/assets/dashboard.jpg", use_container_width=True)
    
    # Đóng khối div lại
    st.markdown('</div>', unsafe_allow_html=True)

# Footer chân trang ở cuối cùng
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:10px; font-weight:500;'>
    © 2026 Crop Recommendation System | Developed using Random Forest, FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)