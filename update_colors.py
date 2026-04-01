import re

FILE = r"c:\Users\ADMIN\Desktop\FitBuddy - Source Code\gui.py"

with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

COLORS = [
    "BG_DEEP", "BG_SURFACE", "BG_CARD", "BG_CARD2", "BORDER", "BORDER_HL",
    "PRI", "PRI_LIGHT", "PRI_DARK", "SEC", "SEC_DARK", "DANGER", "DANGER_DARK",
    "TEXT_PRI", "TEXT_SEC", "TEXT_MUTED"
]

# Split before helpers so we don't mess up THEMES dict
idx = text.find("# ── Helpers ───────────────────────────────────")
header = text[:idx]
body = text[idx:]

for prop in COLORS:
    # Only replace unquoted exact matches (to avoid replacing if they were somehow in strings, 
    # but actually we want to replace them in f-strings like {PRI}, 
    # wait our regex \bPRI\b works on {PRI}.
    # Let's just do it on the body where they are used.
    body = re.sub(r'\b' + prop + r'\b', f'Theme.t["{prop}"]', body)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(header + body)

print("Replacement complete.")
