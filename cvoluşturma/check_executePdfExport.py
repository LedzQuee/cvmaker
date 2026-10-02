import re
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see what executePdfExport looks like now
match = re.search(r'function executePdfExport[\s\S]*?\}\);', text)
if match:
    print(match.group(0))
