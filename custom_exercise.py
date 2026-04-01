import cv2
import json
import os
import numpy as np
from pose_estimation import PoseEstimator
from angle_calculation import calculate_angle

CUSTOM_EXERCISES_FILE = "custom_exercises.json"

JOINTS_TO_TRACK = {
    "left_arm": (11, 13, 15),
    "right_arm": (12, 14, 16),
    "left_leg": (23, 25, 27),
    "right_leg": (24, 26, 28),
    "left_hip": (11, 23, 25),
    "right_hip": (12, 24, 26)
}

class CustomExerciseManager:
    def __init__(self):
        self.exercises = self.load_custom_exercises()

    def load_custom_exercises(self):
        if not os.path.exists(CUSTOM_EXERCISES_FILE):
            return {}
        try:
            with open(CUSTOM_EXERCISES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_custom_exercise(self, rule):
        self.exercises[rule["name"]] = rule
        try:
            with open(CUSTOM_EXERCISES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.exercises, f, indent=4)
            return True
        except Exception:
            return False

    def get_custom_rules(self):
        return self.exercises

class VideoAnalyzer:
    def __init__(self):
        self.pose_estimator = PoseEstimator(mode=False, complexity=1)

    def analyze_video(self, video_path, exercise_name):
        """
        Analyzes a video file to determine the most active joint and its angle range.
        Returns a rule dictionary compatible with ExerciseRules.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Cannot open video file.")

        joint_angles_over_time = {k: [] for k in JOINTS_TO_TRACK.keys()}

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            results = self.pose_estimator.process_frame(frame)
            landmarks = self.pose_estimator.get_landmarks(results)
            
            if landmarks:
                for joint_name, (idx1, idx2, idx3) in JOINTS_TO_TRACK.items():
                    p1 = [landmarks[idx1].x, landmarks[idx1].y]
                    p2 = [landmarks[idx2].x, landmarks[idx2].y]
                    p3 = [landmarks[idx3].x, landmarks[idx3].y]
                    angle = calculate_angle(p1, p2, p3)
                    joint_angles_over_time[joint_name].append(angle)

        cap.release()

        # Find the joint with the highest variance
        max_variance = -1.0
        best_joint = ""
        
        for joint_name, angles in joint_angles_over_time.items():
            if len(angles) < 10:
                continue # not enough data
            variance = float(np.var(angles))
            if variance > max_variance:
                max_variance = variance
                best_joint = str(joint_name)
                
        if not best_joint:
            raise Exception("Could not detect sufficient movement in the video.")

        # Determine thresholds
        angles = list(joint_angles_over_time[best_joint])
        min_angle = np.min(angles)
        max_angle = np.max(angles)

        # We'll set start_threshold to max_angle with slight padding, end_threshold to min_angle with slight padding
        start_threshold = min(180, max_angle - 5)
        end_threshold = max(0, min_angle + 10)

        idx1, idx2, idx3 = JOINTS_TO_TRACK[best_joint]

        rule = {
            "name": exercise_name,
            "joint_angles": ["p1", "p2", "p3"],
            "start_threshold": int(start_threshold),
            "end_threshold": int(end_threshold),
            "landmarks": {
                "p1": idx1,
                "p2": idx2,
                "p3": idx3
            }
        }
        
        return rule
