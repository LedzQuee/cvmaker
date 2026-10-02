with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Update renderSkillForm to make level optional
text = re.sub(
    r"'<label class=\"form-label\">Seviye</label>' \+\s*'<select class=\"form-select\" data-entry-field=\"level\">' \+ levelOptions \+ '</select>'",
    r"""'<label class="form-label">Seviye <span style="color:#94a3b8;font-weight:400;font-size:12px;">(isteğe bağlı)</span></label>' +
                '<select class="form-select" data-entry-field="level"><option value="">Belirtmek istemiyorum</option>' + levelOptions + '</select>'""",
    text
)

# Also update language level just in case
text = re.sub(
    r"'<label class=\"form-label\">Seviye</label>' \+\s*'<select class=\"form-select\" data-entry-field=\"level\">' \+ levelOptions \+ '</select>'",
    r"""'<label class="form-label">Seviye <span style="color:#94a3b8;font-weight:400;font-size:12px;">(isteğe bağlı)</span></label>' +
                '<select class="form-select" data-entry-field="level"><option value="">Belirtmek istemiyorum</option>' + levelOptions + '</select>'""",
    text
)

with open("wwwroot/js/cv-builder.js", "w", encoding="utf-8") as f:
    f.write(text)

print("OK: cv-builder updated")
