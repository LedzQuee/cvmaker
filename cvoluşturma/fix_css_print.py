with open("wwwroot/css/cv-templates.css", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Fix the print media block in CSS by removing padding: 0; and min-height: 297mm;
text = re.sub(
    r"\.cv-tpl \{\s*width: 100% !important;\s*height: 100% !important;\s*min-height: 297mm !important;\s*margin: 0 !important;\s*padding: 0;\s*box-shadow: none !important;\s*\}",
    r".cv-tpl {\n        width: 100% !important;\n        margin: 0 !important;\n        box-shadow: none !important;\n    }",
    text
)

# Also fix the sidebar min-height
text = text.replace("min-height: 297mm; /* A4 */", "min-height: 100%;")

with open("wwwroot/css/cv-templates.css", "w", encoding="utf-8") as f:
    f.write(text)

print("OK: cv-templates.css fixed")
