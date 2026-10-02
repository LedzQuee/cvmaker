with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find the end of bindDynamicEntryEvents — the last part handles entry field changes
# We need to add date picker sync AFTER the existing querySelectorAll('[data-entry-field]') block
# The function ends with the updatePreview(); block and closing })}); 

# Find the function and add date picker binding at the end before closing
old_snippet = "        // nput de\u011fi\u015fiklikleri\n        container.querySelectorAll('[data-entry-field]').forEach(function (input) {\n            ['input', 'change'].forEach(function(evt) {"

if old_snippet not in text:
    # Try with ascii alternative
    print("Snippet not found exactly, searching...")
    idx = text.find("container.querySelectorAll('[data-entry-field]')")
    print(f"Found at: {idx}")
    print(repr(text[max(0,idx-200):idx+100]))
else:
    print("Found snippet")

