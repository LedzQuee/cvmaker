import re
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix bindPersonalInfoEvents
text = re.sub(r'(clearValidation\(this\);\s*updatePreview\(\);\s*)\}\);\s*\}\);\s*\}\);', r'\1});\n        });', text)

# Fix bindProfileSummaryEvents
text = re.sub(r'(CVDataManager\.updateProfileSummary\(this\.value\.trim\(\)\);\s*updatePreview\(\);\s*)\}\);\s*\}\);', r'\1});', text)

# Fix initTemplateSelector
text = re.sub(r'(CVTemplateManager\.setTemplate\(selectedId\);\s*updatePreview\(\);\s*)\}\);\s*\}\);', r'\1});', text)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
