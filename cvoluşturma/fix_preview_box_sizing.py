with open('wwwroot/css/cv-builder.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'(\.preview-container\s*\{[\s\S]*?width:\s*210mm;)', r'\1\n    box-sizing: border-box;', text)

with open('wwwroot/css/cv-builder.css', 'w', encoding='utf-8') as f:
    f.write(text)
