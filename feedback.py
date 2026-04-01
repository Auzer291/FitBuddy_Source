import cv2
import pyttsx3
import threading

class FeedbackSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set property for Vietnamese voice if available, else default
        # self.engine.setProperty('voice', ...) 
        self.last_speech = ""

    def draw_overlay(self, frame, exercise_name, count, state, feedback_text):
        """
        Draws the overlay on the frame.
        """
        # Draw transparent box for stats
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (280, 150), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)
        
        # Text
        cv2.putText(frame, f"Exercise: {exercise_name}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Reps: {count}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"State: {state}", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Feedback color
        color = (0, 255, 0) if "Good" in feedback_text else (0, 0, 255)
        cv2.putText(frame, f"{feedback_text}", (10, 140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame

    def play_audio(self, text):
        """
        Plays audio in a separate thread to avoid blocking.
        """
        if text != self.last_speech: # Avoid repeating same message immediately
            self.last_speech = text
            threading.Thread(target=self._speak, args=(text,)).start()

    def _speak(self, text):
        try:
             # Re-init engine in thread might be safer or lock
             # pyttsx3 often has issues with threads. 
             # Safe approach: usage of simple queue or only short blocking calls.
             # For MVP, try simple runAndWait
             engine = pyttsx3.init() 
             engine.say(text)
             engine.runAndWait()
        except:
            pass
