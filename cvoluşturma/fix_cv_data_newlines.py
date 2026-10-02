with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any literal newline inside single quotes that start with '- '
import re
def remove_newlines(match):
    s = match.group(0)
    s = s.replace('\n', ' ')
    s = s.replace('\r', ' ')
    return s

text = re.sub(r'description:\s*\'[^\']*\'', remove_newlines, text)

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
