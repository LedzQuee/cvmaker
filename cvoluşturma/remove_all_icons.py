with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'<svg width="16" height="16"[\s\S]*?</svg>', '', text)
text = re.sub(r'<svg width="20" height="20"[\s\S]*?</svg>', '', text)

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
