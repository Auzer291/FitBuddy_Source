import json
import os

class SessionManager:
    def __init__(self, filepath="sessions.json"):
        self.filepath = filepath
        self.sessions = self.load_sessions()

    def load_sessions(self):
        if not os.path.exists(self.filepath):
            # Return default sessions with default sets/reps
            return {
                "Quick Start": [
                    {"name": "Squat", "sets": 3, "reps": 10},
                    {"name": "Bicep Curl", "sets": 3, "reps": 10}
                ],
                "Leg Day": [
                    {"name": "Squat", "sets": 3, "reps": 12},
                    {"name": "Squat", "sets": 3, "reps": 12},
                    {"name": "Squat", "sets": 3, "reps": 12}
                ],
                "Arm Day": [
                    {"name": "Bicep Curl", "sets": 4, "reps": 10},
                    {"name": "Bicep Curl", "sets": 4, "reps": 10}
                ]
            }
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                # Migration: Ensure all items are dicts
                cleaned_data = {}
                for s_name, exercises in data.items():
                    cleaned_exercises = []
                    for ex in exercises:
                        if isinstance(ex, str):
                            # Convert old string format to default dict
                            cleaned_exercises.append({"name": ex, "sets": 3, "reps": 10})
                        else:
                            cleaned_exercises.append(ex)
                    cleaned_data[s_name] = cleaned_exercises
                return cleaned_data
        except (json.JSONDecodeError, IOError):
            return {}

    def save_session(self, name, exercises):
        self.sessions[name] = exercises
        self._save_to_file()

    def get_sessions(self):
        return self.sessions

    def get_session(self, name):
        return self.sessions.get(name, [])

    def delete_session(self, name):
        if name in self.sessions:
            del self.sessions[name]
            self._save_to_file()

    def _save_to_file(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.sessions, f, indent=4)
        except IOError as e:
            print(f"Error saving sessions: {e}")
