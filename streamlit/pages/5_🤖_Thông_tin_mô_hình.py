import streamlit as st

st.set_page_config(
    page_title="Thông tin mô hình",
    layout="wide"
)

# Sửa lỗi giải mã mã hóa ký tự trên Windows
with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# BƯỚC 4.2 — Header
st.markdown("""
<div class="header">
    <div class="logo">
        🌱 <span>Crop Recommendation System</span>
    </div>
</div>
""", unsafe_allow_html=True)

# BƯỚC 4.3 — Tiêu đề
st.markdown("""
<div class="big-title">
    THÔNG TIN MÔ HÌNH
</div>
<div class="description">
    Thông tin về mô hình Machine Learning được sử dụng để dự đoán loại cây trồng phù hợp.
</div>
""", unsafe_allow_html=True)

# BƯỚC 4.4 — 4 Card thông tin số liệu phía trên
# BƯỚC 4.4 — Thay đổi một chút class để nhận diện vòng tròn màu
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown('<div class="col-1"><div class="stat-card"><div class="stat-icon">🤖</div><div class="stat-title">Tên mô hình</div><div class="stat-value">Crop ML</div></div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="col-2"><div class="stat-card"><div class="stat-icon">🏷️</div><div class="stat-title">Phiên bản</div><div class="stat-value">v1.0</div></div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="col-3"><div class="stat-card"><div class="stat-icon">🌳</div><div class="stat-title">Thuật toán</div><div class="stat-value">RF</div></div></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="col-4"><div class="stat-card"><div class="stat-icon">📊</div><div class="stat-title">Đặc trưng</div><div class="stat-value">7</div></div></div>', unsafe_allow_html=True)

# BƯỚC 4.5 — Tạo khoảng trống và chia 2 khung bên dưới
st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")

# BƯỚC 4.6 — Khung bên trái (Đặc trưng đầu vào)
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

# BƯỚC 4.7 — Khung bên phải (Thông tin API & Metrics)
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