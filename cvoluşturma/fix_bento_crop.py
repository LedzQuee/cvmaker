with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Add box-sizing: border-box to .cv-tpl-bento
text = re.sub(r'(\.cv-tpl-bento\s*\{\s*font-family:[^;]+;\s*background:[^;]+;\s*padding:\s*20px;)', r'\1\n    box-sizing: border-box;', text)

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
