HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG FitBuddy
==================================================

1. YÊU CẦU HỆ THỐNG & CÀI ĐẶT
-----------------------------
Để chạy phần mềm này, bạn cần cài đặt Python (phiên bản 3.10.11).

Các bước cài đặt chi tiết:

1. Cài đặt Python:
   - Tải và cài đặt Python 3.10.11 từ trang chủ python.org.
   - Khi cài đặt, nhớ tích vào ô "Add Python to PATH".

2. Tạo môi trường ảo (Virtual Environment - Khuyến nghị):
   - Mở Terminal (Command Prompt hoặc PowerShell) tại thư mục dự án.
   - Chạy lệnh sau để tạo môi trường tên là ".venv":
     python -m venv .venv
   
3. Kích hoạt môi trường ảo:
   - Trên Windows (Command Prompt):
     .venv\Scripts\activate
   - Trên Windows (PowerShell):
     .venv\Scripts\Activate.ps1
     (Nếu lỗi quyền hạn, chạy lệnh: Set-ExecutionPolicy Unrestricted -Scope Process)
   - Trên macOS/Linux:
     source .venv/bin/activate
   
   *Sau khi kích hoạt, bạn sẽ thấy (.venv) ở đầu dòng lệnh.*

4. Cài đặt thư viện:
   - Chạy lệnh sau để cài đúng phiên bản các thư viện cần thiết:
     pip install -r requirements.txt

2. CÁCH CHẠY ỨNG DỤNG
---------------------
Sau khi cài đặt xong thư viện, bạn chạy lệnh sau để mở ứng dụng:

    -python main.py
    - Hoặc có thể chạy bằng cách nhấn vào nút chạy trong IDE khi ở trong file main.py

3. HƯỚNG DẪN SỬ DỤNG
--------------------
A. Menu Chính:
   - "Bắt Đầu Tập Luyện" (Start Workout): Chọn một bài tập có sẵn để bắt đầu.
   - "Tạo Phiên Tập" (Create Session): Tự thiết kế bài tập riêng (ví dụ: Squat 3 hiệp, mỗi hiệp 10 lần).
   - "Tạo Kế Hoạch" (Workout Planner): Tạo lịch tập văn bản dựa trên thời gian rảnh của bạn.
   - "Cài Đặt" (Settings): Thay đổi ngôn ngữ (Tiếng Việt / English).

B. Trong Khi Tập Luyện:
   - Đảm bảo ánh sáng tốt và đứng cách camera khoảng 2-3 mét để AI nhìn thấy toàn bộ cơ thể.
   - Nhấn "Bật Camera" để bắt đầu.
   - Thực hiện động tác (ví dụ: Squat hoặc Bicep Curl).
   - AI sẽ tự động đếm số lần (Reps) khi bạn thực hiện đúng động tác.
   - Nếu tư thế sai, AI sẽ cảnh báo bằng giọng nói và dòng chữ màu đỏ.
   - Hoàn thành số Reps mục tiêu để kết thúc Hiệp (Set) và chuyển sang bài tiếp theo.

4. LƯU Ý KHI SỬ DỤNG (QUAN TRỌNG)
------------------------------------
- Khi mở camera trong khi tập luyện(khi bấm vào nút "Bật Camera") phần mềm sẽ mất một khoảng thời gian để khởi động camera, nhận diện cơ thể , quét cơ thể,...
tùy vào cấu hình của thiết bị chạy chương trình 
- KỂ CẢ KHI PHẦN MỀM CÓ VẺ ĐANG CRASH VÀ KHÔNG PHẢN HỒI(CỬA SỔ HIỆN "NOT RESPONDING" TRÊN WINDOWS), HÃY KIÊN NHẪN ĐỢI THÊM 1-2 PHÚT NỮA, NẾU VẪN KHÔNG ĐƯỢC
THÌ RESET PHẦN MỀM 
- Lưu ý khi chọn môi trường luyện tập vì kết quả nhận diện có thể bị ảnh hưởng bởi ánh sáng, góc quay camera hoặc trang phục.
==================================================

