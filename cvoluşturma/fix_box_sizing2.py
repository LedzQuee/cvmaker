with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'(\.cv-tpl\s*\{[^}]*?)(box-sizing:\s*border-box;)?([^}]*?\})', r'\1box-sizing: border-box;\3\n.cv-tpl *, .cv-tpl *::before, .cv-tpl *::after { box-sizing: border-box; }', text, count=1)

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
