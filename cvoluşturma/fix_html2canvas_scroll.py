with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = text.replace("backgroundColor: '#ffffff'", "backgroundColor: '#ffffff',\n                scrollX: 0,\n                scrollY: 0")

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
