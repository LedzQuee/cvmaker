with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Add transition: none !important to #previewContent in print
text = re.sub(r'(#previewContent\s*\{[\s\S]*?transform:\s*none\s*!important;)', r'\1\n        transition: none !important;', text)

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
