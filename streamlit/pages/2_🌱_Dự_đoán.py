import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Crop Recommendation",
    page_icon="streamlit/assets/logo.png",
    layout="wide"
)

# Sửa lỗi encoding khi đọc file CSS trên Windows
with open("style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

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
    DỰ ĐOÁN CÂY TRỒNG PHÙ HỢP
</div>
<div class="description">
    Nhập các chỉ số môi trường và đất đai dưới đây để mô hình AI (Random Forest) gợi ý loại cây trồng tối ưu nhất.
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# GIAO DIỆN NHẬP CHỈ SỐ (Chia làm 2 cột chính)
# -------------------------------------------------------------
st.markdown('<div class="content-card" style="margin-bottom: 25px;">', unsafe_allow_html=True)
st.markdown('<h2 style="color:#2E7D32; font-size: 22px; margin-bottom: 20px;">📊 Nhập thông số môi trường</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("##### 🧪 Thành phân dinh dưỡng trong đất")
    n = st.number_input("N (Nitơ) - Hàm lượng đạm trong đất", min_value=0.0, max_value=150.0, value=50.0, step=1.0)
    p = st.number_input("P (Phốt pho) - Hàm lượng lân trong đất", min_value=0.0, max_value=150.0, value=50.0, step=1.0)
    k = st.number_input("K (Kali) - Hàm lượng kali trong đất", min_value=0.0, max_value=255.0, value=50.0, step=1.0)
    ph = st.number_input("pH - Độ chua/kiềm của đất (0-14)", min_value=0.0, max_value=14.0, value=6.5, step=0.1)

with col2:
    st.markdown("##### 🌦️ Điều kiện khí hậu thời tiết")
    temp = st.number_input("Nhiệt độ (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.5)
    hum = st.number_input("Độ ẩm không khí (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
    rain = st.number_input("Lượng mưa trung bình (mm)", min_value=0.0, max_value=300.0, value=100.0, step=5.0)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
predict_btn = st.button("🚀 Bắt đầu phân tích & dự đoán")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# XỬ LÝ DỰ ĐOÁN KHI BẤM NÚT
# -------------------------------------------------------------
if predict_btn:
    # 1. Tạo payload gửi lên FastAPI
    payload = {
        "N": n,
        "P": p,
        "K": k,
        "temperature": temp,
        "humidity": hum,
        "ph": ph,
        "rainfall": rain
    }
    
    with st.spinner("🧠 Hệ thống đang phân tích dữ liệu..."):
        try:
            # 2. Gọi API FastAPI thực hiện dự đoán
            response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                crop_prediction = result.get("prediction", "Unknown").strip()
                
                # Hiển thị kết quả dự đoán
                st.markdown('<div class="content-card" style="border: 2px solid #2E7D32;">', unsafe_allow_html=True)
                
                res_col1, res_col2 = st.columns([1, 1], gap="large")
                
                with res_col1:
                    st.markdown(f"""
                        <h3 style="color: #2E7D32; margin-top: 10px;">🎉 KẾT QUẢ ĐỀ XUẤT</h3>
                        <p style="font-size: 16px;">Dựa trên phân tích mẫu đất và khí hậu, loại cây trồng phù hợp nhất cho mảnh ruộng của bạn là:</p>
                        <div style="background-color: #DCFCE7; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <span style="color: #1B5E20; font-size: 32px; font-weight: 800; text-transform: uppercase;">
                                {crop_prediction}
                            </span>
                        </div>
                        <p style="font-size: 14px; color: #555;">💡 <i>Hệ thống khuyến nghị hãy đảm bảo nguồn nước tưới tiêu và quy trình chăm bón tiêu chuẩn để đạt năng suất tối đa.</i></p>
                    """, unsafe_allow_html=True)
                    
                with res_col2:
                    # -------------------------------------------------------------
                    # TỰ ĐỘNG DÒ ĐƯỜNG DẪN TUYỆT ĐỐI KHÔNG SỢ LỖI THƯ MỤC CHẠY
                    # -------------------------------------------------------------
                    # Lấy vị trí của chính file code hiện tại (thư mục pages/)
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    # Đi ngược lên 1 cấp để vào thư mục streamlit/
                    streamlit_dir = os.path.dirname(current_dir)
                    
                    # Ghép nối đường dẫn tuyệt đối đến ảnh cây trồng
                    crop_filename = f"{crop_prediction.lower()}.png"
                    image_path = os.path.join(streamlit_dir, "assets", "crops", crop_filename)
                    
                    # Ảnh logo mặc định đề phòng bạn chưa tải đủ 22 ảnh
                    default_image = os.path.join(streamlit_dir, "assets", "logo.png")
                    
                    # Kiểm tra xem file ảnh có tồn tại không
                    if os.path.exists(image_path):
                        final_image_path = image_path
                    else:
                        final_image_path = default_image
                    
                    # Hiển thị ảnh cây trồng bo góc tuyệt đẹp
                    st.image(
                        final_image_path, 
                        caption=f"Hình ảnh cây trồng: {crop_prediction.upper()}", 
                        use_container_width=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.balloons()  # Hiệu ứng bóng bay chúc mừng thành công
                
            else:
                st.error(f"❌ Lỗi từ server FastAPI (Mã lỗi: {response.status_code})")
        except Exception as e:
            st.error(f"❌ Lỗi kết nối đến Backend FastAPI: {e}")

# Footer chân trang ở cuối cùng
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:10px; font-weight:500;'>
    © 2026 Crop Recommendation System | Developed using Random Forest, FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)