with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find the exact input event binding inside bindDynamicEntryEvents
idx = text.find("container.querySelectorAll('[data-entry-field]').forEach")
print(f"Found at: {idx}")
print(repr(text[idx:idx+600]))
