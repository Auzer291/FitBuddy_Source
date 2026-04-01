class Scorer:
    def __init__(self):
        self.total_frames = 0
        self.correct_posture_frames = 0
    
    def update(self, is_correct_posture):
        """
        Updates the scoring stats per frame.
        """
        self.total_frames += 1
        if is_correct_posture:
            self.correct_posture_frames += 1
            
    def get_score(self):
        """
        Returns the score out of 100.
        """
        if self.total_frames == 0:
            return 0
        return int((self.correct_posture_frames / self.total_frames) * 100)
    
    def reset(self):
        self.total_frames = 0
        self.correct_posture_frames = 0
