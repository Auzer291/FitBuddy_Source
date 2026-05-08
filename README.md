# 🏋️ FitBuddy

**FitBuddy** là ứng dụng hỗ trợ tập luyện được hỗ trợ bởi AI, sử dụng webcam và nhận diện tư thế để đếm số lần lặp, đánh giá tư thế và theo dõi quá trình tập luyện trong thời gian thực.

---

## ✨ Tính Năng

- 📷 **Nhận diện tư thế thời gian thực** - sử dụng MediaPipe
- 🔢 **Đếm số lần tự động** - cho các bài tập được hỗ trợ
- ✅ **Phản hồi tư thế** - cảnh báo bằng giọng nói và hiển thị trên màn hình khi tư thế sai
- 💾 **Phiên tập tùy chỉnh** - tự thiết kế và lưu các buổi tập riêng
- 📋 **Lập kế hoạch tập luyện** - tạo lịch tập dưới dạng văn bản dựa trên lịch rảnh và vùng cơ muốn tập
- 🌐 **Giao diện song ngữ** - hỗ trợ Tiếng Việt và English
- 🎨 **Chuyển đổi giao diện** - Sáng / Tối

### Bài Tập Được Hỗ Trợ
| Bài Tập | Vùng Cơ |
|---|---|
| Squat (Ngồi Xuống) | Chân, Mông |
| Bicep Curl (Curl Tay) | Cơ Tay Trước |
| Push Up (Hít Đất) | Ngực, Tay Sau, Vai |

---

## 🛠️ Cài Đặt

### Yêu Cầu
- **Python 3.10.11** Tải tại [python.org](https://www.python.org/downloads/release/python-31011/)
  > ⚠️ Khi cài đặt, nhớ tích vào ô **"Add Python to PATH"**

### Các Bước

**1. Clone repo**
```bash
git clone [https://github.com/Auzer291/fitbuddy.git](https://github.com/Auzer291/FitBuddy_Source.git)
cd fitbuddy
```

**2. Tạo môi trường ảo** *(khuyến nghị)*
```bash
python -m venv .venv
```

**3. Kích hoạt môi trường ảo**

| Hệ Điều Hành | Lệnh |
|---|---|
| Windows (CMD) | `.venv\Scripts\activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

> 💡 Nếu gặp lỗi quyền hạn trên PowerShell, chạy: `Set-ExecutionPolicy Unrestricted -Scope Process`

**4. Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

### Thư Viện Sử Dụng
| Thư Viện | Phiên Bản |
|---|---|
| `opencv-python` | 4.13.0.90 |
| `mediapipe` | 0.10.9 |
| `numpy` | 2.2.6 |
| `pyttsx3` | 2.99 |
| `PyQt6` | 6.10.2 |

---

## 🚀 Chạy Ứng Dụng

```bash
python main.py
```

Hoặc mở file `main.py` trong IDE và nhấn nút Run.

---

## 🖥️ Hướng Dẫn Sử Dụng

### Menu Chính
| Nút | Chức Năng |
|---|---|
| 🏋️ Bắt Đầu Tập Luyện | Chọn phiên tập đã lưu và bắt đầu |
| 💾 Tạo Phiên Tập | Tự thiết kế buổi tập (ví dụ: Squat × 3 hiệp × 10 lần) |
| 📋 Lập Kế Hoạch | Tạo lịch tập dựa trên thời gian và vùng cơ mục tiêu |
| ⚙️ Cài Đặt | Đổi ngôn ngữ (Tiếng Việt / English) và chuyển giao diện Sáng/Tối |

### Trong Khi Tập Luyện
1. Đứng cách camera **2–3 mét** ở nơi có đủ ánh sáng để AI nhìn thấy toàn bộ cơ thể.
2. Nhấn **"Bật Camera"** để kích hoạt nhận diện tư thế.
3. Khi thực hiện bài tập, số lần sẽ được đếm tự động khi tư thế đúng.
4. Nếu tư thế sai, ứng dụng sẽ **cảnh báo bằng giọng nói** và hiển thị **thông báo màu đỏ** trên màn hình.
5. Hoàn thành số lần mục tiêu để kết thúc hiệp và chuyển sang bài tiếp theo.

---

## ⚠️ Lưu Ý Quan Trọng

- **Camera cần thời gian để khởi động** tùy vào cấu hình thiết bị, có thể mất vài giây sau khi nhấn "Bật Camera" trước khi AI sẵn sàng nhận diện.
- **Nếu cửa sổ bị đứng hoặc hiện "Not Responding"** đây là bình thường khi khởi động lần đầu. Hãy **chờ thêm 1–2 phút** trước khi đóng ứng dụng. Ứng dụng đang tải mô hình AI ở nền.
- **Ánh sáng và góc camera ảnh hưởng đến kết quả** tránh ngược sáng và đảm bảo toàn bộ cơ thể nằm trong khung hình.

---

## 📁 Cấu Trúc Dự Án

```
fitbuddy/
├── main.py               # Điểm khởi chạy
├── gui.py                # Toàn bộ màn hình giao diện (PyQt6)
├── camera.py             # Bắt hình từ webcam
├── pose_estimation.py    # Wrapper MediaPipe nhận diện tư thế
├── exercise_rules.py     # Ngưỡng góc theo từng bài tập
├── rep_counter.py        # Máy đếm số lần (state machine)
├── posture_check.py      # Đánh giá tư thế
├── feedback.py           # Phản hồi giọng nói & hiển thị
├── scoring.py            # Chấm điểm chất lượng từng rep
├── angle_calculation.py  # Tính góc khớp
├── planner.py            # Tạo kế hoạch tập luyện
├── session_manager.py    # Lưu/tải phiên tập tùy chỉnh
├── localization.py       # Chuỗi ngôn ngữ VI / EN
├── sessions.json         # Dữ liệu phiên tập đã lưu
└── requirements.txt
```

---

## 📄 Giấy Phép

Dự án này được phát triển cho mục đích học tập. Bạn có thể fork và phát triển thêm!
