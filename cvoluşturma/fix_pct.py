with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Fix pct calculation
old_pct = r"var pct = s\.level === 'expert' \? 95 : s\.level === 'advanced' \? 80 : s\.level === 'intermediate' \? 60 : 40;"
new_pct = '''var lvl = (s.level || '').toLowerCase();
                var pct = 40;
                if (lvl === 'expert' || lvl === 'uzman') pct = 95;
                else if (lvl === 'advanced' || lvl === 'i̇leri' || lvl === 'ileri') pct = 80;
                else if (lvl === 'intermediate' || lvl === 'orta') pct = 60;
                else if (lvl === 'beginner' || lvl === 'başlangıç' || lvl.includes('ba')) pct = 25;'''

text = re.sub(old_pct, new_pct, text)

with open('wwwroot/js/cv-templates.js', 'w', encoding='utf-8') as f:
    f.write(text)
