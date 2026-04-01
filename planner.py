class WorkoutPlanner:
    def __init__(self):
        pass

    # Exercises grouped by body part  (name_en, reps_en, name_vn, reps_vn)
    EXERCISES = {
        "full_body": [
            ("Burpees",         "10-12 reps",                  "Burpees",           "10-12 lần"),
            ("Jump Squats",     "12-15 reps",                  "Squat Nhảy",        "12-15 lần"),
            ("Mountain Climbers","30 seconds",                  "Leo Núi",           "30 giây"),
            ("Thrusters",       "10 reps",                     "Thrusters",         "10 lần"),
            ("Deadlift",        "8-10 reps",                   "Deadlift",          "8-10 lần"),
        ],
        "upper_body": [
            ("Push-ups",        "12-15 reps",                  "Hít Đất",           "12-15 lần"),
            ("Bicep Curls",     "10-12 reps (each arm)",       "Curl Tay",          "10-12 lần (mỗi tay)"),
            ("Shoulder Press",  "10-12 reps",                  "Đẩy Vai",           "10-12 lần"),
            ("Tricep Dips",     "12 reps",                     "Chống Tay Sau",     "12 lần"),
            ("Lateral Raises",  "12 reps",                     "Dang Ngang Vai",    "12 lần"),
            ("Chest Flyes",     "10-12 reps",                  "Dang Ngực",         "10-12 lần"),
        ],
        "lower_body": [
            ("Squats",          "15 reps",                     "Squat",             "15 lần"),
            ("Lunges",          "12 reps each leg",            "Chân Bước",         "12 lần mỗi chân"),
            ("Calf Raises",     "20 reps",                     "Nhón Gót",          "20 lần"),
            ("Leg Press",       "12 reps",                     "Đẩy Chân",          "12 lần"),
            ("Glute Bridge",    "15 reps",                     "Cầu Mông",          "15 lần"),
            ("Step-ups",        "12 reps each leg",            "Bước Lên Bục",      "12 lần mỗi chân"),
        ],
        "core": [
            ("Plank",           "30-45 seconds",               "Plank",             "30-45 giây"),
            ("Crunches",        "20 reps",                     "Gập Bụng",          "20 lần"),
            ("Bicycle Crunches","15 reps each side",           "Đạp Xe Nằm",        "15 lần mỗi bên"),
            ("Leg Raises",      "12-15 reps",                  "Nâng Chân",         "12-15 lần"),
            ("Russian Twists",  "15 reps each side",           "Xoay Thân",         "15 lần mỗi bên"),
            ("Side Plank",      "25 seconds each side",        "Plank Nghiêng",     "25 giây mỗi bên"),
        ],
        "cardio": [
            ("Jumping Jacks",   "40 reps",                     "Nhảy Dang Tay",     "40 lần"),
            ("High Knees",      "30 seconds",                  "Chạy Gối Cao",      "30 giây"),
            ("Box Jumps",       "10 reps",                     "Nhảy Hộp",          "10 lần"),
            ("Jump Rope",       "60 seconds",                  "Nhảy Dây",          "60 giây"),
            ("Skater Jumps",    "20 reps",                     "Nhảy Trượt Băng",   "20 lần"),
        ],
    }

    BODY_PART_LABELS = {
        "en": {
            "full_body":  "Full Body",
            "upper_body": "Upper Body",
            "lower_body": "Lower Body",
            "core":       "Core",
            "cardio":     "Cardio",
        },
        "vn": {
            "full_body":  "Toàn Thân",
            "upper_body": "Thân Trên",
            "lower_body": "Thân Dưới",
            "core":       "Cơ Lõi",
            "cardio":     "Cardio",
        },
    }

    def create_plan(self, minutes, days_per_week, body_parts=None, lang="en"):
        """Generate a targeted workout plan in the given language."""
        if minutes < 10:
            return ("⚠️  Quá ngắn! Hãy thử ít nhất 10 phút."
                    if lang == "vn" else
                    "⚠️  Too short! Try at least 10 minutes.")

        if not body_parts:
            body_parts = ["full_body"]

        # Gather exercises (index 0-1 = EN, 2-3 = VN)
        exercise_pool = []
        for part in body_parts:
            exercise_pool.extend(self.EXERCISES.get(part, []))

        seen, unique_exercises = set(), []
        for ex in exercise_pool:
            if ex[0] not in seen:
                seen.add(ex[0])
                unique_exercises.append(ex)

        main_time = minutes - 4
        sets = max(1, main_time // 3)
        selected = [unique_exercises[i % len(unique_exercises)] for i in range(min(sets, 6))]

        labels = self.BODY_PART_LABELS.get(lang, self.BODY_PART_LABELS["en"])
        part_names = " + ".join(labels.get(p, p) for p in body_parts)

        if lang == "vn":
            plan  = f"🏋️  Kế Hoạch Tập Luyện — {part_names}\n"
            plan += f"📅  {days_per_week} buổi/tuần  |  ⏱  {minutes} phút/buổi\n"
            plan += "─" * 48 + "\n\n"
            plan += "🔥  Khởi Động (2 phút)\n"
            plan += "    Nhảy dang tay + xoay tay + giãn cơ nhẹ\n\n"
            plan += f"💪  Bài Chính ({sets} vòng)\n"
            for *_, name_vn, reps_vn in selected:
                plan += f"    • {name_vn}: {reps_vn}\n"
            plan += "    • Nghỉ: 60 giây giữa các vòng\n\n"
            plan += "🧊  Thư Giãn (2 phút)\n"
            plan += "    Giãn cơ toàn thân + hít thở sâu\n\n"
            plan += "─" * 48 + "\n"
            plan += f"✅  Lịch: Lặp lại {days_per_week}x mỗi tuần để đạt kết quả tốt nhất!\n"
        else:
            plan  = f"🏋️  Workout Plan — {part_names}\n"
            plan += f"📅  {days_per_week} days/week  |  ⏱  {minutes} mins/session\n"
            plan += "─" * 48 + "\n\n"
            plan += "🔥  Warm-up (2 min)\n"
            plan += "    Jumping jacks + arm circles + light stretching\n\n"
            plan += f"💪  Main Workout ({sets} rounds)\n"
            for name_en, reps_en, *_ in selected:
                plan += f"    • {name_en}: {reps_en}\n"
            plan += "    • Rest: 60 sec between rounds\n\n"
            plan += "🧊  Cool-down (2 min)\n"
            plan += "    Full-body stretching + deep breathing\n\n"
            plan += "─" * 48 + "\n"
            plan += f"✅  Schedule: Repeat {days_per_week}x per week for best results!\n"

        return plan
