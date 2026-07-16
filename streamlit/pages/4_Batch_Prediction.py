import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# -------------------------------------------------------------
# ĐỊNH NGHĨA ĐƯỜNG DẪN GỐC (BASE_DIR) TRƯỚC TIÊN
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO = BASE_DIR / "assets" / "logo.png"
CSS_PATH = BASE_DIR / "style.css"

# Cấu hình trang sử dụng đường dẫn tuyệt đối chuẩn xác cho logo icon
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
    DỰ ĐOÁN HÀNG LOẠT
</div>
<div class="description">
    Tải lên file CSV chứa thông tin của nhiều mẫu để hệ thống tự động dự đoán cùng lúc.
</div>
""", unsafe_allow_html=True)

# Gom cụm khu vực Upload vào một content-card để tạo hiệu ứng Canvas bo góc đẹp mắt
st.markdown('<div class="content-card" style="margin-bottom: 25px;">', unsafe_allow_html=True)
st.markdown('<h2 style="color:#2E7D32; font-size: 22px; margin-bottom: 15px;">📂 Tải lên dữ liệu</h2>', unsafe_allow_html=True)

# Bộ chọn file CSV
uploaded_file = st.file_uploader(
    "Chọn file CSV từ máy tính của bạn",
    type=["csv"]
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    # Đọc và hiển thị xem trước file vừa upload
    df = pd.read_csv(uploaded_file)
    
    st.markdown('<div class="content-card" style="margin-bottom: 25px;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#2E7D32; font-size: 22px; margin-bottom: 15px;">📊 Xem trước dữ liệu đầu vào</h2>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    # Nút thực hiện dự đoán hàng loạt
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    predict_btn = st.button("🌱 Bắt đầu dự đoán hàng loạt")
    st.markdown('</div>', unsafe_allow_html=True)

    # Khi người dùng nhấn nút bắt đầu chạy mô hình
    if predict_btn:
        result = df.copy()
        predictions = []
        
        # Tạo thanh tiến trình chạy (Progress Bar) để người dùng theo dõi khi quét vòng lặp
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_rows = len(df)
        
        # Vòng lặp gọi API FastAPI cho từng dòng dữ liệu
        try:
            for index, row in df.iterrows():
                # Cập nhật trạng thái xử lý trên giao diện
                status_text.text(f"⏳ Đang xử lý mẫu số {index + 1}/{total_rows}...")
                progress_bar.progress(int((index + 1) / total_rows * 100))
                
                response = requests.post(
                    "http://api:8000/predict",
                    json={
                        "N": float(row["N"]),
                        "P": float(row["P"]),
                        "K": float(row["K"]),
                        "temperature": float(row["temperature"]),
                        "humidity": float(row["humidity"]),
                        "ph": float(row["ph"]),
                        "rainfall": float(row["rainfall"])
                    },
                    timeout=10  # Tăng timeout lên 10s đề phòng mạng nội bộ Docker bị nghẽn
                )
                
                if response.status_code == 200:
                    predictions.append(response.json()["prediction"])
                else:
                    predictions.append("Lỗi API")
            
            # Lưu mảng kết quả vào cột mới trong dataframe
            result["Prediction"] = predictions
            status_text.success("🎉 Đã hoàn thành dự đoán toàn bộ dữ liệu!")
            
            # Hiển thị bảng kết quả sau cùng
            st.markdown('<div class="content-card" style="margin-top: 25px; margin-bottom: 25px;">', unsafe_allow_html=True)
            st.markdown('<h2 style="color:#2E7D32; font-size: 22px; margin-bottom: 15px;">✅ Kết quả dự đoán chi tiết</h2>', unsafe_allow_html=True)
            st.dataframe(result, use_container_width=True)
            
            # Chuẩn bị dữ liệu và xuất nút Download CSV
            csv_data = result.to_csv(index=False).encode("utf-8")
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.download_button(
                label="⬇️ Tải kết quả xuống (.CSV)",
                data=csv_data,
                file_name="crop_predictions.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Đã xảy ra lỗi trong quá trình kết nối API: {e}")

# Footer chân trang ở cuối cùng
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:10px; font-weight:500;'>
    © 2026 Crop Recommendation System | Developed using Random Forest, FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)