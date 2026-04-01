class RepCounter:
    def __init__(self):
        self.state = "WAITING" # Initial state
        self.count = 0
        self.threshold_down = 0
        self.threshold_up = 0
        
    def set_exercise(self, rule):
        """
        Sets the thresholds based on exercise.
        """
        self.threshold_up = rule["start_threshold"]
        self.threshold_down = rule["end_threshold"]
        self.count = 0
        self.state = "DOWN"

    def process(self, angle):
        """
        Process the current main angle (e.g., knee angle) and update count.
        Returns count and current state.
        """
        # Squat: Up (170) -> Down (90) -> Up (170)
        # Curl: Up (160) -> Down (30) -> Up (160)
        
        if self.state == "UP":
            if angle <= self.threshold_down:
                self.state = "DOWN"
        
        elif self.state == "DOWN":
            if angle >= self.threshold_up:
                self.state = "UP"
                self.count += 1
                return self.count, "COUNT"
                
        return self.count, self.state
