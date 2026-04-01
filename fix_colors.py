FILE = r"c:\Users\ADMIN\Desktop\FitBuddy - Source Code\gui.py"
import re
with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Fix Theme.t['Theme.t["PROP"]'] double wraps
text = re.sub(r'Theme\.t\[\'Theme\.t\["([^"]+)"\]\'\]', r'Theme.t["\1"]', text)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(text)
print("Double wraps fixed.")
