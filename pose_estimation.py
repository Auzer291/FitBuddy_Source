import cv2
import mediapipe as mp

class PoseEstimator:
    def __init__(self, mode=False, complexity=2, smooth=True, 
                 detection_con=0.5, track_con=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=mode,
            model_complexity=complexity,
            smooth_landmarks=smooth,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        Processes the frame to detect pose landmarks.
        Returns the processed frame and the results object.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        return results

    def draw_landmarks(self, frame, results):
        """
        Draws pose landmarks on the frame.
        """
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS
            )
        return frame

    def get_landmarks(self, results):
        """
        Extracts landmarks as a list.
        """
        if not results.pose_landmarks:
            return None
        return results.pose_landmarks.landmark
