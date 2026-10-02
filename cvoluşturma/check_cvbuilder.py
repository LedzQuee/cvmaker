with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'<label class="form-label">.*?irket.*?</label>', text)
if match:
    print(match.group(0).encode('utf-8'))
