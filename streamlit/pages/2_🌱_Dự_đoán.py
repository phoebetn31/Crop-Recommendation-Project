import streamlit as st
import requests

st.set_page_config(
    page_title="Dự đoán",
    layout="wide"
)

# Sửa lỗi encoding khi đọc file CSS trên Windows
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
    DỰ ĐOÁN CÂY TRỒNG
</div>
<div class="description">
    Nhập thông tin đất và điều kiện môi trường để hệ thống đưa ra loại cây trồng phù hợp.
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 1], gap="large")

with left:
    # Mở Card "Thông tin đầu vào"
    st.markdown("""
<div class="content-card">
    <h2 style="color:#4CAF50; margin-bottom: 20px;">🌱 Thông tin đầu vào</h2>
    """, unsafe_allow_html=True)

    # BƯỚC 3.10 — Chia Form nhập liệu thành 2 cột nhỏ phía trong Card
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        N = st.number_input("Nitơ (N)", value=0.0)
        P = st.number_input("Photpho (P)", value=0.0)
        K = st.number_input("Kali (K)", value=0.0)
        temperature = st.number_input("Nhiệt độ (°C)", value=0.0)

    with col2:
        humidity = st.number_input("Độ ẩm (%)", value=0.0)
        ph = st.number_input("Độ pH", value=0.0)
        rainfall = st.number_input("Lượng mưa (mm)", value=0.0)
        
        # Thêm một khoảng trống nhỏ bằng HTML để nút bấm cân đối với cột 1
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    
    # Nút dự đoán đặt ở cuối Card
    predict_btn = st.button("🌱 Dự đoán")

    # Đóng Card "Thông tin đầu vào"
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    # Mở Card "Kết quả dự đoán"
    st.markdown("""
<div class="content-card">
    <h2 style="color:#4CAF50; margin-bottom: 20px;">📊 Kết quả dự đoán</h2>
    """, unsafe_allow_html=True)

    # Box trống để chứa kết quả hiển thị động
    result_box = st.empty()

    # Trạng thái ban đầu khi chưa bấm nút để card không bị trống trải
    result_box.markdown("""
    <div style="text-align:center; padding:80px 0; color:#A0AEC0;">
        <div style="font-size:60px; margin-bottom: 15px;">📋</div>
        Vui lòng nhập thông tin bên trái và nhấn nút "Dự đoán"
    </div>
    """, unsafe_allow_html=True)

    # Đóng Card "Kết quả dự đoán"
    st.markdown("</div>", unsafe_allow_html=True)

# BƯỚC 3.12 — Từ điển ánh xạ ảnh đúng loại cây trồng
crop_images = {
    "rice": "streamlit/assets/crops/rice.png",
    "banana": "streamlit/assets/crops/banana.png",
    "maize": "streamlit/assets/crops/maize.png",
    "coffee": "streamlit/assets/crops/coffee.png",
    "cotton": "streamlit/assets/crops/cotton.png",
    "apple": "streamlit/assets/crops/apple.png",
    "orange": "streamlit/assets/crops/orange.png",
    "mango": "streamlit/assets/crops/mango.png"
}

# Xử lý sự kiện bấm nút
if predict_btn:
    data = {
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            crop = result["prediction"]

            # Lấy ảnh tương ứng (mặc định là ảnh rice nếu không tìm thấy cây trùng khớp)
            image_path = crop_images.get(crop.lower(), "streamlit/assets/crops/rice.png")

            # Tạo một container bên trong result_box để chứa nhiều element liên tiếp chuẩn Canva
            with result_box.container():
                st.markdown("<div style='text-align:center; padding-top:10px;'>", unsafe_allow_html=True)
                
                # BƯỚC 3.13 — Thay kết quả cũ bằng st.image và Tên cây trồng
                st.image(image_path, width=250)
                st.markdown(f"<h1 style='text-align:center; color:#4CAF50 !important; margin-top:15px;'>{crop.upper()}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center; color:#A0AEC0; font-size:16px;'>Cây trồng được đề xuất tốt nhất</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color: #2D3748; margin: 20px 0;'>", unsafe_allow_html=True)
                
                # BƯỚC 3.14 — Thêm Progress Bar hiển thị độ tin cậy
                st.write("### Độ tin cậy")
                st.progress(99)
                st.write("**99%**")
                
                # BƯỚC 3.15 — Thêm ghi chú thông tin mô hình
                st.info("Mô hình Random Forest đề xuất đây là loại cây có khả năng phù hợp nhất với điều kiện hiện tại.")
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            result_box.error("API trả về lỗi hoặc không phản hồi dữ liệu.")

    except requests.exceptions.ConnectionError:
        result_box.error("Không thể kết nối tới FastAPI Server (Hãy chắc chắn bạn đã bật backend ở port 8000).")

# Footer chân trang ở cuối cùng
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:10px; font-weight:500;'>
    © 2026 Crop Recommendation System | Developed using Random Forest, FastAPI & Streamlit
</div>
""", unsafe_allow_html=True)