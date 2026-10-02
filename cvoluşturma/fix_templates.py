with open("wwwroot/js/cv-templates.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# 1. Update pct logic for sidebar-skill-bar
old_pct_block = """                var lvl = (s.level || '').toLowerCase();
                var pct = 40;
                if (lvl === 'expert' || lvl === 'uzman') pct = 95;
                else if (lvl === 'advanced' || lvl === 'i\\u015fleri' || lvl === 'ileri') pct = 80;
                else if (lvl === 'intermediate' || lvl === 'orta') pct = 60;
                else if (lvl === 'beginner' || lvl === 'ba\\u015flang\\u0131\\u00e7' || lvl.includes('ba')) pct = 25;
                h += '<div class="sidebar-skill-bar"><div class="sidebar-skill-fill" style="width:' + pct + '%"></div></div>';"""

# Fix the regex to match the pct block correctly
# A safer way to replace pct block across all files:
text = re.sub(
    r"var lvl = \(s\.level \|\| ''\)\.toLowerCase\(\);\s*var pct = 40;\s*if \([^\n]+\n\s*else if \([^\n]+\n\s*else if \([^\n]+\n\s*else if \([^\n]+\n\s*h \+= '<div class=\"sidebar-skill-bar\">.*?</div></div>';",
    r"""var lvl = (s.level || '').toLowerCase();
                var pct = 0;
                if (lvl === 'expert' || lvl === 'uzman') pct = 95;
                else if (lvl === 'advanced' || lvl === 'ileri' || lvl.includes('iler')) pct = 80;
                else if (lvl === 'intermediate' || lvl === 'orta') pct = 60;
                else if (lvl === 'beginner' || lvl === 'başlangıç' || lvl.includes('ba')) pct = 25;
                if (pct > 0) h += '<div class="sidebar-skill-bar"><div class="sidebar-skill-fill" style="width:' + pct + '%"></div></div>';""",
    text
)

# 2. Update BentoCard and Mono rendering to not show empty parenthesis
text = text.replace(
    r"esc(s.name) + ' (' + skillLabel(s.level) + ')'",
    r"esc(s.name) + (s.level ? ' (' + skillLabel(s.level) + ')' : '')"
)
text = text.replace(
    r"esc(s.name) + ' (' + langLabel(s.level) + ')'",
    r"esc(s.name) + (s.level ? ' (' + langLabel(s.level) + ')' : '')"
)


with open("wwwroot/js/cv-templates.js", "w", encoding="utf-8") as f:
    f.write(text)

print("OK: templates updated")
