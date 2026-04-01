from angle_calculation import calculate_angle

class PostureEvaluator:
    def __init__(self):
        pass

    def check_squat(self, landmarks, side="left"):
        """
        Checks squat posture. 
        Returns (is_correct, feedback_message)
        """
        # Get coordinates
        # Map landmarks to indices based on MediaPipe Pose
        # 23: left_hip, 25: left_knee, 27: left_ankle
        # 11: left_shoulder
        
        # Simplified: using left side by default as per MVP
        hip = [landmarks[23].x, landmarks[23].y]
        knee = [landmarks[25].x, landmarks[25].y]
        ankle = [landmarks[27].x, landmarks[27].y]
        
        knee_angle = calculate_angle(hip, knee, ankle)
        
        # Rule 1: Knee angle safe range at bottom
        # This check is context-dependent (are we at the bottom?)
        # For real-time check, we often check if it violates safe MAX range during movement?
        # Actually, for squat, the "bad" posture is usually knees buckling or going too deep if flexible?
        # Or back bending.
        
        # MVP Rule: If knee angle < 70 (too deep dangerous) -> Warn
        if knee_angle < 70:
             return False, "Knee bent too much!"
        
        return True, "Good Posture"

    def check_curl(self, landmarks, side="left"):
        """
        Checks bicep curl.
        """
        # Shoulder-Elbow-Wrist
        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]
        
        # Check for swinging? (Elbow moving too much) - Hard with single frame
        # MVP: Check if elbow is stable relative to shoulder?
        # For MVP, maybe just check if arm is fully extended at bottom?
        
        return True, "Good Posture"
