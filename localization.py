class LocalizationManager:
    def __init__(self, default_lang='vn'):
        self.current_lang = default_lang
        self.strings = {
            # Meta
            "app_title": {
                "en": "FitBuddy",
                "vn": "FitBuddy"
            },
            "subtitle": {
                "en": "Select an option to begin",
                "vn": "Chọn một tùy chọn để bắt đầu"
            },
            
            # Main Menu
            "btn_start_workout": {
                "en": "Start Workout",
                "vn": "Bắt Đầu Tập Luyện"
            },
            "btn_create_session": {
                "en": "Create Session",
                "vn": "Tạo Phiên Tập"
            },
            "btn_planner": {
                "en": "Workout Planner (Text)",
                "vn": "Lập Kế Hoạch (Văn Bản)"
            },
            "btn_settings": {
                "en": "Settings",
                "vn": "Cài Đặt"
            },
            "btn_exit": {
                "en": "Exit",
                "vn": "Thoát"
            },
            "btn_custom_ex": {
                "en": "Custom Exercise",
                "vn": "Bài Tập Tùy Chỉnh"
            },
            
            # Settings
            "title_settings": {
                "en": "Settings",
                "vn": "Cài Đặt"
            },
            "lbl_language": {
                "en": "Language / Ngôn Ngữ:",
                "vn": "Language / Ngôn Ngữ:"
            },
            "btn_lang_en": {
                "en": "English",
                "vn": "English"
            },
            "btn_lang_vn": {
                "en": "Tiếng Việt",
                "vn": "Tiếng Việt"
            },
            "lbl_theme": {
                "en": "Theme / Giao Diện:",
                "vn": "Theme / Giao Diện:"
            },
            "btn_theme_dark": {
                "en": "Dark Mode",
                "vn": "Giao Diện Tối"
            },
            "btn_theme_light": {
                "en": "Light Mode",
                "vn": "Giao Diện Sáng"
            },

            # Common
            "back": {"en": "Back", "vn": "Quay Lại"},
            "end_session": {"en": "End Session", "vn": "Kết Thúc"},
            
            # Session Creator
            "title_create": {
                "en": "Create New Session",
                "vn": "Tạo Phiên Tập Mới"
            },
            "lbl_session_name": {
                "en": "Session Name:",
                "vn": "Tên Phiên Tập:"
            },
            "ph_session_name": {
                "en": "Enter Session Name (e.g., 'Leg Blaster')",
                "vn": "Nhập Tên (ví dụ: 'Ngày Chân')"
            },
            "grp_add_exercise": {
                "en": "Add Exercise",
                "vn": "Thêm Bài Tập"
            },
            "btn_add": {
                "en": "Add",
                "vn": "Thêm"
            },
            "lbl_session_exercises": {
                "en": "Session Exercises:",
                "vn": "Danh Sách Bài Tập:"
            },
            "btn_save_session": {
                "en": "Save Session",
                "vn": "Lưu Phiên Tập"
            },
            
            # Session Select
            "title_select": {
                "en": "Select Workout Session",
                "vn": "Chọn Phiên Tập Luyện"
            },
            "btn_start_selected": {
                "en": "Start Selected Session",
                "vn": "Bắt Đầu"
            },

            # Planner
            "title_planner": {
                "en": "Workout Planner (Generator)",
                "vn": "Tạo Kế Hoạch Tập Luyện"
            },
            "grp_generate": {
                "en": "Generate a Text Plan",
                "vn": "Tạo Kế Hoạch"
            },
            "lbl_mins": {
                "en": "Minutes per Session:",
                "vn": "Số phút mỗi buổi:"
            },
            "lbl_days": {
                "en": "Days per Week:",
                "vn": "Số buổi mỗi tuần:"
            },
            "btn_generate": {
                "en": "Generate Plan",
                "vn": "Tạo Ngay"
            },
            "lbl_focus": {
                "en": "Focus Area",
                "vn": "Vùng Tập Trung"
            },
            "ph_result": {
                "en": "Your workout plan will appear here...",
                "vn": "Kế hoạch của bạn sẽ hiện ở đây..."
            },

            # Workout Screen
            "title_workout": {
                "en": "Workout Session",
                "vn": "Phiên Tập Luyện"
            },
            "grp_current_ex": {
                "en": "Current Exercise",
                "vn": "Bài Tập Hiện Tại"
            },
            "lbl_exercise": {
                "en": "Exercise:",
                "vn": "Bài Tập:"
            },
            "lbl_set": {
                "en": "Set:",
                "vn": "Hiệp:"
            },
            "lbl_progress": {
                "en": "Total Progress:",
                "vn": "Tiến Độ:"
            },
            "btn_start_cam": {
                "en": "Start Camera",
                "vn": "Bật Camera"
            },
            "btn_stop_cam": {
                "en": "Stop Camera",
                "vn": "Tắt Camera"
            },
            "btn_next_ex": {
                "en": "Next Exercise >>",
                "vn": "Bài Tiếp Theo >>"
            },
            "btn_finish_workout": {
                "en": "Finish Workout",
                "vn": "Hoàn Thành"
            },
            "grp_stats": {
                "en": "Live Stats",
                "vn": "Chỉ Số Trực Tiếp"
            },
            "lbl_reps": {
                "en": "Reps:",
                "vn": "Số Lần:"
            },
            "lbl_state": {
                "en": "State:",
                "vn": "Trạng Thái:"
            },
            "lbl_score": {
                "en": "Score:",
                "vn": "Điểm:"
            },
            "lbl_status": {
                "en": "Status:",
                "vn": "Tình Trạng:"
            },
            "status_ready": {
                "en": "Ready",
                "vn": "Sẵn Sàng"
            },
            "status_good": {
                "en": "Good Form",
                "vn": "Tốt"
            },
            "cam_error": {
                "en": "Camera Error",
                "vn": "Lỗi Camera"
            },
            "cam_stopped": {
                "en": "Camera Stopped",
                "vn": "Đã Tắt Camera"
            },
            
            # Messages
            "msg_set_complete": {
                "en": "Set Complete!",
                "vn": "Hoàn Thành Hiệp!"
            },
            "msg_take_rest": {
                "en": "Take a rest.",
                "vn": "Hãy nghỉ ngơi."
            },
            "msg_ex_complete": {
                "en": "Exercise Complete!",
                "vn": "Hoàn Thành Bài Tập!"
            },
            "msg_finished": {
                "en": "Finished",
                "vn": "Đã Xong"
            },
            "msg_workout_done": {
                "en": "Great job! Workout Session Complete.",
                "vn": "Làm tốt lắm! Buổi tập đã kết thúc."
            },
            "msg_error": {
                "en": "Error",
                "vn": "Lỗi"
            },
            "msg_enter_name": {
                "en": "Please enter a session name.",
                "vn": "Vui lòng nhập tên phiên tập."
            },
            "msg_add_one": {
                "en": "Please add at least one exercise.",
                "vn": "Vui lòng thêm ít nhất một bài tập."
            },
            "msg_saved": {
                "en": "Session saved!",
                "vn": "Đã lưu!"
            },
            "msg_success": {
                "en": "Success",
                "vn": "Thành Công"
            },
        }

    def get(self, key):
        return self.strings.get(key, {}).get(self.current_lang, key)

    def set_language(self, lang):
        if lang in ['en', 'vn']:
            self.current_lang = lang
