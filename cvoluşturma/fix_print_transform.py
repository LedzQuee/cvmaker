with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find the #previewContent inside @media print
# We will just append it to the #previewContent rule
text = re.sub(r'(#previewContent\s*\{[\s\S]*?padding:\s*0\s*!important;)', r'\1\n        transform: none !important;', text)

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
