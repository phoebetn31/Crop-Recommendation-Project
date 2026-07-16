import streamlit as st
from pathlib import Path

# -------------------------------------------------------------
# ĐỊNH NGHĨA ĐƯỜNG DẪN GỐC (BASE_DIR) TRƯỚC TIÊN
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO = BASE_DIR / "assets" / "logo.png"
CSS_PATH = BASE_DIR / "style.css"

# Cấu hình trang sử dụng đường dẫn logo chuẩn xác tuyệt đối để đồng bộ icon
st.set_page_config(
    page_title="Thông tin mô hình",
    page_icon=str(LOGO) if LOGO.exists() else None,
    layout="wide"
)

# Đọc file CSS
if CSS_PATH.exists():
    with open(CSS_PATH, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header hệ thống
st.markdown("""
<div class="header">
    <div class="logo">
        🌱 <span>Crop Recommendation System</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tiêu đề trang
st.markdown("""
<div class="big-title">
    THÔNG TIN MÔ HÌNH
</div>
<div class="description">
    Thông tin về mô hình Machine Learning được sử dụng để dự đoán loại cây trồng phù hợp.
</div>
""", unsafe_allow_html=True)

# 4 Card thông tin số liệu phía trên
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown('<div class="col-1"><div class="stat-card"><div class="stat-icon">🤖</div><div class="stat-title">Tên mô hình</div><div class="stat-value">Crop ML</div></div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="col-2"><div class="stat-card"><div class="stat-icon">🏷️</div><div class="stat-title">Phiên bản</div><div class="stat-value">v1.0</div></div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="col-3"><div class="stat-card"><div class="stat-icon">🌳</div><div class="stat-title">Thuật toán</div><div class="stat-value">RF</div></div></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="col-4"><div class="stat-card"><div class="stat-icon">📊</div><div class="stat-title">Đặc trưng</div><div class="stat-value">7</div></div></div>', unsafe_allow_html=True)

# Tạo khoảng trống và chia 2 khung bên dưới
st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")

# Khung bên trái (Đặc trưng đầu vào)
with left:
    st.markdown("""
<div class="content-card">
    <h2 style="color:#4CAF50; margin-bottom: 15px;">📋 Đặc trưng đầu vào</h2>
    <ul style="font-size:18px; line-height:2; color: #E2E8F0; padding-left: 20px;">
        <li>Nitơ (N)</li>
        <li>Photpho (P)</li>
        <li>Kali (K)</li>
        <li>Nhiệt độ</li>
        <li>Độ ẩm</li>
        <li>Độ pH</li>
        <li>Lượng mưa</li>
    </ul>
</div>
    """, unsafe_allow_html=True)

# Khung bên phải (Thông tin API & Metrics)
with right:
    st.markdown("""
<div class="content-card">
    <h2 style="color:#4CAF50; margin-bottom: 15px;">🔗 REST API</h2>
    <pre style="font-size:16px; background-color: #2D3748; padding: 12px; border-radius: 8px; color: #F7FAFC; border: 1px solid #4A5568;">
POST  /predict
GET   /health
GET   /model-info
GET   /history</pre>
    <hr style="border-color: #2D3748; margin: 20px 0;">
    <p style="color: #E2E8F0; line-height: 1.8; font-size: 16px;">
        <strong>Mô hình:</strong> Random Forest<br>
        <strong>Accuracy:</strong> 99.55%<br>
        <strong>F1-score:</strong> 99.55%<br>
        <strong>AUC:</strong> 1.000
    </p>
</div>
    """, unsafe_allow_html=True)

# Footer chân trang ở cuối cùng
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:10px; font-weight:500;'>
    © 2026 Crop Recommendation System | Developed using Random Forest, FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)