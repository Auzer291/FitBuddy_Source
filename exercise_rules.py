class ExerciseRules:
    
    @staticmethod
    def get_squat_rules():
        """
        Returns thresholds for Squat.
        """
        return {
            "name": "Squat",
            "joint_angles": ["hip", "knee", "ankle"], # Key joints
            "start_threshold": 170, # Standing up (approx straight leg)
            "end_threshold": 90,    # Squat down (knee angle) - adjustable
            "safe_knee_min": 70,
            "safe_knee_max": 120,    # Relaxed max for bottom position
            "landmarks": {
                "hip": 23,  # LEFT_HIP (using left side for simplicity, ideally auto-detect side)
                "knee": 25, # LEFT_KNEE
                "ankle": 27 # LEFT_ANKLE
            }
        }

    @staticmethod
    def get_curl_rules():
        """
        Returns thresholds for Bicep Curl.
        """
        return {
            "name": "Bicep Curl",
            "joint_angles": ["shoulder", "elbow", "wrist"],
            "start_threshold": 160, # Arm straight
            "end_threshold": 30,    # Arm curled
            "landmarks": {
                "shoulder": 11, # LEFT_SHOULDER
                "elbow": 13,    # LEFT_ELBOW
                "wrist": 15     # LEFT_WRIST
            }
        }

    @staticmethod
    def get_push_up_rules():
        """
        Returns thresholds for Push Up.
        """
        return {
            "name": "Push Up",
            "joint_angles": ["shoulder", "elbow", "wrist"],
            "start_threshold": 160, # Arm straight
            "end_threshold": 80,    # Arm bent
            "landmarks": {
                "shoulder": 11, # LEFT_SHOULDER
                "elbow": 13,    # LEFT_ELBOW
                "wrist": 15     # LEFT_WRIST
            }
        }
