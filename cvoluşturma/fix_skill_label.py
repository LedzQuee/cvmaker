with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

old_skill_label = r"function skillLabel\(lvl\) \{[\s\S]*?return lvl;\s*\}"
new_skill_label = '''function skillLabel(lvl) {
        if (!lvl) return '';
        var l = lvl.toLowerCase();
        if (l === 'beginner' || l === 'başlangıç' || l.includes('ba')) return 'Başlangıç';
        if (l === 'intermediate' || l === 'orta') return 'Orta';
        if (l === 'advanced' || l === 'i̇leri' || l === 'ileri') return 'İleri';
        if (l === 'expert' || l === 'uzman') return 'Uzman';
        return lvl;
    }'''

text = re.sub(old_skill_label, new_skill_label, text)

with open('wwwroot/js/cv-templates.js', 'w', encoding='utf-8') as f:
    f.write(text)
