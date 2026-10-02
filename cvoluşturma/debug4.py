with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

# Find all occurrences of updatePreview(); and show context
import re
matches = [(m.start(), text[m.start():m.start()+200]) for m in re.finditer(r'updatePreview\(\);', text)]
for i, (idx, ctx) in enumerate(matches):
    print(f"--- #{i} at {idx} ---")
    print(repr(ctx[:150]))
    print()
