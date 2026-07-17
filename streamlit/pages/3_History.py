import streamlit as st
import pandas as pd
import requests
import os
from pathlib import Path

# -------------------------------------------------------------
# CẤU HÌNH BIẾN MÔI TRƯỜNG API (Local vs Docker)
# -------------------------------------------------------------
# Tự động lấy URL từ biến môi trường (Docker), nếu không có mặc định dùng localhost (Local)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# -------------------------------------------------------------
# ĐỊNH NGHĨA ĐƯỜNG DẪN GỐC (BASE_DIR) TRƯỚC TIÊN
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO = BASE_DIR / "assets" / "logo.png"
CSS_PATH = BASE_DIR / "style.css"

# Cấu hình trang sử dụng đường dẫn logo chuẩn xác tuyệt đối
st.set_page_config(
    page_title="Crop Recommendation",
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
    LỊCH SỬ DỰ ĐOÁN
</div>
<div class="description">
    Danh sách các lần dự đoán đã được thực hiện trong hệ thống.
</div>
""", unsafe_allow_html=True)

# Khởi tạo một biến trạng thái tạm thời để lưu dữ liệu hiển thị tức thời
if "history_df" not in st.session_state:
    st.session_state.history_df = None

# -------------------------------------------------------------
# LẤY DỮ LIỆU LỊCH SỬ TỪ BACKEND
# -------------------------------------------------------------
def fetch_data():
    try:
        # Gọi API lấy lịch sử thông qua biến môi trường API_URL linh hoạt
        response = requests.get(f"{API_URL}/history", timeout=5)
        if response.status_code == 200:
            history = response.json()
            return pd.DataFrame(history)
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối FastAPI khi lấy dữ liệu: {e}")
    return pd.DataFrame()

# Nếu chưa có dữ liệu trong session hoặc người dùng chưa thao tác xoá, tải dữ liệu mới
if st.session_state.history_df is None:
    st.session_state.history_df = fetch_data()

# -------------------------------------------------------------
# BỘ LỌC VÀ CÁC NÚT ĐIỀU KHIỂN
# -------------------------------------------------------------
st.markdown('<div class="content-card" style="padding: 20px; margin-bottom: 25px;">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1], gap="medium")

with col1:
    keyword = st.text_input("🔍 Tìm kiếm theo tên cây trồng", placeholder="Nhập tên cây cần tìm... ví dụ: rice, banana...")

with col2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    refresh = st.button("🔄 Làm mới", use_container_width=True)
    if refresh:
        st.session_state.history_df = fetch_data()
        st.rerun()

with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    clear_btn = st.button("🗑️ Xóa lịch sử", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# XỬ LÝ CLICK NÚT XOÁ LỊCH SỬ (Direct Handler)
# -------------------------------------------------------------
if clear_btn:
    try:
        # Gửi request DELETE tới backend bằng biến môi trường API_URL linh hoạt
        delete_response = requests.delete(f"{API_URL}/history", timeout=5)
        
        # Nếu Backend xoá thành công hoặc phản hồi tốt
        if delete_response.status_code == 200:
            # Ép bảng dữ liệu hiện tại về rỗng ngay lập tức trên UI
            st.session_state.history_df = pd.DataFrame()
            st.toast("🗑️ Đã xoá sạch lịch sử thành công!", icon="✅")
            st.rerun()
        else:
            st.error(f"❌ Server không thực hiện xoá (Mã lỗi: {delete_response.status_code})")
    except Exception as e:
        st.error(f"❌ Không thể kết nối tới server để xoá: {e}")

# Lấy dữ liệu tạm từ session_state để xử lý hiển thị
df_display = st.session_state.history_df.copy() if st.session_state.history_df is not None else pd.DataFrame()

# Xử lý bộ lọc tìm kiếm theo từ khóa người dùng nhập
if not df_display.empty and keyword:
    if "prediction" in df_display.columns:
        df_display = df_display[df_display["prediction"].str.contains(keyword, case=False, na=False)]

# -------------------------------------------------------------
# HIỂN THỊ BẢNG KẾT QUẢ
# -------------------------------------------------------------
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown('<h2 style="color:#2E7D32; font-size: 22px; margin-bottom: 20px;">📋 Bảng dữ liệu chi tiết</h2>', unsafe_allow_html=True)

if df_display.empty:
    st.info("Chưa có dữ liệu lịch sử dự đoán hoặc không tìm thấy kết quả phù hợp nào.")
else:
    # Đánh số thứ tự STT từ 1 thay vì index mặc định bắt đầu từ 0
    df_display.index = range(1, len(df_display) + 1)
    df_display.index.name = "STT"
    
    st.dataframe(df_display, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer chân trang ở cuối cùng
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:10px; font-weight:500;'>
    © 2026 Crop Recommendation System | Developed using Random Forest, FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)