with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()
import re
matches = re.findall(r'.{0,10}Ünvan.{0,10}', text)
print(matches)
