with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find the closing of bindDynamicEntryEvents 
# It ends after the last }); inside the function
# We'll inject the date picker binding block just before the closing brace of the function

# Locate "container.querySelectorAll('[data-entry-field]')" block and find its end
target_marker = "            updatePreview();\n                });\n              });\n          });\n      }"

# Print what's there
idx = text.find("updatePreview();\n                });\n              });\n          });\n      }")
print(f"Found at idx: {idx}")
print(repr(text[idx:idx+150]))
