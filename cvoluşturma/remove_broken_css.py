with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Remove the broken block
text = re.sub(r'    \n    body \* \{[\s\S]*?\}', '}', text, count=1)

# Let's do a cleaner replacement. The broken block is between .classic-skills { ... } and /* ============================== \n   PRINT STYLES
text = re.sub(r'\.cv-tpl-classic \.classic-skills \{\s*font-size: 14px;\s*line-height: 1\.6;\s*\}[\s\S]*?/\* ==============================(\r?\n)\s*PRINT STYLES \(Yazdır Modu\)', 
              '.cv-tpl-classic .classic-skills {\\n    font-size: 14px;\\n    line-height: 1.6;\\n}\\n\\n\\n/* ==============================\\1   PRINT STYLES (Yazdır Modu)', text)

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
