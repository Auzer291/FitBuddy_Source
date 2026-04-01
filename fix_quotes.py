import re

FILE = r"c:\Users\ADMIN\Desktop\FitBuddy - Source Code\gui.py"

with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Just replace Theme.t["PROP"] with Theme.t['PROP']
text = re.sub(r'Theme\.t\["([^"]+)"\]', r"Theme.t['\1']", text)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("Double quotes inside f-strings resolved.")
